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
| 2026-08-03 | Commercial Desk | `pricing/policy.yaml` vs `pricing/rate-card.yaml` (v1 build) | Cross-checked every `segments.*.blended_rate_aed` pin against its source role in `rate-card.yaml` before first commit. Draft pin had `smb` at 425 and `mid_market` at 550 — the pre-revision Consultant/Senior Consultant rates. `rate-card.yaml` v2 (22 Jul 2026) revised those roles to 395 and 525. Left unreconciled, every `smb` proposal would have overquoted by AED 30/hr and every `mid_market` proposal by AED 25/hr. | Corrected `policy.yaml` pins to 395/525 in the v1 build. Superseded in the v2 hardening pass below — see that row for why the same class of drift reappeared. |
| 2026-08-03 | Commercial Desk | Initial seed of `00-knowledge/` and `01-templates/` (see `CHANGELOG.md: pricing v1.0`) | Confirmed all pricing files (`rate-card.yaml`, `saas-modules.yaml`, `hosting.yaml`, `support-training.yaml`, `hour-lookup.yaml`, `policy.yaml`) trace to `commercial-pricing-revised-v2.xlsx` and the SGCTECH.AI pricing playbook, with sources cited inline in each file. `subscription-guardrails.md` (G1–G10, v1) confirmed as a correct mechanization of `12-commercial-rules.md`. | No corrections needed. Superseded by pricing v2.0 — see below. |
| 2026-08-03 | Sales Lead | `02-clients/VGE-vongeyern-realestate` (Rev1, Rev2 issued; Rev3 in draft) | Ported in as the repo's v1 live worked example. Verified `05-issued/` contains only Rev1 and Rev2, immutable, and that Rev3 exists solely in `03-draft/`. | No corrections needed. Kept intact, unmodified, when the v2 hardening pass began — its history remains a clean revision example even though pricing policy has since moved to v2.0. |
| 2026-08-03 | Commercial Desk | `pricing/policy.yaml` v2.0 rebuild (segments block) | This build's own source brief re-specified `segments.smb.blended_rate_aed` (425) and `segments.mid_market.blended_rate_aed` (550) — the **same pre-revision figures** the row above already flagged and fixed once, verbatim, in the v2 rebuild's own instructions. | Used as specified per the "don't invent numbers" build instruction, but flagged inline in `policy.yaml` and logged as `known-defects.md` #21 rather than silently re-corrected or silently accepted — routed to Commercial Desk for resolution: either re-pin to real roles or confirm these are deliberately independent blended figures. |
| 2026-08-03 | Commercial Desk | `03-library/worked-examples/boutique-brokerage-5users-24mo.md` | A worked example built in parallel with the v2 guardrail rewrite used the pre-correction G1 formula (`cts_total_aed × 1.25 ≤ build_value_aed + cts_total_aed`) instead of the corrected one (recurring price ≥ platform floor). | Corrected before commit; logged as `known-defects.md` #22 — a process note about parallel work needing to re-check against current source, not the source as it stood when that work began. |
| 2026-08-03 | Commercial Desk | `02-clients/MRD-meridianview-realty/03-draft/MRD-2026-SUB-01_Rev3/09-partnership-terms.md` and `13-next-steps.md` | Dispute-and-jurisdiction clause and the SGC-side signature block both depend on `06-brand/entity/legal-identity.yaml` fields that are still `RESOLVE`. | Correctly blocked, not worked around — flagged explicitly in `04-review/reviewer-notes.md` for this client folder as an open item for Founder + Commercial Desk, per the entity file's own fail-loudly design. Rev3 is not yet issue-ready for this reason alone; all 41 commercial gates otherwise pass. |
| 2026-08-04 | External review (pre-push) | `pricing/policy.yaml` segments block, row above (`known-defects.md` #21) | Reviewer pushed back on the "flag inline, route to Commercial Desk" resolution: "don't invent numbers" governs fabricating market data, not preserving a rate known to be wrong in a live operational config other SDRs price off without reading a comment. Correct call. | `smb`/`mid_market` re-pinned to real `rate-card.yaml` roles. `mid_market`'s rejected value added to `rate-card.yaml: forbidden_rates` (same treatment as the 690 defect). `smb`'s rejected value can't be blanket-forbidden the same way (it's legitimately `qa_engineer`'s real rate), so `validate.py` gained a structural check (`check_1c_segment_pins`) verifying every segment's `blended_rate_aed` matches its declared `pinned_role` exactly. `known-defects.md` #21 updated to record the resolution, not just the flag. |
| 2026-08-04 | External review (pre-push) | `05-ops/validate.py` forbidden-phrase matching | Reviewer noted the VAT-registered/iOS-Android-app false-positive fix (already caught and corrected this session) was "the right catch" and asked for it to become a permanent regression case, not a one-off fix. | Added `SELFTEST_MUST_NOT_FLAG` / `SELFTEST_MUST_FLAG` corpus and a `--selftest` mode, run automatically before every real `validate.py` invocation. Logged as `known-defects.md` #23. |
| 2026-08-04 | External review (pre-push) | Full `git log -p --all` history scan | Checked for credentials, real TRNs, hosting secrets, or PII that entered and was later removed. | Clean — only the two fictional TRN placeholders (`VGE`, `MRD` client briefs) found, no real credentials or identifiers anywhere in history. |
| 2026-08-04 | External review (pre-push) | GitHub repo visibility (`samanabran/sgc-proposal-engine`) | Confirmed via `gh repo view --json visibility,isPrivate` before push, not after. | `"isPrivate": true, "visibility": "PRIVATE"` — confirmed. Pushed 6 local commits to `origin/main`. |

## Notes for reviewers

- If a finding matches an existing `known-defects.md` entry, cite the
  entry number rather than re-describing the mechanism — keeps this log
  short and the defect catalog as the single source of the "why."
- A finding with no corrective action is still worth a row — it's evidence
  the check happened, which matters when someone later asks "was this ever
  reviewed."
