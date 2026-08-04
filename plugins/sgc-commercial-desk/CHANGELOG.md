# Changelog — sgc-commercial-desk (approver plugin)

All notable changes to the desk plugin are recorded here. Per the
versioning protocol, any rate, formula, gate, or clause change is a
version bump with the author recorded.

## [1.0.0] — 2026-08-04

### Added

- Five skills: `walk-away-authoring`, `deal-card-review`, `published-floor-authoring`, `redacted-derivative-release`, `signature-handler-monitor`.
- `knowledge/guardrails-g42-g53.yaml` (canonical) — G42 (published-floor), G43 (package-rate), G44 (edition disclosure), G45 (VAT disclosure), G53 (no envelope without valid approval record). G46–G52 (signature-pipeline) are referenced from `knowledge/10-signature/guardrails-G46-G52.md`.
- Verbatim copies of the full `00-knowledge/` (pricing, commercial-rules, clause-library, market-data, failure-modes) and `00-knowledge/runbook/subscription-proposal-runbook.md`.
- Verbatim copies of `07-protection/` (doctrine, walkaway, exposure, abort, monitoring, evidence) — the full desk-only layer.
- Verbatim copies of `04-governance/` (access-model, approval-matrix, escalation-triggers, negotiation-authority, review-log).
- Verbatim copies of `05-ops/` (glossary, naming-conventions, onboarding-new-sdr, validate.md, validate.py).
- Verbatim copies of `06-brand/` (entity, registry, brand-qa-checklist, rotation, locale, co-brand, tokens, styles, watermarks, fonts).
- `contracts/subscription_mode_sla_msa.htm` (verbatim copy of the root MSA & SLA v2026.08, including Appendix I Order Form and Appendix IV consistency map).
- `contracts/consistency-map.template.md` (NEW — generic template; the VGE-specific `08-contracts/msa-proposal-consistency-map.md` is excluded).
- `contracts/order-form.template.html` (extracted Appendix I Order Form template).
- `knowledge/10-signature/` reference (excl. `handler/`, `webhook-fixtures/`, `sgc-crm-fields/`).
- `knowledge/published-floor-table.yaml` (canonical) — desk-authored minimum quotable subscription per cell. The SDR plugin's `published-floor-authoring` skill re-issues this when cells change.

### Security

- The plugin does **not** include the Zoho Sign handler. The handler lives in the SRE repo. The desk's `signature-handler-monitor` skill reads handler logs and Odoo state over a Den-managed MCP connection.
- The plugin does **not** include real client folders or any `DEMO-` folder.
- The plugin does **not** include any credential. Zoho tokens, `whsec_` webhook key, and Odoo credentials live in the handler's secret manager.

### Known limitations

- The root MSA at `subscription_mode_sla_msa.htm` still has stale `FZE` and unresolved IFZA/DIFC/address (lines 152–153, 217–225, 318–320, 1831). The entity file `06-brand/entity/legal-identity.yaml` resolves the drift to FZCO/IFZA/Al Rigga. The desk plugin ships the root MSA as-is and flags the drift in `PUBLISHING.md` for a separate desk-side remediation task.
- The Zoho Sign FROM address is currently `notifications@zohosign.com`, not the branded `hello@scholarixglobal.com`. The `signature-handler-monitor` skill reports the status; `signature-dispatch` (in the SDR plugin) surfaces the warning on every send.
- The `published-floor-table.yaml` is shipped with conservative defaults. The desk must review and tighten each cell before this plugin is published to production.
- `validate.py` documents 18 checks but only implements ~13. The agentic validator (in the SDR plugin) is the primary enforcement path; `validate.py` is an optional fast-path called only when Python is detected. No `validate.py` code fix is required for this build.
- The `sgc_crm_fields` Odoo module is not installed. The `signature-dispatch` skill degrades gracefully by appending to `05-approval/pending-odoo-writes.yaml`; the desk's `signature-handler-monitor` skill reconciles when the module is deployed.
