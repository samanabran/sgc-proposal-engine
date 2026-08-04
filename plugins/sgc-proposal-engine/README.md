# sgc-proposal-engine (SDR plugin)

The SDR-facing proposal-engine plugin for Scholarix Global Consultants
FZCO (SGC TECH AI). Six skills cover the 13-step pipeline from
intake to envelope send, plus a sanitized knowledge base the SDR
plugin can read at runtime.

## Who is this for

All SDRs. Assigned via Den RBAC. Not for the approver — the
approver uses `sgc-commercial-desk` instead.

## Skills

1. `proposal-intake` (step 1) — interrogates a vague request, runs the tiered question bank, confirms the fact ledger
2. `subscription-pricing` (steps 3–8) — pricing worksheet, payment-plan worksheet, risk assessment, exposure, walk-away card, gate check
3. `proposal-drafting` (steps 9–11) — renders the 13-section HTML, applies the brand, produces the frozen PDF with SHA-256
4. `contract-assembly` (steps 10–11) — Order Form, MSA & SLA, consistency map
5. `approval-gate` (step 12) — the mandatory human approval gate. Sole approver: Ali Asghar Teli Muhammad Iqbal Teli. SHA-256 binding to the frozen PDF.
6. `signature-dispatch` (step 13) — calls Zoho Sign, refuses to send without a valid approval record (G53), degrades gracefully if the Odoo sgc_crm_fields module is not deployed

The fixed sequence is enforced by every skill's body. Out-of-order invocation is refused by name and the specific gate that forbids it.

## What this plugin does NOT contain

- The desk-only cost-to-serve formula, the absolute margin floor (G23), the internal AED 150/h, the cash exposure caps, the liquid reserve figures, the concession-ladder true values, the walk-away true values, the deal-card template, the abort criteria, the early-warning indicators, the runbook's worked numbers, the operational validator, the failure-mode internal defect history, the `06-brand/entity/legal-identity.yaml` (with the signatory's name, phone, licence number, registered address, contact details), the brand QA checklist, the rotation.yaml, the registry.yaml, the watermark masters, the source fonts, the Zoho Sign handler code, the webhook fixtures, the `sgc_crm_fields` Odoo module, the `08-contracts/` VGE-specific consistency map, the untracked duplicate MSA, the `_SCAFFOLD` per-client real folders (`MRD-meridianview-realty/`, `VGE-vongeyern-realestate/`), or any `DEMO-` folder.

All of the above live in `sgc-commercial-desk`. The Den RBAC assignment is the confidentiality boundary; this plugin is a subset of the desk's knowledge, redacted.

## Pricing content is desk-owned

This plugin's pricing content (`knowledge/policy.yaml`, `hosting.yaml`,
`payment-plans.yaml`, `concession-ladder.yaml`, `phase2-catalogue.yaml`,
`published-floor-table.yaml`, and the `subscription-proposal-runbook.md`)
is **desk-owned**. The desk authors and re-issues the
`published-floor-table.yaml` whenever a cell changes. The redacted
derivatives are cut by the desk's `redacted-derivative-release` skill.

**Local edits to any of these files are overwritten on sync.** Do not
edit them locally; the next sync will revert your change. If you
need a new figure, ask the desk. If you find a defect in a redaction,
open an issue against the desk plugin's `redacted-derivative-release`
skill.

## How to use

The plugin is loaded by Den from the marketplace manifest. The
six skills are available via the agent's normal skill invocation.
Out-of-order invocation is refused with a specific gate citation.

On first use of `proposal-intake` for a new client, run
`init-workspace.sh` to create the per-client folder. The script
copies `workspace-bootstrap/` to `<cwd>/sgc-proposals/<CLIENT-CODE>/`.

## CI gates (run on every commit to this plugin's path)

- `ci/diff-redacted-derivatives.py` — verifies the redacted derivatives match the desk originals on the SDR-safe line set and contain no desk-only line
- `ci/forbidden-strings.sh` — verifies no forbidden string appears in the plugin
- `ci/secrets-scan.sh` — verifies no credential, key, or client PII in any bundled file

A failure on any of these blocks release. The GitHub Actions
workflow runs them on every commit to `plugins/sgc-proposal-engine/`.

## Acceptance

`tests/acceptance.sh` runs the 10 acceptance items from the build
brief. Each item reports pass/fail individually. The script is the
canonical answer to "is the plugin ready to ship?".

## Versioning

Semantic versions per `plugin.json` and `CHANGELOG.md`. Any rate,
formula, gate, or clause change is a version bump with the author
recorded. The desk-side `redacted-derivative-release` skill is the
only authorised writer of the redacted derivatives; the desk
publishes new versions and the SDR plugin receives them via sync.

## Related

- `sgc-commercial-desk` — the approver-only plugin. RBAC-assigned to the approver (Ali Asghar Teli Muhammad Iqbal Teli) only.
- `PUBLISHING.md` at the repo root — Den self-host + RBAC + sync steps.
- `DISTRIBUTION-MANIFEST.md` at the repo root — every repo file's classification.
- `MIGRATION-NOTES.md` at the repo root — what moved, what was excluded, what an SDR does on first run.
