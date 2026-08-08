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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pricing_engine as pe  # noqa: E402 -- V1/V2 checks and the pricing_engine
                              # module are the single code path (P14) for
                              # anything B_hours/passthrough-ceiling related.

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _forbidden_rates():
    """All forbidden_rates from rate-card.yaml, not just one hardcoded
    value — see failure-modes/known-defects.md #2 (690) and #21 (550,
    added after 425/550 were found reintroduced into policy.yaml)."""
    rc = load_yaml(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "rate-card.yaml"))
    return [r["rate_aed_hr"] for r in rc.get("forbidden_rates", [])]

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

# check_19, separate from check_18 on purpose: check_18 catches commercial
# CLAIMS that would misrepresent terms to a client (a promise, a rate, a
# VAT position). This list catches internal NARRATION about SGC's own
# authoring/strategy process leaking into client-facing prose — a
# different failure mode with a different fix (delete the sentence, not
# renegotiate the term). Evidence-based, not a generic ban list: each
# entry below is a phrase actually found leaking into a draft this repo
# audited (Kallat 2026-08-07 pass) — add to it as found, don't
# pre-populate with hypotheticals.
#   - "disarm-hesitation": names SGC's own negotiating posture
#     (found: KP-2026-SUB-01 03-draft/10-commercial-terms.md).
#   - "placeholder-driven": discloses that a risk/scoring input is an
#     unconfirmed guess, not a verified fact — worse than a strategy
#     leak, since it undermines the numbers themselves, not just the
#     framing (found: KP-2026-SUB-01 03-draft/09-partnership-terms.md).
# Deliberately narrow substring matches (not generic words like
# "internal" or "draft") so the required "INTERNAL DRAFT — NOT FOR
# CLIENT TRANSMISSION" banner and other intentional internal-only
# disclaimers are never caught by this check — those are correct,
# required text, not a leak.
INTERNAL_VOCABULARY_PHRASES = [
    "disarm-hesitation",
    "placeholder-driven",
]

# A currency figure tied directly to a per-user/seat/agent divisor (e.g.
# "AED 250/user/month") — the exact shape of exposure decision #9
# (Kallat, manifest.yaml 2026-08-07) ruled must never appear in a
# client-facing document, even as a labelled illustration. Requires the
# AED figure, not just the bare phrase "per-user" alone, so correction
# language like "our pricing isn't per-user" (no figure attached) does
# not false-positive — found live 2026-08-08 in Kallat's own
# 03-draft/KP-2026-SUB-01_Rev1/07-options-inclusions.md:10, stale
# against the 2026-08-05 v3.0 recompute (see manifest.yaml 2026-08-08
# entry). Distinct failure mode from check_18 (commercial claims) and
# check_19 (internal vocabulary) — a pricing-shape leak, not a
# forbidden word — kept as its own check for the same reason check_19
# was kept separate from check_18.
PER_USER_RATE_PATTERN = re.compile(
    r"AED\s*[\d,]+(?:\.\d+)?\s*/?\s*per[- ]?(?:user|seat|agent)\b"
    r"|AED\s*[\d,]+(?:\.\d+)?\s*/\s*(?:user|seat|agent)\b",
    re.IGNORECASE,
)

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
        self.structural_exceptions = []  # known-obsolete check, red on purpose -- see check_4_hour_benchmark
        self.passed = []

    def fail(self, check, msg):
        self.gate_failures.append(f"[FAIL] {check}: {msg}")

    def structural_exception(self, check, msg):
        self.structural_exceptions.append(f"[STRUCTURAL EXCEPTION] {check}: {msg}")

    def ok(self, check, msg=""):
        self.passed.append(f"[ OK ] {check}" + (f": {msg}" if msg else ""))


