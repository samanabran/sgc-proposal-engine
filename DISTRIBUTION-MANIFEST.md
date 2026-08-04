# DISTRIBUTION MANIFEST

Classification of every repository file as `sdr` (shipped in the `sgc-proposal-engine` plugin), `desk` (shipped in the `sgc-commercial-desk` plugin), `both` (shipped in both), or `excluded` (never bundled). RBAC at the Den level is the confidentiality boundary — plugin content is readable on the installer's disk. The manifest exists to drive CI gates (`forbidden-strings.sh`, `secrets-scan.sh`, `diff-redacted-derivatives.py`) and to inform the `acceptsence.sh` test set.

Generated: 2026-08-04. Plugin versions: sgc-proposal-engine v1.0.0, sgc-commercial-desk v1.0.0.

## Top-level

| Path | Class | Reason |
|---|---|---|
| `AGENTS.md` | desk | Authoritative operating contract; references G1–G41 + commercial rules; not for SDR plugin |
| `CHANGELOG.md` | desk | Records v1→v2 pricing hardening, knowledge internals |
| `README.md` | desk | Repo-level entry point with full layer map |
| `subscription_mode_sla_msa.htm` | both | Canonical MSA & SLA v2026.08 (root file is provenance); SDR plugin gets a sanitized copy; desk ships the root verbatim |
| `_source-documents/` | excluded | Source commercial export and brand guidelines contain desk values and supplier pricing |
| `Playfair_Display/` | excluded | Font cache; the desk-controlled renderer uses bundled base64 or Google Fonts at render time |
| `*.png` (root watermarks) | excluded | Raw watermark masters; the SDR plugin's renderer uses desk-controlled references only |

## `00-knowledge/`

### `00-knowledge/PRECEDENCE.md`

Class: **sdr** — the load order, no desk-only values.

### `00-knowledge/commercial-rules/`

| File | Class | Reason |
|---|---|---|
| `12-commercial-rules.md` | sdr | The 12 base Commercial Rules; qualitative, no arithmetic |
| `subscription-guardrails.md` | sdr | G1–G10 names and tests; numeric anchors are policy.yaml references |
| `payment-plan-guardrails.md` | sdr | G11–G20 names and tests |
| `protection-guardrails.md` | sdr | G21–G41 names and tests |

### `00-knowledge/clause-library/`

All 24 files: class **sdr**. Verbatim client-facing clause text, mechanical triggers, "do not use" guards. No desk-only arithmetic; the `1650-650=1000` derivable from support-training and `[uplift_pct]%` placeholder are template tokens, not desk-only.

| File |
|---|
| `adoption.md`, `clawback.md`, `data-portability.md`, `deferred-start.md`, `dispute-and-jurisdiction.md`, `edition-and-upgrades.md`, `exclusions-standard.md`, `exclusivity-replacement.md`, `financing-disclosure.md`, `force-majeure-and-third-party.md`, `ip-and-configuration.md`, `key-person-and-subcontractor.md`, `liability-cap.md`, `payment-cadence.md`, `post-dated-cheques.md`, `post-recovery-continuation.md`, `price-lock.md`, `referral-capped.md`, `security-deposit.md`, `service-credit-guarantee.md`, `suspension-and-reinstatement.md`, `term-commencement.md`, `vat-gross-up.md`, `vat-uae.md` |

### `00-knowledge/pricing/`

| File | Class | Reason |
|---|---|---|
| `rate-card.yaml` | sdr | Verbatim. Role rates 280/395/425/450/475/525/600/650/700/800; forbidden_rates 690/550; "a rate not listed here does not exist" |
| `editions.yaml` | sdr | Verbatim. Edition names, Community exclusions, Enterprise trigger conditions, upgrade policy |
| `hosting.yaml` | sdr | REDACTED DERIVATIVE: list prices 990/1950/3490 + AWS pass-through 120/350. Cost-basis note (lines 7–14, 38, 40) is desk-only |
| `payment-plans.yaml` | sdr | REDACTED DERIVATIVE: cadence table, one-time structures, hard_caps rates. The `withdrawn.option_b_zero_mobilisation` block and `margin_floor_binding` are desk-only |
| `phase2-catalogue.yaml` | sdr | REDACTED (line 29 only): published prices only. Marginal cost 102 and the "more than double its marginal cost" comment are desk-only |
| `hour-lookup.yaml` | sdr | Verbatim. Per-package hours, no cost basis |
| `saas-modules.yaml` | sdr | Verbatim. Module list prices |
| `support-training.yaml` | sdr | Verbatim. Support tier and training prices |
| `risk-security-matrix.yaml` | sdr | Verbatim. Weights, bands, instrument types, absolute_rule |
| `concession-ladder.yaml` | sdr | REDACTED DERIVATIVE: concession and compensator names, effect descriptions, forbidden_compensators list, procedure narrative. `value_formula` fields are desk-only |
| `policy.yaml` | sdr | REDACTED DERIVATIVE (highest density): `segments`, `overlays`, `gates` numeric anchors (1.25/0.30/0.33/0.25/30/quarterly), `vat` block, `financing_uplift` rates. `cost_to_serve` block (incl. `internal_consultant_cost_aed_hr: 150`), `absolute_margin_floor: 0.25`, header narrative, `monthly_24: 0.18` reasoning, `review_trigger` are desk-only |

