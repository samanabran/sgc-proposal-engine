# sgc-commercial-desk (approver plugin)

The approver-only plugin for Scholarix Global Consultants FZCO
(SGC TECH AI). Five skills cover the desk-side counterparts of the
SDR pipeline, plus the full desk-only knowledge base.

## Who is this for

**One person only**: the named approver, Ali Asghar Teli Muhammad
Iqbali Teli, Company Manager. Assigned via Den RBAC. No
delegation, no alternate, no "approved by agent on behalf of."

The SDR plugin (`sgc-proposal-engine`) is for the SDR team. The
desk plugin is for the approver. The two plugins together are the
full pipeline.

## Skills

1. `walk-away-authoring` (step 7) — desk-side counterpart to `subscription-pricing`. Authors the per-deal walk-away card, computes the desk-only figures (CTS, internal build cost, margin floor, peak cash exposure, reservation pricing) the SDR plugin never sees.
2. `deal-card-review` (step 8) — the approver's review. Reads the deal card, exposure calculation, and gate report together. Ratifies or returns reviewer notes.
3. `published-floor-authoring` (anytime) — authors and maintains the `published-floor-table.yaml` consumed by the SDR plugin's G42 guardrail.
4. `redacted-derivative-release` (anytime) — authors and verifies the redacted derivatives the SDR plugin ships. Runs the diff gate. Pushes new versions.
5. `signature-handler-monitor` (continuous) — monitors the webhook handler's signature pipeline, alerts on G46–G52 anomalies, reconciles `pending-odoo-writes.yaml` when `sgc_crm_fields` is deployed.

## What this plugin contains

Everything the SDR plugin doesn't, plus the desk-side originals:

- The full `00-knowledge/` — pricing (with desk-only cost_to_serve, financing_uplift reasoning, absolute_margin_floor, withdrawn structures), commercial-rules, clause-library, market-data, failure-modes, the full runbook.
- The full `07-protection/` — doctrine, walkaway, exposure, abort, monitoring, evidence.
- The full `04-governance/` — access-model, approval-matrix, escalation-triggers, negotiation-authority, review-log.
- The full `05-ops/` — glossary, naming-conventions, onboarding-new-sdr, validate.md, validate.py.
- The full `06-brand/` — entity, registry, brand-qa-checklist, rotation, locale, co-brand, tokens, styles, watermarks, fonts.
- The full `10-signature/` reference material — **except** the handler code, the webhook fixtures, and the `sgc_crm_fields` Odoo module. The handler is in the SRE repo.
- The full `08-contracts/` (root MSA) and a generic consistency-map template. The untracked duplicate `08-contracts/subscription_sla_msa.html` (still says FZE) is **excluded**; the root MSA is canonical.
- The `guardrails-g42-g53.yaml` canonical (G42–G45, G53). G46–G52 are in `10-signature/guardrails-G46-G52.md`.

## What this plugin does NOT contain

- The Zoho Sign handler code (`10-signature/handler/`) — the handler is in the SRE repo. The desk's `signature-handler-monitor` reads its logs over a Den-managed MCP connection.
- Real client folders (`02-clients/MRD-meridianview-realty/`, `02-clients/VGE-vongeyern-realestate/`) — historical, in the repo root, excluded from both bundles.
- Any `DEMO-` folder — none exist in this repo, but the rule stands: excluded from both bundles.

## Sole approver

`Ali Asghar Teli Muhammad Iqbal Teli` — Company Manager, Scholarix
Global Consultants FZCO / SGC TECH AI. Encoded as a literal string
in `knowledge/guardrails-g42-g53.yaml: approver.name` and enforced at
the SDR plugin's `approval-gate` and `signature-dispatch` skills.

## How to use

The plugin is loaded by Den from the marketplace manifest. The five
skills are available via the agent's normal skill invocation. The
desk's RBAC assignment ensures only the named approver runs them.

When the desk needs to re-issue the `published-floor-table.yaml` or
re-cut a redacted derivative, the appropriate skill runs, the diff
gate passes, the version is bumped, and `PUBLISHING.md` describes
the sync mechanism that pushes the new file to the SDR plugin.

## Versioning

Semantic versions per `plugin.json` and `CHANGELOG.md`. Any rate,
formula, gate, or clause change is a version bump with the author
recorded. Bad versions reach everyone via sync — CI revalidates on
every commit.

## Related

- `sgc-proposal-engine` — the SDR-facing plugin. RBAC-assigned to all SDRs.
- `PUBLISHING.md` at the repo root — Den self-host + RBAC + sync steps.
- `DISTRIBUTION-MANIFEST.md` at the repo root — every repo file's classification.
- `MIGRATION-NOTES.md` at the repo root — what moved, what was excluded, what an SDR does on first run.
