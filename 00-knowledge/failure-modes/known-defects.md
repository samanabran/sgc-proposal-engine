# Known Defects

Fifteen concrete failure modes this repository's structure exists to
prevent, with the arithmetic attached. This is the highest-value onboarding
asset in the repo — read it before running your first deal
(`05-ops/onboarding-new-sdr.md`). Each defect names the mechanism that now
catches it.

## 1. Segment rate drift between `policy.yaml` and `rate-card.yaml`

**What happened while building this repo, not a hypothetical**: the
original design draft for `pricing/policy.yaml` pinned `smb.blended_rate_aed`
to 425 and `mid_market.blended_rate_aed` to 550 — the *pre-revision*
Consultant and Senior Consultant rates. `rate-card.yaml` v2 (22 Jul 2026)
revised those roles to 395 and 525. Left unreconciled, every `smb` proposal
would have overquoted by AED 30/hr and every `mid_market` proposal by
AED 25/hr against the actual card — a client checking the numbers against a
later-issued sibling proposal would find two different rates for the same
role.

**Caught by**: building `policy.yaml` and `rate-card.yaml` in the same
commit and cross-checking every pinned rate against its source role before
first commit (see the comment block at the top of `policy.yaml`).

**Mechanism that prevents recurrence**: `policy.yaml`'s segment block
documents which `rate-card.yaml` role each `blended_rate_aed` is pinned to.
A rate-card change that doesn't touch `policy.yaml` in the same commit is a
review-log flag (`04-governance/review-log.md`).

## 2. SDR copies a peer's client folder instead of `_SCAFFOLD`

A live deal folder can contain a one-off concession — a discounted rate, a
waived setup fee, a non-standard payment term. Copying it as the starting
point for a new client silently propagates that concession as if it were
policy. Six months and a dozen copies later, three different "standard"
rates exist and nobody can say which is real.

**Mechanism**: `runbook/subscription-proposal-runbook.md` §1 mandates
copying `_SCAFFOLD`, which is empty of numbers by design.

## 3. Discounting past the margin floor to win a deal

A client pushes back on a AED 55,000 build quote. An SDR under pressure
drops the rate until the deal "feels winnable" — say, cutting the effective
blended rate until gross margin lands at 22%, below the 30% floor
(`policy.yaml: gates.min_gross_margin`).

**Mechanism**: G8 in `subscription-guardrails.md` fails mechanically at
30%. The runbook and `AGENTS.md` both state the fix explicitly: reduce
scope, never price under the floor.

## 4. Verbal promise never logged

On a discovery call, the SDR tells the client "we'll throw in the extra
training session." Three months later, at issue, the client expects it and
it isn't in the worksheet or the draft. The client reasonably feels misled;
SGC either eats the cost or damages the relationship.

**Mechanism**: `00-intake/verbal-promises.md` plus `AGENTS.md`: "anything
said aloud is scope," logged the same day. QA checklist checks
`verbal_promises_logged: true` before issue.

## 5. Editing a sent revision instead of issuing a new one

A typo is found in an issued proposal's pricing table. The fastest fix is
to open `05-issued/CLIENT-2026-SUB-01_Rev1/` and correct it in place — but
the client already has a PDF of the original, and now the repo and the
client's copy disagree with no record of the change.

**Mechanism**: `05-issued/` is immutable by contract (`AGENTS.md`). A
correction is `Rev2`, or a `correction-notice.md` if the wrong version was
already sent.

## 6. VAT clause paraphrased instead of copied verbatim

A drafter rewrites the standard VAT clause in their own words to "make it
flow better" with the rest of §10. The rewrite drops the Designated Zone
qualifying-condition language from `clause-library/vat-uae.md`, and the
proposal now implies blanket free-zone VAT exemption — which
`market-data/vertical-notes/uae-tax-vat.md` explicitly flags as false for
most clients (`policy.yaml: vat.free_zone_exempt: false`).

**Mechanism**: `AGENTS.md` — tax and legal wording copied verbatim from
`clause-library/`, always flagged for human review.

## 7. Undocumented custom feature

A bespoke report is scoped into `number_2_build` with dev hours only — no
`documentation_hours` line, because "it's a small report." Six months later
a new consultant inherits the account and has no record of what the report
does or why.