### `00-knowledge/runbook/`

| File | Class | Reason |
|---|---|---|
| `subscription-proposal-runbook.md` | sdr | REDACTED (6th interleaved file): stage structure, term selection, option structure, gate check, QA, draft steps. CTS formula, `internal_build_cost = total_hours × 150`, `mobilisation = build_value × 0.33` arithmetic, `max_give_aed` formula, AED 10,800/yr note are desk-only |

### `00-knowledge/market-data/`

| File | Class | Reason |
|---|---|---|
| `benchmarks.yaml` | sdr | Verbatim. External reference benchmarks |
| `sources.md` | sdr | Verbatim. Source list |
| `vertical-notes/uae-real-estate.md` | sdr | Verbatim. RERA, portal APIs, TRN context |
| `vertical-notes/uae-tax-vat.md` | sdr | Verbatim. Public FEC thresholds |

### `00-knowledge/failure-modes/`

| File | Class | Reason |
|---|---:|---|
| `known-defects.md` | desk | Defect #1 (AED 879 vs AED 2,360 cost stack), #4 (33 vs 46 hours), #6 (AED 1,250/mo), #14 (AED 30,000+), #19 (AED 10,800/yr), #21 (smb/mid_market blended rates) are desk-only internal defect history. Defects #2, #7, #8, #9, #10, #11, #12, #16, #17, #18, #20 are publishable as guardrail evidence |

## `01-templates/`

| Path | Class | Reason |
|---|---|---|
| `01-templates/proposal/01-executive-summary.md` | sdr | After scrubbing internal source/gate directive at top + "no VAT" figure |
| `01-templates/proposal/02-about.md` | sdr | After scrubbing any internal source/gate |
| `01-templates/proposal/03-understanding-business.md` | sdr | Verbatim |
| `01-templates/proposal/04-as-is.md` | sdr | Verbatim |
| `01-templates/proposal/05-to-be.md` | sdr | Verbatim |
| `01-templates/proposal/06-solution-phase1.md` | sdr | After scrubbing source/gate and origin-tracking instructions |
| `01-templates/proposal/07-options-inclusions.md` | sdr | Verbatim |
| `01-templates/proposal/08-implementation-recovery.md` | sdr | Verbatim |
| `01-templates/proposal/09-partnership-terms.md` | sdr | Verbatim |
| `01-templates/proposal/10-commercial-terms.md` | sdr | After scrubbing 33% mobilisation, worksheet/knowledge-version references, VAT policy |
| `01-templates/proposal/11-support-sla.md` | sdr | After scrubbing price placeholder and source file |
| `01-templates/proposal/12-why-sgc.md` | sdr | Verbatim |
| `01-templates/proposal/13-next-steps.md` | sdr | After scrubbing 30-day validity and "internal not shown" note |
| `01-templates/proposal/_section-map.md` | sdr | Verbatim |
| `01-templates/intake/client-brief.template.yaml` | sdr | Verbatim |
| `01-templates/comms/transmittal-letter.md` | sdr | Verbatim |
| `01-templates/comms/follow-up-email.md` | sdr | Verbatim |
| `01-templates/comms/correction-notice.md` | excluded | Internal note at line 28; bundled only with desk permissions |
| `01-templates/calc/pricing-worksheet.template.yaml` | excluded | Internal cost, margins, mobilisation all exposed |
| `01-templates/calc/payment-plan-worksheet.template.yaml` | excluded | Internal margin-floor/concession ceilings |
| `01-templates/calc/exposure-calculator.template.yaml` | excluded | Internal cost/cash exposure/portfolio-cap mechanics |
| `01-templates/calc/risk-assessment.template.yaml` | excluded | Exposure bands, internal risk/security instruments |
| `01-templates/qa/pre-send-checklist.template.md` | desk | Internal G references, 41-gate checks, AED 2,500 threshold, forbidden phrase list |
| `01-templates/qa/brand-qa-checklist.template.md` | desk | Internal brand QA references |

