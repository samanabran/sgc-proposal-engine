# SGC TECH AI — Scholarix Global Consultants FZCO

The SGC TECH AI proposal engine. Two installable plugins, one
marketplace:

- **`sgc-proposal-engine`** — SDR-facing. Six skills for the 13-step
  proposal pipeline, plus a sanitized knowledge base. Assigned to
  the SDR team.
- **`sgc-commercial-desk`** — approver-only. Five skills for the
  desk-side counterparts, plus the full desk-only knowledge base.
  Assigned to the named approver (`Ali Asghar Teli Muhammad Iqbal
  Teli`) only.

The marketplace lives at `.claude-plugin/marketplace.json`. The
distribution manifest at `DISTRIBUTION-MANIFEST.md` classifies every
repo file as `sdr` / `desk` / `both` / `excluded`. The publishing
guide at `PUBLISHING.md` describes the Den self-host + RBAC + sync
steps. The migration notes at `MIGRATION-NOTES.md` describe what
moved, what was excluded, and what an SDR does on first run.

## The mandatory human approval gate

Nothing reaches a client without a recorded decision from the named
approver. The `approval-gate` skill in the SDR plugin produces a
`05-approval/approval-request.md` and stops; the approver writes
`05-approval/approval-record.yaml` with a SHA-256 binding to one
exact artifact. The `signature-dispatch` skill refuses to send
without a valid, unexpired, hash-matching approval record (G53).
Re-approval is a new record, never an edit of the old one.

## The two plugins, side-by-side

| Plugin | Skills | Knowledge | RBAC |
|---|---|---|---|
| `sgc-proposal-engine` | 6 (intake, pricing, drafting, contract-assembly, approval-gate, signature-dispatch) | Sanitized derivatives + verbatim clause-library + verbatim commercial-rules | All SDRs |
| `sgc-commercial-desk` | 5 (walk-away-authoring, deal-card-review, published-floor-authoring, redacted-derivative-release, signature-handler-monitor) | Full desk originals (`00-knowledge/`, `07-protection/`, `04-governance/`, `05-ops/`, `06-brand/`, `10-signature/` reference) | Approver only |

The Den RBAC assignment is the confidentiality boundary. Plugin
content is a subset of the desk's knowledge, redacted. Both plugins
together are the full pipeline.

## The 13-step pipeline

```
intake → fact ledger confirmed → risk assessment → pricing worksheet →
payment-plan worksheet → exposure calculation → walk-away card →
gates G1–G41 → brand resolution → draft → consistency map → validate →
QA → PDF + hash → approval gate → envelope
```

Every skill in either plugin names its position in this sequence and
refuses to run out of order. The refusal cites the specific gate
that forbids the out-of-order invocation.

## The guardrails

- **G1–G41** — commercial guardrails (subscription, payment-plan,
  protection). Stated verbatim in
  `00-knowledge/commercial-rules/{subscription,payment-plan,protection}-guardrails.md`.
- **G42–G45** — plugin-conversion guardrails (published-floor,
  package-rate, edition disclosure, VAT disclosure). Authored in
  `plugins/sgc-commercial-desk/knowledge/guardrails-g42-g53.yaml`;
  mirror copy in the SDR plugin.
- **G46–G52** — signature-pipeline guardrails. Stated verbatim in
  `10-signature/guardrails-G46-G52.md`.
- **G53** — the new approval-record gate. No envelope may be
  created without a valid `approval-record.yaml` whose
  `approved_artifact_sha256` matches the PDF being sent.

## CI gates

Run on every commit to a plugin path; failure blocks release:

- `plugins/sgc-proposal-engine/ci/diff-redacted-derivatives.py` —
  verifies the redacted derivatives match the desk originals on the
  SDR-safe line set and contain no desk-only line
- `plugins/sgc-proposal-engine/ci/forbidden-strings.sh` — verifies
  no forbidden string appears in the plugin
- `plugins/sgc-proposal-engine/ci/secrets-scan.sh` — verifies no
  credential, key, or client PII in any bundled file
