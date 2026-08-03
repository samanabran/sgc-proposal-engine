# Escalation Triggers

Exactly when an SDR must stop and escalate rather than proceed. If none of
these apply, proceed per the normal runbook sequence
(`runbook/subscription-proposal-runbook.md`). If any of these apply,
**stop, log the escalation in the client's `manifest.yaml: escalations`,
and route to the Commercial Desk** — see `approval-matrix.md` for who
signs off at what level. Never resolve any of the following by
improvising, discounting, or paraphrasing around it (`AGENTS.md: On
uncertainty`).

## 1. Any G1–G10 gate failure

Every gate failure is an escalation, no exceptions. One line each
(`commercial-rules/subscription-guardrails.md`):

| Gate | Fails when | Matching known defect |
|---|---|---|
| **G1** — Platform floor | Build value + cost-to-serve doesn't clear `cts_total_aed × 1.25` | `known-defects.md #3` |
| **G2** — Term ≥ recovery | Mobilisation + recovery isn't fully recovered within the subscription term | `known-defects.md #9` |
| **G3** — Rate provenance | Any rate, hour figure, or percentage doesn't trace to a `pricing/*.yaml` key | `known-defects.md #15` |
| **G4** — Documentation coverage | `documentation_hours` below `max(overlays.documentation_hours_min, 5% of dev hours)` | `known-defects.md #7` |
| **G5** — QA coverage | `qa_hours` below `max(overlays.qa_hours_min, 8% of delivery hours)` | `known-defects.md #8` |
| **G6** — PM coverage | PM line doesn't equal the segment's `pm_pct` × subtotal | — (Commercial Rule 6; no dedicated defect entry, still a hard stop) |
| **G7** — Segment rate integrity | `blended_rate_aed` used doesn't match the segment implied by the client's user count | `known-defects.md #12` |
| **G8** — Gross margin floor | Margin falls below 30% (target 35%) | `known-defects.md #3` |
| **G9** — Market test | `year1_client_cost_aed` exceeds 1.30× the incumbent benchmark | `known-defects.md #11` |
| **G10** — Budget test | Quote meets or exceeds a previously rejected budget without a logged value justification | `known-defects.md #10` |

On resolution: reduce scope (fewer modules, fewer users, a lower support
tier, a longer term), never discount below the floor or shorten the
recovery assumption to force a pass — see `subscription-guardrails.md: On
a failed gate` for the per-gate remediation pattern.

## 2. A rate or module not on the card

If a client asks for an Odoo module, a role, or a rate that has no key in
`pricing/*.yaml` (`saas-modules.yaml`, `rate-card.yaml`, `hour-lookup.yaml`,
`hosting.yaml`, `support-training.yaml`), that is an escalation, not an
estimate-by-analogy. **Escalate; do not interpolate** —
`rate-card.yaml: notes`, `saas-modules.yaml: notes`,
`hour-lookup.yaml: notes` all say this independently. See
`known-defects.md #15` for what happens when a drafter prices "close to
similar modules" instead.

## 3. A client budget below the platform floor

If the client's stated budget, before any worksheet is even built, is
below what `platform_floor_aed` (`cts_total_aed × 1.25`,
`policy.yaml: gates.platform_floor_multiplier`) would require for the
smallest realistic scope, don't build a worksheet designed to force a fit.
Escalate the budget mismatch and have the Commercial Desk confirm whether
scope can be cut far enough to make the segment viable, or whether the
deal should be declined.

## 4. A legal or VAT clause needing paraphrase

Tax and legal wording is copied verbatim from `clause-library/` — never
paraphrased (`AGENTS.md`). If a client's situation genuinely doesn't fit
any existing clause (e.g. `vat-uae.md`, `clawback.md`,
`financing-disclosure.md`, `exclusivity-replacement.md`,
`term-commencement.md`) and the language would need to change to cover
it, that is an escalation for legal + Commercial Desk review before the
clause goes anywhere near a draft. See `known-defects.md #6` for the VAT
Designated Zone example of why this matters — a well-intentioned rewrite
dropped a qualifying condition and implied a VAT exemption that wasn't
true.

## 5. An issued-revision correction

`05-issued/` is immutable once a revision has been sent (`AGENTS.md`). If
an error is found in an issued proposal — pricing, a clause, a number —
that is always an escalation: a new revision (`_RevN+1`) or a
`correction-notice.md` (`01-templates/comms/`), never a silent edit to the
issued folder. See `known-defects.md #5`. Route through
`approval-matrix.md`'s L1/L2 sign-off for issued corrections depending on
whether pricing is affected.

## What "escalate" means in practice

1. Stop drafting. Do not proceed past the point of the trigger.
2. Log one line in the client's `manifest.yaml: escalations` — what
   triggered it, which gate/rule, and the resolution once one exists.
3. Route to the Commercial Desk (or the level specified in
   `approval-matrix.md`).
4. Resume only once the escalation is resolved and, for gate failures, the
   worksheet has been re-run and re-passed — not patched around.
