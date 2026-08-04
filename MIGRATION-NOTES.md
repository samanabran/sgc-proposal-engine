# MIGRATION NOTES

What moved, what was excluded, and what an SDR does on first run.

## What moved

The repository's content is now distributed across three locations:

1. **The two plugins** (`plugins/sgc-proposal-engine/`,
   `plugins/sgc-commercial-desk/`) — installable via the marketplace
   manifest. The marketplace lives at
   `.claude-plugin/marketplace.json`. The Den RBAC assignment is the
   confidentiality boundary.
2. **The repo root** — `AGENTS.md`, `CHANGELOG.md`, `README.md`,
   `subscription_mode_sla_msa.htm`, `_source-documents/`, the
   `00-knowledge/`, `01-templates/`, `02-clients/`, `03-library/`,
   `04-governance/`, `05-ops/`, `06-brand/`, `07-protection/`,
   `08-contracts/`, `09-agent/`, `10-signature/` directories — the
   desk originals. The desk plugin pulls verbatim from these.
3. **The new `sgc-proposals/` workspace** — per-client folders
   created at runtime by the SDR plugin's `init-workspace.sh` script.
   The script copies `plugins/sgc-proposal-engine/workspace-bootstrap/`
   to `<cwd>/sgc-proposals/<CLIENT-CODE>/`.

The `02-clients/_SCAFFOLD/` directory has been **moved** to
`plugins/sgc-proposal-engine/workspace-bootstrap/`. The two real
client folders (`02-clients/MRD-meridianview-realty/`,
`02-clients/VGE-vongeyern-realestate/`) stay in the repo root as
historical. New work goes to `<cwd>/sgc-proposals/<CLIENT-CODE>/`.

## What was excluded

The following are **not** in either plugin:

- **All real client folders** — `02-clients/MRD-meridianview-realty/`
  (29 files) and `02-clients/VGE-vongeyern-realestate/` (33 files)
  contain client PII, real contract figures, and audit artefacts.
  These stay in the repo root as historical; the plugins never see
  them.
- **Any `DEMO-` folder** — none exist in this repo, but the rule
  stands: any folder whose name starts with `DEMO-` is excluded
  from both bundles. Demo data lives in the desk-only `03-library/`
  under `worked-examples/` and is referenced from the SDR plugin's
  `proposal-drafting` skill as a drafting reference, not a source.
- **The Zoho Sign handler** — `10-signature/handler/*` lives in the
  SRE repo. The plugin invokes it over a Den-managed MCP
  connection. The handler is not bundled.
- **Webhook fixtures** — `10-signature/webhook-fixtures/*` are test
  fixtures; not bundled.
- **The `sgc_crm_fields` Odoo module** — `10-signature/sgc-crm-fields/*`
  is an Odoo install; not bundled.
- **The untracked duplicate MSA** — `08-contracts/subscription_sla_msa.html`
  is an untracked alternate/duplicate of the root MSA & SLA. The
  root MSA at `subscription_mode_sla_msa.htm` is canonical. The
  duplicate is excluded.
- **The VGE-specific consistency map** — `08-contracts/msa-proposal-consistency-map.md`
  is a per-deal reconciliation with PII. Not a generic template.
  Excluded. The desk plugin ships a generic
  `contracts/consistency-map.template.md` instead.
- **Source documents** — `_source-documents/` (SGC-TECH-AI-Brand-Guidelines-v3.pdf,
  SGC-TECH-AI-Commercial-Export-v2_REVISED.xlsx, the 2025–2026 Odoo
  Implementation Pricing Strategy PDF) contain desk values and
  supplier pricing. Excluded.
- **Root watermark masters** — `water mark (1).png` through
  `water mark (18).png` at the repo root are raw watermark
  masters. The desk-controlled renderer uses bundled base64 or
  Google Fonts at render time. Excluded.
- **The Playfair_Display cache** — the directory at the repo root
  is a font cache. Excluded.
- **The `_SCAFFOLD/` directory at the repo root** — moved to
  `plugins/sgc-proposal-engine/workspace-bootstrap/`. The two real
  client folders stay in the repo root as historical.

## What an SDR does on first run

1. **Get the SDR plugin** — your Den admin has assigned
   `sgc-proposal-engine` to you. The plugin's six skills
   (`proposal-intake`, `subscription-pricing`, `proposal-drafting`,
   `contract-assembly`, `approval-gate`, `signature-dispatch`) are
   now available.

2. **Read the README** — `plugins/sgc-proposal-engine/README.md`.
   It explains what's in the plugin and what's not, and why pricing
   content is desk-owned and local edits are overwritten on sync.

3. **Read the skills** — each skill's `SKILL.md` body has a
   "Position in step gate" section that names the previous and next
   step and the gate that forbids out-of-order invocation. Start
   with `proposal-intake`.

4. **Run `init-workspace.sh`** for your first new client. The
   script creates `<cwd>/sgc-proposals/<CLIENT-CODE>/` from the
   bootstrap. Don't copy a peer's folder.

5. **Use the tiered question bank** — the bank is at
   `knowledge/question-bank.yaml` and is read by
   `proposal-intake`. Tier 0 blocks pricing; Tier 1 blocks issue;
   Tier 2 forces a conservative risk band default.