- `plugins/sgc-proposal-engine/tests/acceptance.sh` — runs all 10
  acceptance items

The GitHub Actions workflow lives at
`plugins/sgc-proposal-engine/ci/github-actions-workflow.yml` and is
referenced for placement at `.github/workflows/plugin-gates.yml`.

## Company facts

- **Not registered for UAE VAT. No TRN.** The gross-up clause from
  `00-knowledge/clause-library/vat-gross-up.md` is verbatim in the
  MSA §C.6. Never "VAT inclusive", "VAT exempt", "free zone
  exempt", or any TRN field in the proposal narrative.
- **Odoo Community default**, version-pinned. State exclusions
  plainly: no Odoo Enterprise mobile app (mobile-optimised browser
  only), no Studio, limited advanced accounting, major upgrades
  quoted separately.
- **"Enterprise" refers only to the Odoo edition.** Top service
  tier is **Professional**.
- **G32**: every deal cash-positive within 30 days of Kickoff.
- **G33**: Quarterly in advance minimum cadence.
- **G34**: Mobilisation ≥33% and covers any pre-paid third-party
  cost.

## Open RESOLVE fields

The following block the first go-live of the plugin; the desk
authorises each before any SDR receives the plugin. See
`PUBLISHING.md` for the full list.

1. The root MSA at `subscription_mode_sla_msa.htm` still has stale
   FZE and unresolved IFZA/DIFC/address. The entity file
   `06-brand/entity/legal-identity.yaml` resolves to FZCO/IFZA/Al
   Rigga. The plugin ships the root MSA verbatim; the desk-side
   remediation is a separate task.
2. **Den deployment status** — whether Den is fully configured for
   this team's RBAC and sync is unknown.
3. **GitHub connector configuration** — the connector that lets
   Den pull from the repo is **not yet configured**.

Countersignatory is resolved: `Ali Asghar Teli Muhammad Iqbal
Teli` per `06-brand/entity/legal-identity.yaml: contact.name`.

## What this repository contains

- `AGENTS.md` — the desk's authoritative operating contract
- `CHANGELOG.md` — the desk's changelog
- `README.md` — this file
- `subscription_mode_sla_msa.htm` — canonical MSA & SLA v2026.08
  (root file is provenance)
- `_source-documents/` — source PDFs and the commercial export
  (desk reference)
- `00-knowledge/` — pricing, commercial-rules, clause-library,
  market-data, failure-modes, runbook
- `01-templates/` — proposal sections, intake, comms, QA
- `02-clients/` — historical (MRD, VGE); the `_SCAFFOLD` has been
  moved to `plugins/sgc-proposal-engine/workspace-bootstrap/`
- `03-library/` — worked examples (drafting reference)
- `04-governance/` — access-model, approval-matrix, escalation-triggers
- `05-ops/` — glossary, naming-conventions, onboarding, validate
- `06-brand/` — entity, registry, brand-tokens, styles, watermarks
- `07-protection/` — doctrine, walkaway, exposure, abort, monitoring
- `08-contracts/` — root MSA (canonical) + untracked duplicate
  (excluded from bundles) + VGE-specific consistency map (excluded)
- `09-agent/` — step-gate, fabrication-rules, intake-interview,
  question-bank, sufficiency, session-log (verbatim copies in the
  SDR plugin)
- `10-signature/` — Zoho Sign integration: send-protocol, webhook
  spec, Odoo mapping, audit retention, notification templates,
  guardrails G46–G52. The handler code (`handler/`) is in the SRE
  repo.
- `.claude-plugin/marketplace.json` — the marketplace manifest
- `plugins/` — the two installable plugins
- `DISTRIBUTION-MANIFEST.md` — every file classified
- `PUBLISHING.md` — Den self-host + RBAC + sync
- `MIGRATION-NOTES.md` — what moved, what was excluded, what an SDR
  does on first run

## License

Proprietary — internal use only.
