# Step Gate — the non-skippable sequence

This is `00-knowledge/runbook/subscription-proposal-runbook.md`'s existing
11-stage sequence, with the pre-drafting interview made explicit and the
previously-implicit sub-steps (deal card, payment-plan worksheet,
consistency map, `validate.py`) named as their own checkpoints. It does not
replace the runbook — it is the runbook, read through the lens of "what
gate must this specific artifact clear before the next one is allowed to
start."

**Gate count is 41 (G1–G41)** — see `00-knowledge/commercial-rules/*`,
`05-ops/glossary.md`, and `05-ops/validate.py`. (A `G45`-labeled tag exists
in this repo, but only as an unrelated clause-annotation scheme inside the
MSA/SLA contract HTML — not part of this gate system. Do not confuse the
two.)

## The sequence

```
intake → fact ledger confirmed → risk assessment → pricing worksheet →
payment-plan worksheet → exposure calculation → walk-away card →
gates G1–G41 → brand resolution → draft → consistency map → validate.py →
QA checklist → issue-ready
```

No step may be skipped, reordered, or run in parallel with another. At
each step, state which step you're on, what it produced, and what the next
step is. If a step fails, stop and report — do not draft around the
failure or proceed to a later step. If asked to skip a step, refuse and
name the specific guardrail that forbids it.

| # | Step | Produces | Guardrail if skipped |
|---|---|---|---|
| 1 | Intake | `00-intake/client-brief.yaml`, `00-intake/verbal-promises.md`, `00-intake/session-log.md` | `intake-interview.md` — no drafting without a confirmed fact ledger |
| 2 | Fact ledger confirmed | SDR sign-off on the printed ledger (`intake-interview.md` step 6) | `fabrication-rules.md` — this is the checkpoint where fabrication gets caught |
| 3 | Risk assessment | `02-calc/risk-assessment.yaml` | Runbook §2 — must run before any pricing conversation |
| 4 | Pricing worksheet | `02-calc/pricing-worksheet.yaml` | `AGENTS.md` — "ALWAYS complete pricing-worksheet.yaml in full before drafting any prose"; blocked outright if Tier 0 incomplete (`sufficiency-rules.yaml`) |
| 5 | Payment-plan worksheet | `02-calc/payment-plan-worksheet.yaml` | Runbook §3 assembly — cadence/mobilisation math depends on it |
| 6 | Exposure calculation | `exposure:` block inside the pricing worksheet (all three exposures — contractual, cash, economic) | `AGENTS.md` G21 — "ALWAYS compute all three exposures" |
| 7 | Walk-away card | `02-calc/deal-card.md` | `AGENTS.md` G22 — "ALWAYS produce the walk-away deal card... before any pricing conversation" |
| 8 | Gate check (G1–G41) | `02-calc/gate-report.md` | `AGENTS.md` — "If any gate fails, STOP and escalate — do not discount around it" |
| 9 | Brand/entity resolution | RESOLVE scan against `06-brand/entity/legal-identity.yaml` and this client's Tier 1 facts | `fabrication-rules.md` + `validate.py: check_14_entity` — resolve or carry forward as RESOLVE, never guess |
| 10 | Draft | `03-draft/{PROPOSAL-REF}_RevN/` (§01–§13 per `01-templates/proposal/_section-map.md`) | Runbook §6 — only once `gates_passed: true` |
| 11 | Consistency map | Reconciliation of every shared variable across proposal / MSA / Order Form | `08-contracts/msa-proposal-consistency-map.md`'s own rule: "a mismatch in any row is a drafting defect, not a rounding difference to wave through" |
| 12 | `validate.py` | Exit code + report from `python 05-ops/validate.py 02-clients/{client}/` | Must exit 0, or report exactly which of the 18 checks failed — gate failures and the entity blocker are reported separately, never conflated |
| 13 | QA checklist | `04-review/qa-checklist.md`, `04-review/brand-qa-checklist.md` | Runbook §7 — every verbal-promise item reflected, no forbidden phrase, brand tokens only from `06-brand/registry.yaml` |
| 14 | Issue-ready | Human sign-off recorded in the QA checklist, `manifest.yaml: stage` ready to move to `issued` | Cannot be reached while any Tier 1 field is still `RESOLVE` (`sufficiency-rules.yaml: tier_1`) or `validate.py` hasn't been run clean |

## Known placement inconsistency (flagged, not fixed here)

The live `08-contracts/msa-proposal-consistency-map.md` is a per-deal
(VGE-specific) reconciliation table stored at the top-level `08-contracts/`
rather than inside `02-clients/VGE-.../04-review/`, and `08-contracts/`
isn't yet in `AGENTS.md`'s access-model table. Step 11 above references the
file where it actually lives today. A future cleanup should either move
per-deal consistency maps under each client's own `04-review/` folder, or
formally document `08-contracts/` as the shared home for them — this task
doesn't resolve which, it just names the gap so it isn't silently assumed
away.