6. **The fact-ledger confirmation step is where fabrication gets
   caught** — `proposal-intake` step 6. Every fact must trace to
   `sdr` / `document:<file>#<loc>` / `client-words`. Confirm the
   ledger with the SDR before drafting starts.

7. **The verbal-promises question is mandatory** — `t1_verbal_promises`
   has `unknown_ok: false`. "None" is a valid, complete answer;
   silence is not. Log every answer, including "none".

8. **The approval-gate produces a packet and stops** — it does
   not draft the covering email, does not create an envelope, does
   not pre-fill Zoho Sign. It waits for a recorded decision from
   `Ali Asghar Teli Muhammad Iqbal Teli`. The decision lands in
   `05-approval/approval-record.yaml` and binds to one exact
   artifact via SHA-256.

9. **The signature-dispatch refuses to send without a valid
   approval record (G53)** — and refuses to send with a stale
   one. Any change to the HTML or PDF, any figure change, any term
   or cadence change, any clause substitution, or any new
   concession voids the existing approval. Re-approval is a new
   record, never an edit of the old one.

10. **If you find a defect in a redaction** — open an issue against
    the desk plugin's `redacted-derivative-release` skill. Don't
    edit the derivative locally; the next sync will revert your
    change.

## What an approver does on first run

1. **Get the desk plugin** — your Den admin has assigned
   `sgc-commercial-desk` to you. The plugin's five skills
   (`walk-away-authoring`, `deal-card-review`,
   `published-floor-authoring`, `redacted-derivative-release`,
   `signature-handler-monitor`) are now available.

2. **You are the sole approver** — `Ali Asghar Teli Muhammad Iqbal
   Teli`. No delegation, no alternate, no "approved by agent on
   behalf of." The approval record must name you exactly.

3. **The deal-card review is where you ratify or return** — the
   desk's `walk-away-authoring` produces the per-deal walk-away
   card with the desk-only figures (CTS, internal build cost,
   margin floor, peak cash exposure, reservation pricing). Your
   `deal-card-review` skill reads the deal card, the exposure
   calculation, and the gate report together. The 10-item
   checklist in the skill body is the canonical review process.

4. **The published-floor table is yours** — the
   `published-floor-authoring` skill authors and maintains the
   `published-floor-table.yaml` consumed by the SDR plugin's G42
   guardrail. The desk may tighten any cell by re-issuing the file
   with a version bump.

5. **The redacted derivatives are yours** — the
   `redacted-derivative-release` skill cuts the SDR-safe
   derivatives and verifies the diff gate. Re-cut whenever a desk
   original changes.

6. **The signature pipeline is yours to monitor** — the
   `signature-handler-monitor` skill watches the webhook handler,
   alerts on G46–G52 anomalies, and reconciles
   `pending-odoo-writes.yaml` when `sgc_crm_fields` is deployed.

## What changes for the SDR team

- **The intake flow is the same** — the tiered question bank, the
  fact-ledger confirmation, the verbal-promises question, the
  fabrication prohibition — all unchanged. They live in
  `knowledge/` and the skills read them verbatim.

- **The pricing work is the same** — but the desk-only figures
  (CTS, internal build cost, margin floor, peak cash exposure,
  reservation pricing) are now in the desk plugin. The SDR enters
  the deal; the desk computes and returns the desk-side values
  for the worksheet.

- **The drafting flow is the same** — 13 sections, verbatim
  clause-library text, no paraphrasing, no fabricated figures.

- **The contract assembly is the same** — the MSA & SLA v2026.08,
  the Order Form Appendix I, the consistency map across proposal
  ↔ MSA ↔ Order Form.

- **The approval gate is new** — every deal must produce a valid
  `approval-record.yaml` before any envelope is created. The
  approval record binds the approver's authority to one exact
  artifact via SHA-256. Re-approval is a new record, never an
  edit of the old one.

- **The signature dispatch is new** — every envelope must be
  preflighted against G53 (no envelope without a valid approval
  record). The Zoho Sign two-step flow is the same; the G47 HMAC
  verification, G48 idempotency, G49 Won-requires-both-parties,
  G50 immutability, G51 invoice-as-draft, and G52 no-secrets
  guardrails are all unchanged.

## What changes for the desk

- **The desk plugin exists** — `sgc-commercial-desk`. The
  approver is the only person who runs its skills.

- **The desk's redacted derivatives are the SDR plugin's
  redaction** — the `redacted-derivative-release` skill is the
  only authorised writer of the SDR plugin's redacted files. The
  diff gate (`plugins/sgc-proposal-engine/ci/diff-redacted-derivatives.py`)
  runs on every commit.

- **The published-floor table is the SDR plugin's floor** — the
  `published-floor-authoring` skill authors and maintains
  `published-floor-table.yaml`. The desk may tighten any cell by
  re-issuing the file with a version bump. The G42 guardrail
  cross-checks every proposed subscription against the table
  before producing the approval packet.

- **The Zoho Sign handler is in the SRE repo** — the desk's
  `signature-handler-monitor` skill reads handler logs and Odoo
  state over a Den-managed MCP connection. The handler is not in
  the plugin.