**Mechanism**: G4 (`subscription-guardrails.md`) requires documentation
hours ≥ `max(overlays.documentation_hours_min, 5% of dev hours)` on every
worksheet, mechanically, regardless of perceived size.

## 8. QA hours zeroed to hit a tight budget

Facing budget pressure, a worksheet sets `qa_hours: 0` to shave the
subtotal, planning to "test as we go" instead.

**Mechanism**: G5 requires `qa_hours ≥ max(overlays.qa_hours_min, 8% of
delivery hours)`. This is Commercial Rule 5 — QA is never waived — made
mechanical rather than a matter of discipline.

## 9. Mobilisation term shorter than build recovery

A client wants a 6-month subscription term with zero mobilisation. Applied
naively, SGC would still be recovering build cost through month 9 while the
contract ends at month 6 — a guaranteed loss on the deal regardless of the
monthly rate.

**Mechanism**: G2 (`Term ≥ recovery`) checks `mobilisation_aed +
recovery_total_aed` against `term_months` before the worksheet can pass.

## 10. Quoting near a budget the client already rejected

A client rejected a AED 85,000 quote from a competitor three months ago.
Unaware of this, a fresh worksheet — built independently, correctly, on
current rates — lands at AED 92,000. Quoting it without acknowledging the
history reads as tone-deaf and re-triggers the same objection.

**Mechanism**: G10 (budget test) checks `year1_client_cost_aed` against
`budget_rejected_aed` from the client brief and forces an explicit value
justification before requoting near a known-rejected number.

## 11. Pricing above the market-position ceiling

A heavily customized build stacks enough complexity multipliers that the
quoted price reaches 1.6× the client's stated incumbent cost — well past
SGC's "15–20% under mid-tier" positioning
(`market-data/benchmarks.yaml: strategic_position`) and into Big-4
territory the specialist-boutique band is built to avoid.

**Mechanism**: G9 (market test) caps at `policy.yaml:
gates.max_multiple_of_incumbent` (1.30×). A failure here is a signal to
check for double-counted overlays before cutting scope.

## 12. Startup-segment deal priced at the wrong rate

A 8-user client clearly qualifies for `startup_boutique`
(`policy.yaml: segments.startup_boutique.max_users: 10`) but the worksheet
uses the `smb` blended rate (395 instead of 280) and 15% PM instead of 10%,
because the drafter defaulted to the "normal" segment out of habit.

**Mechanism**: G7 (segment rate integrity) checks the blended rate used
against the segment implied by the client's user count.

## 13. Training billed as a recurring line

A drafter adds the two bundled training sessions
(`policy.yaml: overlays.training_sessions`) to the *recurring* subscription
line instead of billing them once in the build, stacking an ongoing
training overhead the client never agreed to.

**Mechanism**: Commercial Rule 8 — training billed once, no overhead
percentage stacked on top — checked at QA checklist stage against the
`number_2_build` vs. `assembly` split.

## 14. Knowledge version not pinned

A proposal is built, gates pass, and drafting begins — but
`manifest.yaml: knowledge_version_used` is left blank. Two weeks later
`pricing/policy.yaml` bumps to v1.1 with a rate change. Nobody can now tell
whether the in-flight proposal was built on v1.0 or should be re-priced
against v1.1.

**Mechanism**: `AGENTS.md` — always pin `knowledge_version_used` before
drafting. `CHANGELOG.md` version bumps never silently revalue an
in-progress worksheet because the worksheet records which version it was
built against.

## 15. Escalation resolved by improvising instead of asking

A client asks for an Odoo module that isn't in `saas-modules.yaml`. Rather
than escalate, the drafter estimates a price "close to similar modules" and
adds it to the worksheet, breaking Rule 3 (auditability) — the number now
has no source key to trace to.

**Mechanism**: `AGENTS.md` absolute rule — a rate not on the card is an
escalation (`manifest.yaml: escalations`), never an improvisation. This is
the rule from which every other gate in this file ultimately derives: if
every number traces to a file, defects 1–14 above become mechanically
detectable instead of relying on someone noticing.
