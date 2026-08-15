# Reviewer Notes — RVN-2026-SUB-01_Rev1

**Status**: Draft complete, all 41 commercial gates pass, validate.py run
pending. This revision has NOT been through human review yet — these are
open items surfaced during self-QA (`04-review/qa-checklist.md`) for the
human reviewer's attention, not a completed review.

## Open items before issue (not before draft/review)

1. **Transmittal/cover letter not yet drafted.** Template exists at
   `01-templates/comms/transmittal-letter.md` — draft once a revision is
   approved for issue, not before.
2. **Entity facts unresolved** (`06-brand/entity/legal-identity.yaml`) —
   check-14, by-design administrative block per SKILL.md §6. Does not
   block draft or human review; blocks issue only.
3. **Client legal name unconfirmed** — "RVN" used as the working name
   throughout. Confirm the registered legal name before any signed
   document is issued.
4. **Risk-band assumptions** — 4 of 8 `risk-security-matrix.yaml` inputs
   (entity age, VAT registration, trade licence validity, jurisdiction)
   are call-transcript ASSUMPTIONS, not confirmed facts. Scored toward
   the higher-risk side; re-score once confirmed — see
   `02-calc/risk-assessment.yaml: notes`.
5. **Two uncatalogued feature requests** (automated call-analyzer/
   telephony integration; sensor-based attendance tracking) are
   explicitly excluded from Phase 1 pricing and flagged throughout the
   draft (§05, §06, §07, §12) and in `manifest.yaml: escalations`. These
   require Commercial Desk scoping once RVN's phone/telephony stack and
   sensor vendor/API are known — not a defect in this draft, a genuine
   knowledge-layer gap correctly escalated rather than guessed.
6. **G1 boundary pass** — `platform_portion_aed_mo` (1,170) equals the
   CTS floor exactly, with no margin above it. If any concession is
   requested on this deal, there is zero headroom on the platform
   portion before it breaches G1 — reduce scope or use the concession
   ladder's other levers (recovery uplift, cadence, term) instead.
7. **Migration record count** — 400-600 leads/month volume confirmed;
   total Google Sheet backlog record count not stated. `data_migration_500`
   used as the nearest catalogue band; confirm actual count before
   kickoff.