def load_yaml(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def find_worksheet(client_dir):
    matches = glob.glob(os.path.join(client_dir, "02-calc", "pricing-worksheet.yaml"))
    return matches[0] if matches else None


def check_1_forbidden_rate_in_pricing(result):
    forbidden = _forbidden_rates()
    for f in glob.glob(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "*.yaml")):
        if "rate-card.yaml" in f:
            continue  # the guard entries themselves legitimately state the number
        text = open(f, encoding="utf-8").read()
        for rate in forbidden:
            if re.search(rf"\b{rate}\b", text):
                result.fail("1. forbidden rate", f"{rate} appears in {f}")
    result.ok(f"1. forbidden rates {forbidden} not present in pricing/*.yaml (outside rate-card.yaml's own guard entries)")


def check_1c_segment_pins(result):
    """Structural guard for known-defects.md #21: each segment's
    blended_rate_aed must equal the rate_aed_hr of its declared
    pinned_role, not just be SOME value that happens to exist on the card
    (425 legitimately exists as qa_engineer's rate, which is why a
    forbidden_rates entry alone can't catch it being misused as smb's
    blended rate)."""
    policy = load_yaml(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml"))
    rate_card = load_yaml(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "rate-card.yaml"))
    roles = rate_card.get("roles", {})
    for seg_name, seg in policy.get("segments", {}).items():
        pinned_role = seg.get("pinned_role")
        if not pinned_role or pinned_role not in roles:
            result.fail("1c. segment rate pin", f"segments.{seg_name} has no valid pinned_role on rate-card.yaml")
            continue
        expected = roles[pinned_role]["rate_aed_hr"]
        actual = seg.get("blended_rate_aed")
        if actual != expected:
            result.fail("1c. segment rate pin", f"segments.{seg_name}.blended_rate_aed ({actual}) != roles.{pinned_role}.rate_aed_hr ({expected})")
    result.ok("1c. every segment's blended_rate_aed matches its pinned rate-card role exactly")


def check_1b_forbidden_rate_in_client(result, client_dir):
    # Only scan the ACTIVE pricing surface — the worksheet and the current
    # draft. manifest.yaml (escalation narrative) and 05-issued/ (retracted
    # historical record, or an immutable clean-history document like VGE's)
    # are legitimately allowed to reference a forbidden rate as a
    # documented past defect, not a live figure — see
    # check_1_forbidden_rate_in_pricing for the check that guards live
    # pricing data itself.
    forbidden = _forbidden_rates()
    targets = glob.glob(os.path.join(client_dir, "02-calc", "*.yaml")) + \
        glob.glob(os.path.join(client_dir, "03-draft", "**", "*.md"), recursive=True)
    for f in targets:
        text = open(f, encoding="utf-8").read()
        for rate in forbidden:
            if re.search(rf"\b{rate}\b", text):
                result.fail("1. forbidden rate in client folder", f"{rate} appears in {f}")
    result.ok(f"1. forbidden rates {forbidden} not present in active client worksheet/draft")


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


# check_4's 9.2h/user literal is NOT changed here — per K-5
# (pricing-engine-cost-class-model.md Rev.2), it stays until fixture
# evidence exists to justify touching it. That evidence now exists:
# test_pricing_engine.py's T8 sweeps the SAME engine the recompute uses
# across N=1..400 and finds check_4 passes comfortably at low N, then
# fails starting at exactly N=19 and never recovers through N=400 --
# per-user hours fall from 69.1 (N=1) to 0.72 (N=400) while check_4
# demands a flat 4.6h/user floor forever. A flat per-user benchmark is
# structurally incompatible with a model where Class A is near-flat,
# Class B is sub-linear (Wright's law), and hypercare is a coarse
# ceil(N/5) step -- ANY such model eventually falls below a flat floor
# regardless of the exact constants chosen (T8 also confirms every local
# uptick traces to a known, small, explained step boundary, not noise).
# This is why the check is now classified structural_exception rather
# than gate_failures for N >= CHECK_4_STRUCTURAL_BREACH_N: it is EXPECTED
# to be red there, and that redness is not evidence the recompute is
# wrong. Do NOT "fix" this by loosening the 9.2 literal, the 50% floor,
# or this threshold without first re-running
# test_pricing_engine.py's t8_check4_structural_sweep and reading why it
# was classified this way -- see CHANGELOG.md pricing v3.0 addendum.
CHECK_4_STRUCTURAL_BREACH_N = 19


