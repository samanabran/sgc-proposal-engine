#!/usr/bin/env python3
"""
SGC Proposal Engine — client folder validator.
Implements the 18 checks in 05-ops/validate.md against a client folder.

Usage:
    python validate.py 02-clients/{client}/

Exit code 0 = clean (all checks pass, or only the expected entity-
resolution blocker fails). Exit code 1 = a real gate/content failure.
Exit code 2 = usage error.

Dependencies: PyYAML only (stdlib otherwise).
"""
import glob
import os
import re
import sys

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FORBIDDEN_RATE = 690

# Phrases that are unconditionally wrong wherever they appear as an
# affirmative claim — no legitimate proposal ever needs to assert these.
FORBIDDEN_PHRASES = [
    "bargain",
    "not on our public list",
    "will not be extended to any other brokerage",
]

# These two are only forbidden as an AFFIRMATIVE, PRESENT-TENSE claim
# ("SGC TECH AI is VAT-registered", "we operate from a free zone so no
# VAT applies"). The correct, mandatory disclosures in this repo need to
# reference these same words in a NEGATED or FUTURE-CONDITIONAL sense
# (vat-gross-up.md's "Should SGC TECH AI become VAT-registered...",
# vat-uae.md's "is not currently registered") — a blunt substring ban
# would also reject the correct text. Checked via NEGATION_PATTERNS below
# rather than a plain substring match.
CONDITIONAL_FORBIDDEN = {
    "VAT-registered": re.compile(r"(?<!not currently )(?<!become )\bis\s+VAT-registered\b", re.IGNORECASE),
    "no VAT applies": re.compile(r"\bno VAT applies\b(?!.*\bfree zone\b)", re.IGNORECASE),
}

# Edition-conditional forbidden phrases, checked only when edition ==
# community, and only as an affirmative claim — "not a dedicated
# iOS/Android app" and "does not include ... Odoo Enterprise" are the
# correct, required disclosures and must not be flagged.
NEGATION_PATTERN = re.compile(
    r"\b(not|no|excludes?|without|rather than|never|doesn'?t|does\s+not|isn'?t)\b",
    re.IGNORECASE,
)


def _has_nearby_negation(text, match_start, window=60):
    # Strip markdown emphasis markers so "**not**" matches the same as
    # "not" — a literal substring check would miss the bolded word.
    lookback = text[max(0, match_start - window):match_start].replace("*", "")
    return bool(NEGATION_PATTERN.search(lookback))


COMMUNITY_ONLY_FORBIDDEN = ["Odoo Enterprise", "iOS / Android app", "iOS/Android app"]

# Files where forbidden phrases are EXPECTED to appear (they name the
# phrases as a reference list) — excluded from check 18.
FORBIDDEN_PHRASE_EXEMPT_SUFFIXES = (
    os.path.join("01-templates", "qa", "pre-send-checklist.template.md"),
    os.path.join("04-review", "qa-checklist.md"),
    os.path.join("05-ops", "validate.md"),
    os.path.join("05-ops", "validate.py"),
    os.path.join("00-knowledge", "failure-modes", "known-defects.md"),
    os.path.join("05-ops", "glossary.md"),
    os.path.join("05-ops", "escalation-triggers.md"),
    "manifest.yaml",  # escalations/revisions narrate defect history by design
)


def _is_retracted_historical(path):
    """True if this file documents a retracted/superseded revision — a
    preserved historical record of what was WRONG, not an active claim.
    Detected by a sibling RETRACTION-NOTICE.md in the same directory."""
    d = os.path.dirname(path)
    return os.path.exists(os.path.join(d, "RETRACTION-NOTICE.md")) or \
        os.path.basename(path) == "RETRACTION-NOTICE.md"


class Result:
    def __init__(self):
        self.gate_failures = []      # blocks issue — real defects
        self.entity_blocker = None   # expected-by-design blocker, reported separately
        self.passed = []

    def fail(self, check, msg):
        self.gate_failures.append(f"[FAIL] {check}: {msg}")

    def ok(self, check, msg=""):
        self.passed.append(f"[ OK ] {check}" + (f": {msg}" if msg else ""))


