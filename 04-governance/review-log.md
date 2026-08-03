# Review Log

Log of reviews performed against this repository's knowledge layer,
client artifacts, or process — governance-level oversight, not the
per-deal QA checklist (`04-review/qa-checklist.md` inside a client
folder covers that). Append a row per review; never edit a prior row's
substance after the fact — if a finding needs correction, add a new row
referencing the original.

This is a starter log with the format demonstrated on real seed rows, not
a fabricated extensive history. Most rows below document the initial
knowledge-layer build on 2026-08-03.

## Format

| Date | Reviewer | Artifact reviewed | Finding | Action |
|---|---|---|---|---|

- **Date**: ISO format, `YYYY-MM-DD`.
- **Reviewer**: name or role (e.g. "Commercial Desk", "Sales Lead").
- **Artifact reviewed**: file path or client proposal ref.
- **Finding**: what was checked and what was found — pass, discrepancy,
  gap. Be specific enough that a later reader doesn't have to re-derive
  the context.
- **Action**: what was done as a result — fixed in the same commit,
  logged as a defect, escalated, no action needed.

## Log

| Date | Reviewer | Artifact reviewed | Finding | Action |
|---|---|---|---|---|
| 2026-08-03 | Commercial Desk | `pricing/policy.yaml` vs `pricing/rate-card.yaml` | Cross-checked every `segments.*.blended_rate_aed` pin against its source role in `rate-card.yaml` before first commit. Draft pin had `smb` at 425 and `mid_market` at 550 — the pre-revision Consultant/Senior Consultant rates. `rate-card.yaml` v2 (22 Jul 2026) revised those roles to 395 and 525. Left unreconciled, every `smb` proposal would have overquoted by AED 30/hr and every `mid_market` proposal by AED 25/hr. | Corrected `policy.yaml` pins to 395/525 in the same commit as `rate-card.yaml`. Documented the check in `policy.yaml`'s header comment and seeded the incident as `failure-modes/known-defects.md #1` so the mechanism (build both files in the same commit, cross-check pins) is visible to every future SDR, not just this reviewer. |
| 2026-08-03 | Commercial Desk | Initial seed of `00-knowledge/` and `01-templates/` (see `CHANGELOG.md: pricing v1.0`) | Confirmed all pricing files (`rate-card.yaml`, `saas-modules.yaml`, `hosting.yaml`, `support-training.yaml`, `hour-lookup.yaml`, `policy.yaml`) trace to `commercial-pricing-revised-v2.xlsx` and the SGCTECH.AI pricing playbook, with sources cited inline in each file. `subscription-guardrails.md` (G1–G10) confirmed as a correct mechanization of `12-commercial-rules.md`. | No corrections needed. Logged as the baseline review for `knowledge_version_used: 1.0` — any future worksheet pinning this version can be traced back to this row as the review that cleared it for use. |
| 2026-08-03 | Sales Lead | `02-clients/VGE-vongeyern-realestate` (Rev1, Rev2 issued; Rev3 in draft) | Ported in as the repo's live worked example alongside the seed. Verified `05-issued/` contains only Rev1 and Rev2, immutable, and that Rev3 exists solely in `03-draft/` per the revision-immutability rule. | No corrections needed. Confirmed as the reference example for `05-ops/naming-conventions.md` proposal-ref format (`VGE-2026-SUB-01_RevN`). |

## Notes for reviewers

- If a finding matches an existing `known-defects.md` entry, cite the
  entry number rather than re-describing the mechanism — keeps this log
  short and the defect catalog as the single source of the "why."
- A finding with no corrective action is still worth a row — it's evidence
  the check happened, which matters when someone later asks "was this ever
  reviewed."
