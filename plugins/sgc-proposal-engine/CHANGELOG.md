# Changelog — sgc-proposal-engine (SDR plugin)

All notable changes to the SDR plugin are recorded here. Per the
versioning protocol, any rate, formula, gate, or clause change is a
version bump with the author recorded. The desk-side
`redacted-derivative-release` skill is the only authorised writer of
the redacted derivatives.

## [1.0.0] — 2026-08-04

### Added

- Six skills: `proposal-intake`, `subscription-pricing`, `proposal-drafting`, `contract-assembly`, `approval-gate` (Part 1 of the build — the mandatory human approval gate), `signature-dispatch`.
- `knowledge/published-floor-table.yaml` — desk-authored minimum quotable subscription per cell (users × edition × term × cadence). G42 cross-checks proposals against this table.
- `knowledge/guardrails-g42-g53.yaml` — mirror copy of the canonical desk plugin's plugin-conversion guardrails. G42 (published-floor), G43 (package-rate), G44 (edition disclosure), G45 (VAT disclosure), G53 (no envelope without valid approval record).
- Redacted derivatives of `00-knowledge/pricing/policy.yaml`, `hosting.yaml`, `payment-plans.yaml`, `concession-ladder.yaml`, `phase2-catalogue.yaml`, and `00-knowledge/runbook/subscription-proposal-runbook.md`. Verified by `ci/diff-redacted-derivatives.py`.
- Verbatim copies of `00-knowledge/pricing/rate-card.yaml`, `editions.yaml`, `hour-lookup.yaml`, `saas-modules.yaml`, `support-training.yaml`, `risk-security-matrix.yaml`.
- Verbatim copies of `00-knowledge/commercial-rules/` (G1–G41 statements).
- Verbatim copies of `00-knowledge/clause-library/` (24 files).
- Verbatim copies of `09-agent/` (the intake / fabrication / step-gate / question-bank / sufficiency / session-log files).
- Sanitized copies of `01-templates/proposal/` (13 sections + section-map) and `01-templates/intake/client-brief.template.yaml`.
- Sanitized copies of `01-templates/comms/{transmittal-letter,follow-up-email}.md`.
- Sanitized copies of `06-brand/tokens/*.yaml` and `06-brand/styles/proposal.pdf.css`.
- `contracts/msa-sla.html` (sanitized copy of root MSA & SLA v2026.08).
- `contracts/order-form.template.html` (extracted Appendix I Order Form template).
- `workspace-bootstrap/` (verbatim copy of `02-clients/_SCAFFOLD/`).
- `init-workspace.sh` — creates `<cwd>/sgc-proposals/<CLIENT-CODE>/` from the bootstrap on first run.
- `ci/diff-redacted-derivatives.py` — diff gate for the redacted derivatives.
- `ci/forbidden-strings.sh` — scans the plugin for `AED 690`, `43,300`, `3,700`, `TRN`, `VAT exempt`, `free zone exempt`, `Enterprise tier`, `unlimited`, `AWS`, `Odoo mobile app`, `hosting_node_true_cost`, `liquid reserve`, `AED 7,000`, `AED 14,000`, `AED 4,960`, `internal_consultant_cost`, `absolute_margin_floor`, `AED 150/h`, `AED 150/hr`, `AED 360`, `150 AED`, `360 AED`.
- `ci/secrets-scan.sh` — detects AWS keys, Zoho refresh tokens, generic API key patterns, base64 long strings, `whsec_` not equal to `whsec_test_0000`, cheque numbers, plain-text email addresses.
- `tests/acceptance.sh` — runs all 10 acceptance items from the build brief.
- `README.md` — states that pricing content is desk-owned and local edits are overwritten on sync.

### Security

- The plugin does **not** include the Zoho Sign handler. The handler lives in the SRE repo and is invoked over a Den-managed MCP connection. No credentials in the plugin.
- The plugin does **not** include `10-signature/handler/`, `webhook-fixtures/`, or `sgc-crm-fields/`.
- The plugin does **not** include real client folders (`02-clients/MRD-meridianview-realty/`, `02-clients/VGE-vongeyern-realestate/`) or any `DEMO-` folders.

### Known limitations

- The `published-floor-table.yaml` is shipped with conservative defaults. The desk may tighten any cell by re-issuing the file with a version bump. Until the desk does so, the cells are pre-publication defaults; the approval-gate blocks on any cell whose proposed AED/mo is below the published value.
- The root MSA at `subscription_mode_sla_msa.htm` still has stale `FZE` and unresolved IFZA/DIFC/address. The SDR plugin ships a verbatim copy of the root file. The drift is flagged in `PUBLISHING.md` for desk-side remediation.
- The Zoho Sign FROM address is currently `notifications@zohosign.com`, not the branded `hello@scholarixglobal.com`. The `signature-dispatch` skill surfaces this on every send as a deliverability/recognition warning (not a validity block).