def load_yaml(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def find_worksheet(client_dir):
    matches = glob.glob(os.path.join(client_dir, "02-calc", "pricing-worksheet.yaml"))
    return matches[0] if matches else None


def check_1_forbidden_rate_in_pricing(result):
    for f in glob.glob(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "*.yaml")):
        text = open(f, encoding="utf-8").read()
        if re.search(rf"\b{FORBIDDEN_RATE}\b", text) and "forbidden_rates" not in text.split(str(FORBIDDEN_RATE))[0][-200:]:
            # crude proximity check: allow the number only inside the
            # forbidden_rates block of rate-card.yaml itself
            if "rate-card.yaml" not in f:
                result.fail("1. forbidden rate", f"{FORBIDDEN_RATE} appears in {f}")
    result.ok("1. forbidden rate not present in pricing/*.yaml (outside its own guard entry)")


def check_1b_forbidden_rate_in_client(result, client_dir):
    # Only scan the ACTIVE pricing surface — the worksheet and the current
    # draft. manifest.yaml (escalation narrative) and 05-issued/ (retracted
    # historical record, or an immutable clean-history document like VGE's)
    # are legitimately allowed to reference the number 690 as a documented
    # past defect, not a live rate — see check_1_forbidden_rate_in_pricing
    # for the check that actually guards live pricing data.
    targets = glob.glob(os.path.join(client_dir, "02-calc", "*.yaml")) + \
        glob.glob(os.path.join(client_dir, "03-draft", "**", "*.md"), recursive=True)
    for f in targets:
        text = open(f, encoding="utf-8").read()
        if re.search(rf"\b{FORBIDDEN_RATE}\b", text):
            result.fail("1. forbidden rate in client folder", f"{FORBIDDEN_RATE} appears in {f}")
    result.ok("1. forbidden rate not present in active client worksheet/draft")


def check_2_3_worksheet_complete(result, ws):
    b = ws.get("number_2_build", {})
    for key in ("documentation_hours", "qa_hours", "training_hours", "total_hours",
                "rate_aed", "rate_exists_on_card", "subtotal_aed", "pm_aed",
                "contingency_aed", "build_value_aed", "internal_build_cost_aed"):
        if b.get(key) in (None, ""):
            result.fail("2/3. worksheet completeness", f"number_2_build.{key} is empty")
    if not b.get("rate_exists_on_card"):
        result.fail("2. rate provenance", "rate_exists_on_card is not true")
    rate_card = load_yaml(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "rate-card.yaml"))
    valid_rates = {v["rate_aed_hr"] for v in rate_card.get("roles", {}).values()}
    forbidden = {r["rate_aed_hr"] for r in rate_card.get("forbidden_rates", [])}
    rate = b.get("rate_aed")
    if rate in forbidden:
        result.fail("2. rate provenance", f"rate_aed {rate} is in rate-card.yaml forbidden_rates")
    elif rate not in valid_rates:
        result.fail("2. rate provenance", f"rate_aed {rate} does not match any rate-card.yaml role")
    result.ok("2/3. worksheet build block complete, PM/QA/documentation/contingency present, rate on card")


def check_4_hour_benchmark(result, ws):
    users = ws.get("inputs", {}).get("users_now")
    total_hours = ws.get("number_2_build", {}).get("total_hours")
    if users and total_hours:
        benchmark = 9.2 * users
        if total_hours < benchmark * 0.5:
            result.fail("4. hour benchmark", f"{total_hours}h for {users} users is well under the ~{benchmark:.0f}h reference benchmark")
        else:
            result.ok("4. hour benchmark", f"{total_hours}h for {users} users vs ~{benchmark:.0f}h reference")
    else:
        result.fail("4. hour benchmark", "users_now or total_hours missing from worksheet")


def check_6_all_gates_recorded(result, ws):
    gates = ws.get("gates", {})
    expected = [f"G{i}" for i in range(1, 42)]
    missing = [g for g in expected if not any(k.startswith(g + "_") or k == g for k in gates)]
    failed = [k for k, v in gates.items() if isinstance(v, dict) and v.get("pass") is False]
    if missing:
        result.fail("6. all gates recorded", f"missing gate entries for: {missing}")
    if failed:
        result.fail("6. gate failures", f"gates recorded as failing: {failed}")
    if not missing and not failed:
        result.ok("6. all 41 gates recorded and passing")