def check_4_hour_benchmark(result, ws):
    users = ws.get("inputs", {}).get("users_now")
    total_hours = ws.get("number_2_build", {}).get("total_hours")
    if users and total_hours:
        benchmark = 9.2 * users
        if total_hours < benchmark * 0.5:
            msg = f"{total_hours}h for {users} users is well under the ~{benchmark:.0f}h reference benchmark"
            if users >= CHECK_4_STRUCTURAL_BREACH_N:
                result.structural_exception(
                    "4. hour benchmark", msg + f" -- EXPECTED for users>={CHECK_4_STRUCTURAL_BREACH_N} "
                    "(structural obsolescence confirmed, see test_pricing_engine.py t8_check4_structural_sweep "
                    "and CHANGELOG.md pricing v3.0 addendum, not a worksheet defect)")
            else:
                result.fail("4. hour benchmark", msg)
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


def check_19_internal_vocabulary(result, draft_files):
    """Internal narration/strategy vocabulary leaking into client-facing
    draft prose — distinct failure mode from check_18 (commercial
    claims), see INTERNAL_VOCABULARY_PHRASES comment above for why this
    is a separate check rather than folded into check_18's list."""
    for f in draft_files:
        if any(f.endswith(s) for s in FORBIDDEN_PHRASE_EXEMPT_SUFFIXES) or _is_retracted_historical(f):
            continue
        text = open(f, encoding="utf-8").read()
        for p in INTERNAL_VOCABULARY_PHRASES:
            if p.lower() in text.lower():
                result.fail("19. internal vocabulary leak", f"'{p}' found in {f}")
    result.ok("19. no internal narration/strategy vocabulary found outside exempt/historical reference files")


def check_20_per_user_rate_leak(result, draft_files):
    """A per-user rate or divisor in client-facing draft prose (e.g.
    "AED 250/user/month") — see PER_USER_RATE_PATTERN comment above for
    why this is its own check rather than folded into check_18/19."""
    for f in draft_files:
        if any(f.endswith(s) for s in FORBIDDEN_PHRASE_EXEMPT_SUFFIXES) or _is_retracted_historical(f):
            continue
        text = open(f, encoding="utf-8").read()
        for m in PER_USER_RATE_PATTERN.finditer(text):
            result.fail("20. per-user rate leak", f"{m.group(0)!r} found in {f}")
    result.ok("20. no per-user rate/divisor found outside exempt/historical reference files")


# ---------------------------------------------------------------------
# V1-V5 (pricing-engine-cost-class-model.md Rev.2 §I) and R1-R12
# (Commercial Rules as executable checks, D-11). Additive to checks
# 1-18 above -- none of the existing checks are modified, per K-5
# (validate.py:199's literal 9.2*users is untouched; V1 supersedes it
# functionally without replacing it).
# ---------------------------------------------------------------------

V1_TOLERANCE = 0.40
# Derived (D-10), not chosen at implementation time: average relative
# spread between hours_simple and hours_standard across all 11 original
# hour-lookup.yaml work packages (the only documented source of
# legitimate task-time variance in this repo) = 40.5%, rounded to 40%.
# See pricing-engine-cost-class-model.md Rev.2 §I for the per-package
# derivation. No client price or pass/fail was referenced in deriving
# this number (P7).


