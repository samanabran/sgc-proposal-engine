# Brand QA Checklist — RVN-2026-SUB-01_Rev1

- [x] No colour, type, grid, or decor tokens used in the drafted markdown sections — plain markdown only at this stage, no brand-token rendering applied yet (deferred to PDF/DOCX render step, out of scope for this pipeline run)
- [ ] Every entity fact (legal name, licence authority, address, contact) — **BLOCKED**: `06-brand/entity/legal-identity.yaml` fields are unresolved (`RESOLVE`) per known repo state. This is the expected, by-design check-14 block per SKILL.md §6 — administrative, not a gate failure. `RVN` is used as the working client name throughout; the client's actual legal name was not stated on the discovery call (see `client-brief.yaml`).
- [ ] Co-branding — N/A, no co-brand agreement for this client
- [x] No Arabic content used
- [x] No landscape layout used outside §10 commercial table (N/A at markdown stage)

Reviewer: _pending human review_  Date: _______________
Result: [ ] Approved   [x] Changes required — entity fields must be supplied by Commercial Desk before **issue** (not before draft/review); see `manifest.yaml: escalations`