## `02-clients/`

| Path | Class | Reason |
|---|---|---|
| `02-clients/_SCAFFOLD/` | both | Becomes `workspace-bootstrap/` in both plugins; empty of numbers, inherits by reference. **The bootstrap does not seed any numbers** — every figure must be loaded at run time from the plugin's knowledge. |
| `02-clients/MRD-meridianview-realty/` | excluded | Real client folder — 29 files |
| `02-clients/VGE-vongeyern-realestate/` | excluded | Real client folder — 33 files |
| (no `DEMO-` folders exist) | n/a | Brief assumption: "anything `DEMO-` prefixed" — there are no such folders in this repo |

## `03-library/`

| Path | Class | Reason |
|---|---|---|
| `03-library/worked-examples/boutique-brokerage-5users-24mo.md` | sdr | Fictional worked example, used as a drafting reference; not under a `DEMO-` prefix (predates convention; flagged in `fabrication-rules.md`) |

## `04-governance/`

All files class **desk** (Sales leadership / Commercial Desk only; SDR does not need to see authority levels and matrix).

| File |
|---|
| `access-model.md` |
| `approval-matrix.md` |
| `escalation-triggers.md` |
| `negotiation-authority.md` |
| `review-log.md` |

## `05-ops/`

All files class **desk**.

| File | Reason |
|---|---|
| `glossary.md` | Glossary of internal terms |
| `naming-conventions.md` | Internal naming |
| `onboarding-new-sdr.md` | References internal runbook/known-defects and MRD/VGE arithmetic (lines 6–17, 24–42, 44–66); requires Sales Lead/Commercial Desk review |
| `validate.md` | Documents 18 checks; partial actual implementation |
| `validate.py` | Validator — not bundleable as a hard dependency; agentic validator in the plugin is the primary path, `validate.py` is an optional fast-path |

## `06-brand/`

| Path | Class | Reason |
|---|---|---|
| `06-brand/entity/legal-identity.yaml` | desk | Sole signatory, licence, registered address, VAT register status, contact details |
| `06-brand/registry.yaml` | desk | Internal asset registry with status/provenance |
| `06-brand/brand-qa-checklist.md` | desk | Internal QA referencing entity facts |
| `06-brand/rotation.yaml` | desk | Per-section landmark rotation; implementation opacity 0.85 |
| `06-brand/locale/ar-AE.md` | desk | Spec incomplete; do not draft Arabic without native review |
| `06-brand/co-brand/rules.md` | desk | Restricts client branding; escalation rules |
| `06-brand/tokens/color.yaml` | sdr | Sanitized render tokens — strip internal comments |
| `06-brand/tokens/type.yaml` | sdr | Sanitized render tokens — strip internal comments |
| `06-brand/tokens/grid.yaml` | sdr | Sanitized render tokens — strip internal comments |
| `06-brand/tokens/decor.yaml` | sdr | Sanitized render tokens — strip internal comments |
| `06-brand/styles/proposal.pdf.css` | sdr | A4 portrait, 20mm margins, brand colour variables (ivory, navy, gold, charcoal, slate, champagne, parchment) |
| `06-brand/styles/landscape.css` | sdr | Verbatim |
| `06-brand/styles/proposal.docx.style.md` | sdr | Verbatim |
| `06-brand/assets/watermarks/` (masters) | desk | 18 PNG masters + derivatives; rendered only by the desk-controlled renderer |
| `06-brand/assets/fonts/` (raw) | desk | Rendered only by the desk-controlled renderer; not bundleable to a generic SDR install |
| `06-brand/assets/.gitkeep` | both | Placeholder |

## `07-protection/`

All files class **desk**. The brief classifies every file in this directory as desk-only; no SDR redaction needed because the directory is not copied into the SDR plugin.

| File |
|---|
| `doctrine.md` |
| `walkaway/deal-card.template.md` |
| `walkaway/reservation-pricing.md` |
| `exposure/exposure-model.md` |
| `exposure/portfolio-limits.yaml` |
| `abort/abort-criteria.md` |
| `evidence/evidence-file-standard.md` |
| `monitoring/early-warning-indicators.yaml` |
| `monitoring/graduated-response.md` |

## `08-contracts/`

| File | Class | Reason |
|---|---|---|
| `08-contracts/subscription_sla_msa.html` | excluded | Untracked duplicate of root MSA; says FZE (pre-correction); conflicts with canonical |
| `08-contracts/msa-proposal-consistency-map.md` | excluded | VGE-specific per-deal reconciliation with PII; not a generic template |