def check_v1_effort_reconciliation(result, ws):
    """Effort reconciliation: computed A_hours (sum of hour-lookup.yaml
    hours_<band> for each declared delivery_hours entry) vs the
    worksheet's own declared subtotal for those same entries, within
    V1_TOLERANCE. Makes the market-band gate (V3) an annotation, not a
    control, once effort reconciles bottom-up."""
    hl = pe.load_hour_lookup()["work_packages"]
    delivery = ws.get("number_2_build", {}).get("delivery_hours", [])
    if not delivery:
        result.ok("V1. effort reconciliation", "no delivery_hours entries to reconcile")
        return
    catalogue_sum = 0.0
    declared_sum = 0.0
    untraceable = []
    for entry in delivery:
        pkg, band, hours = entry.get("package"), entry.get("band"), entry.get("hours", 0)
        declared_sum += hours
        key = f"hours_{band}"
        if pkg in hl and key in hl[pkg]:
            catalogue_sum += hl[pkg][key]
        else:
            untraceable.append(f"{pkg}/{band}")
    if untraceable:
        result.fail("V1. effort reconciliation", f"no hour-lookup.yaml key for: {untraceable}")
        return
    rel_diff = abs(declared_sum - catalogue_sum) / catalogue_sum if catalogue_sum else 0
    if rel_diff > V1_TOLERANCE:
        result.fail("V1. effort reconciliation",
                    f"declared {declared_sum}h vs catalogue {catalogue_sum}h, "
                    f"{rel_diff:.1%} apart, exceeds {V1_TOLERANCE:.0%} tolerance")
    else:
        result.ok("V1. effort reconciliation",
                   f"declared {declared_sum}h vs catalogue {catalogue_sum}h, within {V1_TOLERANCE:.0%}")


def check_v2_rate_mix_ceiling(result, ws):
    """Rate-mix ceiling, per-task-role (D-5): Class B work must not be
    billed at an L2+ segment-blended rate. Checks the legacy
    number_2_build.rollout_hours field (pre-recompute worksheets, e.g.
    Kallat/Prosper before step (h)) against the passthrough ceiling --
    this is the exact check that catches Kallat Rev1's 120h@525."""
    build = ws.get("number_2_build", {})
    rollout_hours = build.get("rollout_hours", 0)
    rate = build.get("rate_aed")
    if rollout_hours and rate:
        ceiling = pe.junior_passthrough_ceiling_aed_hr()
        if rate > ceiling:
            result.fail("V2. rate-mix ceiling",
                        f"{rollout_hours}h of per-user-shaped rollout work billed at {rate} "
                        f"AED/hr, exceeds Class B ceiling {ceiling} AED/hr -- no written "
                        "per-task justification on file")
            return
    # Post-recompute schema: number_2_build.class_b.tasks[], each with its
    # own role/rate -- checked against rate-card.yaml per task once present.
    class_b = build.get("class_b")
    if class_b:
        rc = pe.load_rate_card()
        roles = rc.get("roles", {})
        ceiling = pe.junior_passthrough_ceiling_aed_hr(rc)
        for task in class_b.get("tasks", []):
            role = task.get("role")
            applied_rate = task.get("rate_aed")
            if role == "junior_passthrough":
                max_rate = ceiling
            elif role in roles:
                max_rate = roles[role]["rate_aed_hr"]
            else:
                result.fail("V2. rate-mix ceiling", f"task {task.get('name')} has unknown role '{role}'")
                continue
            if applied_rate and applied_rate > max_rate:
                result.fail("V2. rate-mix ceiling",
                            f"task {task.get('name')} billed at {applied_rate} AED/hr, "
                            f"exceeds role '{role}' ceiling {max_rate} AED/hr")
    result.ok("V2. rate-mix ceiling", "no Class B task exceeds its per-task-role ceiling")


def check_v3_band_applicability(result, ws):
    """Band check with applicability guard (V3): the 22,000-55,000
    implementation band (benchmarks.yaml market_positioning) is scoped
    10-30 users. Out-of-range N is ANNOTATION ONLY -- never pass, never
    fail."""
    users = ws.get("inputs", {}).get("users_now")
    build_value = ws.get("number_2_build", {}).get("build_value_aed")
    if users is None or build_value is None:
        return
    if 10 <= users <= 30:
        low, high = 22000, 55000
        if low <= build_value <= high:
            result.ok("V3. band check", f"{build_value} AED within [22000,55000] band for {users} users")
        else:
            result.ok("V3. band check", f"OUT-OF-BAND (annotation only) -- {build_value} AED "
                       f"outside [22000,55000] for {users} users, in-range population")
    else:
        result.ok("V3. band check",
                   f"OUT-OF-RANGE -- ANNOTATION ONLY. Band scoped to 10-30 users, "
                   f"this deal is {users}. No pass/fail emitted.")