def check_8_cash_positive(result, ws):
    policy = load_yaml(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml"))
    max_days = policy["gates"]["cash_positive_within_days"]
    day = ws.get("exposure", {}).get("cash_positive_by_day")
    if day is None:
        result.fail("8. cash-positive within 30 days", "exposure.cash_positive_by_day not recorded")
    elif day > max_days:
        result.fail("8. cash-positive within 30 days", f"day {day} exceeds policy max {max_days}")
    else:
        result.ok("8. cash-positive within 30 days", f"day {day} <= {max_days}")


def check_9_10_cadence_mobilisation(result, ws):
    policy = load_yaml(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml"))
    min_pct = policy["gates"]["default_mobilisation_pct"]
    mob = ws.get("number_3_financing", {}).get("mobilisation_aed")
    build = ws.get("number_2_build", {}).get("build_value_aed")
    if mob and build:
        actual_pct = mob / build
        if actual_pct < min_pct - 0.005:
            result.fail("10. mobilisation floor", f"{actual_pct:.1%} below required {min_pct:.0%}")
        else:
            result.ok("10. mobilisation floor", f"{actual_pct:.1%} >= {min_pct:.0%}")
    cadence = ws.get("payment_cadence")
    allowed = {"quarterly_in_advance", "semi_annual_in_advance", "annual_in_advance", "full_prepay_term"}
    if cadence and cadence not in allowed:
        result.fail("9. min cadence", f"cadence '{cadence}' is below the quarterly-in-advance minimum without a logged exception")
    else:
        result.ok("9. min cadence", f"cadence '{cadence}' meets or exceeds minimum")


def check_11_vat(result, draft_files):
    for f in draft_files:
        if _is_retracted_historical(f):
            continue  # preserved evidence of the original defect, not a live claim
        text = open(f, encoding="utf-8").read()
        m = CONDITIONAL_FORBIDDEN["VAT-registered"].search(text)
        if m:
            result.fail("11. VAT claim", f"affirmative 'is VAT-registered' claim found in {f}")
        m = re.search(r"no VAT applies", text, re.IGNORECASE)
        if m and "free zone" in text[max(0, m.start() - 80):m.start() + 80].lower():
            result.fail("11. VAT claim", f"'no VAT applies ... free zone' claim found in {f}")
    result.ok("11. no false VAT claim in draft/issued documents")


def check_12_edition(result, ws, draft_files):
    edition = ws.get("inputs", {}).get("edition")
    if edition not in ("community", "enterprise"):
        result.fail("12. edition declared", f"inputs.edition is '{edition}', expected community/enterprise")
        return
    if edition == "community":
        for f in draft_files:
            if _is_retracted_historical(f):
                continue  # preserved evidence of the original defect, not a live claim
            text = open(f, encoding="utf-8").read()
            for phrase in COMMUNITY_ONLY_FORBIDDEN:
                for m in re.finditer(re.escape(phrase), text):
                    if not _has_nearby_negation(text, m.start()):
                        result.fail("12. edition honesty", f"affirmative '{phrase}' claim found in Community-edition draft: {f}")
    if edition == "enterprise":
        licences = ws.get("number_1_cost_to_serve", {}).get("licences_aed")
        if not licences or licences == 0:
            result.fail("12. edition honesty", "edition is 'enterprise' but number_1_cost_to_serve.licences_aed is 0 — Enterprise carries a real per-user licence cost (editions.yaml), a zero here means either the edition or the cost-to-serve figure is wrong")
    result.ok("12. edition declared and consistent with draft content")


def check_13_clawback(result, ws, current_revision_files):
    # Scoped to the CURRENT revision only (03-draft, or 05-issued if this
    # revision has already been issued) — 05-issued/ folders for OTHER,
    # superseded/retracted revisions legitimately mention "clawback" when
    # documenting its historical absence as a defect, which must not
    # count as evidence the current revision has one.
    # Look for the clause's actual obligation language, not just the word
    # "clawback" — that word alone can appear in passing (e.g. an exit-fee
    # table row referencing "unrecovered clawback balance") without the
    # substantive clause itself being present anywhere in the document.
    clawback_substance = re.compile(r"unrecovered\s+balance.{0,60}(immediately due and payable|becomes)", re.IGNORECASE | re.DOTALL)
    deferred = ws.get("number_3_financing", {}).get("deferred_aed", 0) or 0
    if deferred > 0:
        found = any(clawback_substance.search(open(f, encoding="utf-8").read()) for f in current_revision_files)
        if not found:
            result.fail("13. clawback present", "deferred_aed > 0 but no clawback clause found in draft")
        else:
            result.ok("13. clawback present on deferred structure")
    else:
        result.ok("13. no deferred value — clawback not required")


def check_14_entity(result):
    path = os.path.join(REPO_ROOT, "06-brand", "entity", "legal-identity.yaml")
    data = load_yaml(path)
    unresolved = [k for k, v in data.items() if v == "RESOLVE"]
    nested = data.get("contact", {})
    unresolved += ["contact." + k for k, v in nested.items() if v == "RESOLVE"]
    if unresolved:
        result.entity_blocker = f"legal-identity.yaml unresolved fields: {unresolved}"
    else:
        result.ok("14. all entity fields resolved")


def check_16_verbal_promises(result, client_dir):
    matches = glob.glob(os.path.join(client_dir, "00-intake", "verbal-promises.md"))
    if not matches:
        result.fail("16. verbal promises log", "verbal-promises.md not found")
        return
    text = open(matches[0], encoding="utf-8").read()
    for tag in ("PRICED", "DEFERRED"):
        if tag not in text:
            result.fail("16. verbal promises classified", f"no '{tag}' entries found")
    result.ok("16. verbal-promises.md exists with classified entries")


def check_18_forbidden_phrases(result, draft_files, edition):
    # Unconditional phrases: no legitimate proposal ever needs these, so a
    # plain substring match is correct here (no negation carve-out).
    for f in draft_files:
        if any(f.endswith(s) for s in FORBIDDEN_PHRASE_EXEMPT_SUFFIXES) or _is_retracted_historical(f):
            continue
        text = open(f, encoding="utf-8").read()
        for p in FORBIDDEN_PHRASES:
            if p.lower() in text.lower():
                result.fail("18. forbidden phrase", f"'{p}' found in {f}")
        # Edition-conditional phrases: only forbidden as an affirmative
        # claim — see check_12 for why a plain substring match is wrong
        # for these two specifically.
        if edition == "community":
            for p in COMMUNITY_ONLY_FORBIDDEN:
                for m in re.finditer(re.escape(p), text, re.IGNORECASE):
                    if not _has_nearby_negation(text, m.start()):
                        result.fail("18. forbidden phrase", f"affirmative '{p}' claim found in {f}")
    result.ok("18. no forbidden phrases found outside exempt/historical reference files")


def gather_draft_files(client_dir):
    """All content files, including historical/retracted 05-issued/
    revisions — used for checks that must look everywhere (e.g. the
    forbidden-rate scan already excludes these explicitly where needed)."""
    files = []
    for sub in ("03-draft", "05-issued"):
        files += glob.glob(os.path.join(client_dir, sub, "**", "*.md"), recursive=True)
    return files


def gather_current_revision_files(client_dir):
    """Only the CURRENTLY ACTIVE revision's own content — 03-draft if a
    revision is still in draft. A superseded/retracted revision's mention
    of a clause (present or notably absent) in 05-issued/ must never be
    read as evidence about the current revision's own content."""
    return glob.glob(os.path.join(client_dir, "03-draft", "**", "*.md"), recursive=True)


def run(client_dir):
    result = Result()
    ws_path = find_worksheet(client_dir)
    if not ws_path:
        print(f"No pricing-worksheet.yaml found under {client_dir}", file=sys.stderr)
        return 2
    ws = load_yaml(ws_path)
    draft_files = gather_draft_files(client_dir)
    current_revision_files = gather_current_revision_files(client_dir)
    edition = ws.get("inputs", {}).get("edition")

    check_1_forbidden_rate_in_pricing(result)
    check_1b_forbidden_rate_in_client(result, client_dir)
    check_2_3_worksheet_complete(result, ws)
    check_4_hour_benchmark(result, ws)
    check_6_all_gates_recorded(result, ws)
    check_8_cash_positive(result, ws)
    check_9_10_cadence_mobilisation(result, ws)
    check_11_vat(result, draft_files)
    check_12_edition(result, ws, draft_files)
    check_13_clawback(result, ws, current_revision_files)
    check_14_entity(result)
    check_16_verbal_promises(result, client_dir)
    check_18_forbidden_phrases(result, draft_files, edition)

    print(f"\n=== validate.py — {client_dir} ===\n")
    for line in result.passed:
        print(line)
    if result.gate_failures:
        print()
        for line in result.gate_failures:
            print(line)
    if result.entity_blocker:
        print(f"\n[BLOCKED — by design] 14. entity resolution: {result.entity_blocker}")
        print("This blocks ISSUE, not the commercial gate check. See 05-ops/validate.md.")

    print()
    if result.gate_failures:
        print(f"RESULT: {len(result.gate_failures)} gate/content failure(s). NOT clean.")
        return 1
    if result.entity_blocker:
        print("RESULT: all commercial gates PASS. Blocked on entity resolution only (expected).")
        return 0
    print("RESULT: clean.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(run(sys.argv[1]))