## `09-agent/`

All files class **sdr** (verbatim — these are the intake, fabrication, step-gate, question-bank, sufficiency, and session-log templates that the SDR plugin's `proposal-intake` skill reads).

| File |
|---|
| `step-gate.md` |
| `fabrication-rules.md` |
| `intake-interview.md` |
| `question-bank.yaml` |
| `sufficiency-rules.yaml` |
| `session-log.template.md` |

## `10-signature/`

| Path | Class | Reason |
|---|---|---|
| `10-signature/send-protocol.md` | both | The two-step Zoho API flow. SDR plugin: sanitized (strip env-var names, FROM-status discussion stays). Desk: verbatim |
| `10-signature/odoo-mapping.yaml` | both | Field/event mapping. SDR plugin: summary view only (no env-var names); desk: verbatim |
| `10-signature/guardrails-G46-G52.md` | both | G46–G52 statements. SDR plugin gets the gate names + acceptance criteria; desk gets the full text |
| `10-signature/webhook-spec.md` | desk | Handler contract; not agent concern |
| `10-signature/failure-modes.md` | desk | Failure playbook |
| `10-signature/audit-retention.md` | desk | Retention policy |
| `10-signature/provider-evaluation.md` | desk | Provider choice rationale |
| `10-signature/webhook-db-schema.sql` | excluded | Handler runtime |
| `10-signature/zoho-sign-ui-setup-checklist.md` | desk | Manual ops |
| `10-signature/notification-templates/*.md` | desk | Templates are handler-bound, not plugin-bound |
| `10-signature/webhook-fixtures/*` | excluded | Test fixtures |
| `10-signature/sgc-crm-fields/*` | excluded | Odoo install |
| `10-signature/handler/*` | excluded | **Not bundleable.** Even with no real secrets, env-var names + test placeholder constitute a credential surface. Lives in SRE repo or desk private area only |

## Plugin-generated files (NEW)

The following files are **authored during the build**, not derived from existing repo content.

### In `plugins/sgc-proposal-engine/`

| File | Reason |
|---|---|
| `.claude-plugin/plugin.json` | Plugin manifest |
| `plugin.json` | Marketplace manifest |
| `CHANGELOG.md` | Per-plugin changelog |
| `README.md` | Per-plugin README; **states pricing content is desk-owned and local edits are overwritten on sync** |
| `skills/proposal-intake/SKILL.md` | NEW |
| `skills/subscription-pricing/SKILL.md` | NEW |
| `skills/proposal-drafting/SKILL.md` | NEW |
| `skills/contract-assembly/SKILL.md` | NEW |
| `skills/approval-gate/SKILL.md` | NEW (Part 1) |
| `skills/signature-dispatch/SKILL.md` | NEW (Part 3) |
| `knowledge/published-floor-table.yaml` | NEW (desk-authored, consumed by approval gate and pricing) |
| `knowledge/guardrails-g42-g53.yaml` | NEW (mirror copy in the SDR plugin for reference; canonical in desk plugin) |
| `knowledge/policy.yaml` (redacted) | Hand-authored derivative of `00-knowledge/pricing/policy.yaml` |
| `knowledge/hosting.yaml` (redacted) | Hand-authored derivative |
| `knowledge/payment-plans.yaml` (redacted) | Hand-authored derivative |
| `knowledge/concession-ladder.yaml` (redacted) | Hand-authored derivative |
| `knowledge/phase2-catalogue.yaml` (redacted) | Hand-authored derivative |
| `knowledge/subscription-proposal-runbook.md` (redacted) | Hand-authored derivative |
| `knowledge/clause-library/` (24 files) | Verbatim copies |
| `knowledge/commercial-rules/` (4 files) | Verbatim copies |
| `knowledge/rate-card.yaml`, `editions.yaml`, `hour-lookup.yaml`, `saas-modules.yaml`, `support-training.yaml`, `risk-security-matrix.yaml` | Verbatim copies |
| `knowledge/step-gate.md`, `fabrication-rules.md`, `intake-interview.md`, `question-bank.yaml`, `sufficiency-rules.yaml`, `session-log.template.md` | Verbatim copies |
| `templates/proposal/01–13.md` (+ `_section-map.md`) | Sanitized copies |
| `templates/intake/client-brief.template.yaml` | Verbatim copy |
| `templates/comms/transmittal-letter.md`, `follow-up-email.md` | Verbatim copies |
| `brand/tokens/*.yaml` (4 files) | Sanitized copies |
| `brand/styles/proposal.pdf.css` | Verbatim copy |
| `contracts/msa-sla.html` | Verbatim copy of root MSA (sanitize FZE → FZCO note included) |
| `contracts/order-form.template.html` | Extracted Appendix I Order Form template from root MSA |
| `workspace-bootstrap/` | Verbatim copy of `02-clients/_SCAFFOLD/` |
| `init-workspace.sh` | NEW — creates `<cwd>/sgc-proposals/<CLIENT-CODE>/` from the bootstrap on first run |
| `ci/diff-redacted-derivatives.py` | NEW |
| `ci/forbidden-strings.sh` | NEW |
| `ci/secrets-scan.sh` | NEW |
| `tests/acceptance.sh` | NEW |

### In `plugins/sgc-commercial-desk/`

| File | Reason |
|---|---|
| `.claude-plugin/plugin.json` | Plugin manifest |
| `plugin.json` | Marketplace manifest |
| `CHANGELOG.md` | Per-plugin changelog |
| `README.md` | Per-plugin README |
| `skills/walk-away-authoring/SKILL.md` | NEW |
| `skills/deal-card-review/SKILL.md` | NEW |
| `skills/published-floor-authoring/SKILL.md` | NEW (generates the floor table) |
| `skills/redacted-derivative-release/SKILL.md` | NEW (cuts the SDR-safe derivatives and verifies the diff gate) |
| `skills/signature-handler-monitor/SKILL.md` | NEW (monitors the webhook handler; not a writer) |
| `knowledge/guardrails-g42-g53.yaml` | NEW — canonical |
| `knowledge/policy.yaml` (full) | Verbatim copy |
| `knowledge/hosting.yaml` (full) | Verbatim copy |
| `knowledge/payment-plans.yaml` (full) | Verbatim copy |
| `knowledge/concession-ladder.yaml` (full) | Verbatim copy |
| `knowledge/phase2-catalogue.yaml` (full) | Verbatim copy |
| `knowledge/risk-security-matrix.yaml` (full) | Verbatim copy |
| `knowledge/subscription-proposal-runbook.md` (full) | Verbatim copy |
| `knowledge/07-protection/**` (full) | Verbatim copies |
| `knowledge/00-knowledge/**` (full) | Verbatim copies of every original |
| `governance/**` (full) | Verbatim copies |
| `contracts/subscription_mode_sla_msa.htm` (full) | Verbatim copy of root |
| `contracts/consistency-map.template.md` | NEW — generic template (not the VGE-specific one) |
| `contracts/order-form.template.html` | Extracted Appendix I Order Form |
| `brand/**` (full) | Verbatim copies of every 06-brand file |
| `ops/**` (full) | Verbatim copies of every 05-ops file |
| `10-signature/**` (excl. `handler/`, `webhook-fixtures/`, `sgc-crm-fields/`) | Verbatim copies |

### In `.claude-plugin/`

| File | Reason |
|---|---|
| `marketplace.json` | Lists both plugins with `version`, `description`, `author`, `tags` for RBAC |

### At repo root

| File | Reason |
|---|---|
| `DISTRIBUTION-MANIFEST.md` | This file |
| `PUBLISHING.md` | Den self-host + RBAC + sync steps |
| `MIGRATION-NOTES.md` | What moved, what was excluded, SDR first-run |

## Forbidden strings (CI gate on SDR bundle)

These strings, found anywhere under `plugins/sgc-proposal-engine/`, fail the build:

`AED 690`, `43,300`, `3,700`, `TRN`, `VAT exempt`, `free zone exempt`, `Enterprise tier`, `unlimited`, `AWS`, `Odoo mobile app`, `hosting_node_true_cost`, `liquid reserve`, `AED 7,000`, `AED 14,000`, `AED 4,960`, `internal_consultant_cost`, `absolute_margin_floor`, `AED 150/h`, `AED 150/hr`, `AED 360`, `150 AED`, `360 AED`.

The string `unlimited` is also banned because `hosting.yaml:27` contains `max_users: null   # unlimited` — a value that the desk can interpret but the SDR must never quote.

## CI: secrets-scan.sh targets

AWS access keys (`AKIA[0-9A-Z]{16}`), Zoho refresh tokens (`1000\.[a-f0-9]{32}\.[a-f0-9]{32}`), generic API key patterns, base64 long strings in examples, `whsec_` not equal to the placeholder `whsec_test_0000`, cheque numbers (long digit runs), email addresses of any real person (legal-identity.yaml's `hello@sgctech.ai` is the only allowed address; everything else fails).