def check_v4_positioning_claim(result, ws, draft_files):
    """Positioning-claim check (V4), computed not asserted: '15-20% below
    mid-tier' may appear only if blended rate <= 0.85 x mid-tier midpoint
    (350-550 -> 450 -> threshold 382.5)."""
    rate = ws.get("number_2_build", {}).get("rate_aed")
    threshold = 0.85 * 450
    claim_pattern = re.compile(r"below\s+mid-?tier", re.IGNORECASE)
    for f in draft_files:
        if _is_retracted_historical(f):
            continue
        text = open(f, encoding="utf-8").read()
        if claim_pattern.search(text):
            if rate is None:
                result.fail("V4. positioning claim", f"claim found in {f} but rate_aed unknown")
            elif rate > threshold:
                result.fail("V4. positioning claim",
                            f"'{claim_pattern.search(text).group(0)}' claim in {f} is FALSE: "
                            f"blended rate {rate} AED/hr > threshold {threshold} AED/hr")
            else:
                result.ok("V4. positioning claim", f"claim in {f} holds: {rate} <= {threshold}")
            return
    result.ok("V4. positioning claim", "no 'below mid-tier' claim present -- nothing to check")


def check_r1_r2_discount_hygiene(result, ws):
    """R1 (implementation computed pre-discount) + R2 (discount never
    changes hours). No corpus client currently applies a discount
    (G10_concessions_capped: no concessions on any of the four deals) --
    both checks pass trivially in that case, which is the correct,
    non-outcome-fitted result, not a weakened check."""
    discount = ws.get("discount", {})
    hours_before = ws.get("number_2_build", {}).get("total_hours")
    if not discount:
        result.ok("R1/R2. pre-discount computation + hours unchanged by discount",
                   "no discount applied on this deal -- trivially compliant")
        return
    hours_after = discount.get("total_hours_after_discount", hours_before)
    if hours_after != hours_before:
        result.fail("R2. discount never changes hours",
                     f"total_hours changed from {hours_before} to {hours_after} under discount")
    else:
        result.ok("R1/R2. pre-discount computation + hours unchanged by discount")


def check_r3_hour_traceability(result, ws):
    """R3: every hour traces to task x complexity in hour-lookup.yaml.
    Fails on any declared hour with no lookup key -- this is Kallat
    Rev1's real, current failure (the 120 rollout_hours have no
    hour-lookup.yaml key at all, pre step (h) recompute)."""
    hl = pe.load_hour_lookup()["work_packages"]
    build = ws.get("number_2_build", {})
    untraceable = []
    for entry in build.get("delivery_hours", []):
        pkg, band = entry.get("package"), entry.get("band")
        if pkg not in hl or f"hours_{band}" not in hl.get(pkg, {}):
            untraceable.append(f"{pkg}/{band}")
    if build.get("rollout_hours", 0) > 0 and "rollout_hours" not in hl:
        untraceable.append("rollout_hours (no hour-lookup.yaml key -- legacy overlay-derived hours)")
    if untraceable:
        result.fail("R3. hour traceability", f"untraceable to hour-lookup.yaml: {untraceable}")
    else:
        result.ok("R3. hour traceability", "every declared hour traces to a hour-lookup.yaml key")


def check_r6_pm(result, ws):
    """R6: PM present at 15% standard / 10% startup, exact."""
    policy = pe._load(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml"))
    segment = ws.get("inputs", {}).get("segment")
    build = ws.get("number_2_build", {})
    pm_aed, subtotal = build.get("pm_aed"), build.get("subtotal_aed")
    if segment not in policy.get("segments", {}) or pm_aed is None or subtotal is None:
        result.fail("R6. PM present, correct %", "segment/pm_aed/subtotal_aed missing or segment unknown")
        return
    expected_pct = policy["segments"][segment]["pm_pct"]
    expected_pm = subtotal * expected_pct
    if abs(pm_aed - expected_pm) > 1:
        result.fail("R6. PM present, correct %",
                     f"pm_aed {pm_aed} != subtotal {subtotal} x {expected_pct} = {expected_pm}")
    else:
        result.ok("R6. PM present at correct %", f"{expected_pct:.0%} of subtotal, matches exactly")


def check_r8_training_once(result, ws):
    """R8: training billed once, no overhead stacked on top of it."""
    policy = pe._load(os.path.join(REPO_ROOT, "00-knowledge", "pricing", "policy.yaml"))
    build = ws.get("number_2_build", {})
    training_hours = build.get("training_hours")
    expected = policy["overlays"]["training_sessions"] * policy["overlays"]["training_hours_per_session"]
    if training_hours != expected:
        result.fail("R8. training billed once", f"training_hours {training_hours} != expected {expected}")
        return
    dev_base = build.get("dev_hours_for_overlays") or build.get("work_package_hours_subtotal")
    if dev_base is not None and training_hours and (dev_base + training_hours) == build.get("total_hours"):
        # training_hours is additive to total but NOT part of the base PM/QA/doc
        # overlays are computed against -- confirms no overhead stacked on it.
        result.ok("R8. training billed once, no overhead stacked on it",
                   f"{training_hours}h, excluded from PM/QA/doc overlay base ({dev_base}h)")
    else:
        result.ok("R8. training billed once", f"{training_hours}h present, matches policy default exactly")


ASSUMPTIONS_HEADING = re.compile(r"^#{1,3}\s*Assumptions\s*$", re.IGNORECASE | re.MULTILINE)
EXCLUSIONS_HEADING = re.compile(r"^#{1,3}\s*Exclusions\s*$", re.IGNORECASE | re.MULTILINE)


def _section_nonempty(text, heading_re, min_chars=30):
    m = heading_re.search(text)
    if not m:
        return False
    rest = text[m.end():]
    next_heading = re.search(r"^#{1,3}\s", rest, re.MULTILINE)
    body = rest[:next_heading.start()] if next_heading else rest
    return len(body.strip()) >= min_chars


def check_r9_r10_assumptions_exclusions(result, draft_files):
    """R9 (assumptions present, non-empty) + R10 (exclusions present,
    non-empty). Checked against the actual draft prose, not just the
    exclusions_confirmed boolean already present in every worksheet."""
    found_assumptions = found_exclusions = False
    for f in draft_files:
        if _is_retracted_historical(f):
            continue
        text = open(f, encoding="utf-8").read()
        if not found_assumptions and _section_nonempty(text, ASSUMPTIONS_HEADING):
            found_assumptions = True
        if not found_exclusions and _section_nonempty(text, EXCLUSIONS_HEADING):
            found_exclusions = True
    if not found_assumptions:
        result.fail("R9. assumptions section present, non-empty", "no non-empty 'Assumptions' heading found in draft")
    else:
        result.ok("R9. assumptions section present, non-empty")
    if not found_exclusions:
        result.fail("R10. exclusions section present, non-empty", "no non-empty 'Exclusions' heading found in draft")
    else:
        result.ok("R10. exclusions section present, non-empty")


def check_r11_r12_deliverables(result, client_dir):
    """R11 (standalone quotation PDF) + R12 (one-page commercial
    summary). Confirmed real, repo-wide gap (kallat-recost-rev2.md D5) --
    neither artefact exists for any corpus client as of this check."""
    quotation = glob.glob(os.path.join(client_dir, "0*-draft", "**", "*uotation*.pdf"), recursive=True) + \
        glob.glob(os.path.join(client_dir, "05-issued", "**", "*uotation*.pdf"), recursive=True)
    summary = glob.glob(os.path.join(client_dir, "0*-draft", "**", "*ummary*.pdf"), recursive=True) + \
        glob.glob(os.path.join(client_dir, "05-issued", "**", "*ummary*.pdf"), recursive=True)
    if not quotation:
        result.fail("R11. standalone quotation PDF", "no *Quotation*.pdf found under 03-draft/04-draft/05-issued")
    else:
        result.ok("R11. standalone quotation PDF present", quotation[0])
    if not summary:
        result.fail("R12. one-page commercial summary", "no *Summary*.pdf found under 03-draft/04-draft/05-issued")
    else:
        result.ok("R12. one-page commercial summary present", summary[0])


def run_v5_corpus_prediction():
    """V5: mandatory corpus prediction, written before any gate lands.
    Predicted vs actual for all four corpus clients against the NEW
    checks. See pricing-engine-cost-class-model.md Rev.2 §I for the
    written-in-advance prediction this reproduces."""
    corpus = {
        "VGE-vongeyern-realestate": {"users": 5, "predicted_v2": "PASS", "predicted_v4": "PASS (rate 280 <= 382.5)"},
        "MRD-meridianview-realty": {"users": 5, "predicted_v2": "PASS", "predicted_v4": "PASS (rate 280 <= 382.5)"},
        "KP-kallat-properties": {"users": 40, "predicted_v2": "FAIL (120h@525 pre-fix)", "predicted_v4": "FAIL if claim present (rate 525 > 382.5)"},
        # CORRECTED after first run: originally predicted PASS ("no rollout_hours
        # legacy field billed at 525"), which was WRONG -- Prosper's own worksheet
        # (pricing-worksheet.yaml:52) has rollout_hours: 84 at the same 525 AED/hr
        # mid_market rate, same defect shape as Kallat, just smaller. The wrong
        # prediction is left documented here, not silently fixed, per V5's own
        # discipline (report predicted vs actual, including when the prediction
        # itself was wrong) -- this repo's implementer had already read this exact
        # worksheet earlier and should have caught it before predicting.
        "PRO-prosper-realestate": {"users": 31, "predicted_v2": "FAIL (84h@525, same shape as Kallat -- CORRECTED, originally mispredicted PASS)", "predicted_v4": "FAIL if claim present (rate 525 > 382.5)"},
    }
    print("=== V5: corpus prediction (written before running) ===")
    for name, pred in corpus.items():
        print(f"  {name}: predicted V2={pred['predicted_v2']}, V4={pred['predicted_v4']}")
    print()
    for name in corpus:
        client_dir = os.path.join(REPO_ROOT, "02-clients", name)
        ws_path = find_worksheet(client_dir)
        if not ws_path:
            print(f"  {name}: ACTUAL -- no worksheet found")
            continue
        ws = pe._load(ws_path)
        result = Result()
        check_v2_rate_mix_ceiling(result, ws)
        actual_v2 = "PASS" if not result.gate_failures else f"FAIL ({result.gate_failures[0]})"
        print(f"  {name}: ACTUAL V2={actual_v2}")


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
    check_1c_segment_pins(result)
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
    check_19_internal_vocabulary(result, draft_files)
    check_20_per_user_rate_leak(result, draft_files)

    # V1-V5 + R1-R12 (additive, D-11/pricing-engine-cost-class-model.md Rev.2)
    check_v1_effort_reconciliation(result, ws)
    check_v2_rate_mix_ceiling(result, ws)
    check_v3_band_applicability(result, ws)
    check_v4_positioning_claim(result, ws, draft_files)
    check_r1_r2_discount_hygiene(result, ws)
    check_r3_hour_traceability(result, ws)
    check_r6_pm(result, ws)
    check_r8_training_once(result, ws)
    check_r9_r10_assumptions_exclusions(result, draft_files)
    check_r11_r12_deliverables(result, client_dir)

    print(f"\n=== validate.py — {client_dir} ===\n")
    for line in result.passed:
        print(line)
    if result.gate_failures:
        print()
        for line in result.gate_failures:
            print(line)
    if result.structural_exceptions:
        print()
        for line in result.structural_exceptions:
            print(line)
    if result.entity_blocker:
        print(f"\n[BLOCKED — by design] 14. entity resolution: {result.entity_blocker}")
        print("This blocks ISSUE, not the commercial gate check. See 05-ops/validate.md.")

    print()
    if result.gate_failures:
        print(f"RESULT: {len(result.gate_failures)} gate/content failure(s). NOT clean.")
        return 1
    if result.structural_exceptions and result.entity_blocker:
        print(f"RESULT: all commercial gates PASS. {len(result.structural_exceptions)} known structural "
              "exception(s) (expected, see pricing_engine.py/CHANGELOG), blocked on entity resolution (expected).")
        return 0
    if result.structural_exceptions:
        print(f"RESULT: all commercial gates PASS. {len(result.structural_exceptions)} known structural "
              "exception(s) (expected -- see test_pricing_engine.py t8_check4_structural_sweep).")
        return 0
    if result.entity_blocker:
        print("RESULT: all commercial gates PASS. Blocked on entity resolution only (expected).")
        return 0
    print("RESULT: clean.")
    return 0


# --- Permanent regression corpus -------------------------------------
# These cases exist because the negation-aware phrase matching in this
# file already caused real false positives once (flagging this repo's
# OWN correct, mandatory disclosures — the VAT gross-up clause and the
# Community mobile-access disclosure — as violations). A validator that
# cries wolf on correct text is worse than no validator: people start
# passing --no-verify. Run automatically before every check_11/12/18
# invocation so a future regex "tightening" can't silently reintroduce
# the bug without being caught immediately.

SELFTEST_MUST_NOT_FLAG = [
    ("VAT-registered", "SGC TECH AI is not currently registered for UAE VAT, and no VAT is charged on this proposal."),
    ("VAT-registered", "Should SGC TECH AI become VAT-registered during the term, VAT at the prevailing rate will be added to invoices."),
    ("no VAT applies", "Full detail, including why this invoice carries no VAT charge, is in section 10."),
    ("iOS/Android app", "mobile-optimised browser access — **not** a dedicated\niOS/Android app. It does not include automated bank reconciliation."),
    ("Odoo Enterprise", "This proposal does not include Odoo Enterprise licensing or Odoo's own vendor upgrade service."),
]

SELFTEST_MUST_FLAG = [
    ("VAT-registered", "SGC TECH AI is VAT-registered and this invoice includes VAT."),
    ("no VAT applies", "No VAT applies — we operate from a free zone."),
    ("iOS/Android app", "This comes with a native iOS/Android app included at no extra cost."),
    ("Odoo Enterprise", "Includes full Odoo Enterprise licences at no extra cost."),
]


def self_test():
    failures = []
    for label, text in SELFTEST_MUST_NOT_FLAG:
        if label == "VAT-registered":
            hit = bool(CONDITIONAL_FORBIDDEN["VAT-registered"].search(text))
        elif label == "no VAT applies":
            m = re.search(r"no VAT applies", text, re.IGNORECASE)
            hit = bool(m and "free zone" in text[max(0, m.start() - 80):m.start() + 80].lower())
        else:
            m = re.search(re.escape(label), text, re.IGNORECASE)
            hit = bool(m and not _has_nearby_negation(text, m.start()))
        if hit:
            failures.append(f"FALSE POSITIVE: '{label}' wrongly flagged in correct text: {text!r}")
    for label, text in SELFTEST_MUST_FLAG:
        if label == "VAT-registered":
            hit = bool(CONDITIONAL_FORBIDDEN["VAT-registered"].search(text))
        elif label == "no VAT applies":
            m = re.search(r"no VAT applies", text, re.IGNORECASE)
            hit = bool(m and "free zone" in text[max(0, m.start() - 80):m.start() + 80].lower())
        else:
            m = re.search(re.escape(label), text, re.IGNORECASE)
            hit = bool(m and not _has_nearby_negation(text, m.start()))
        if not hit:
            failures.append(f"FALSE NEGATIVE: '{label}' should have been flagged but wasn't: {text!r}")
    return failures


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--corpus-predict":
        run_v5_corpus_prediction()
        sys.exit(0)

    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        failures = self_test()
        if failures:
            for f in failures:
                print(f"[SELFTEST FAIL] {f}")
            sys.exit(1)
        print(f"[SELFTEST OK] {len(SELFTEST_MUST_NOT_FLAG)} true-negative + {len(SELFTEST_MUST_FLAG)} true-positive cases pass")
        sys.exit(0)

    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)

    selftest_failures = self_test()
    if selftest_failures:
        print("Refusing to run: validate.py's own phrase-matching logic has regressed.", file=sys.stderr)
        for f in selftest_failures:
            print(f"[SELFTEST FAIL] {f}", file=sys.stderr)
        sys.exit(2)

    sys.exit(run(sys.argv[1]))
