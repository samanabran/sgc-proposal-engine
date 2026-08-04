# PUBLISHING — Den self-host + RBAC + sync steps

This document describes how to publish the two plugins to a self-hosted
Den, how to connect the repo for sync, and how to assign the plugins to
the right users.

## Two plugins, one marketplace

```
sgc-proposal-engine-marketplace
├── sgc-proposal-engine   (RBAC: all SDRs)
└── sgc-commercial-desk   (RBAC: Ali Asghar Teli Muhammad Iqbal Teli only)
```

`marketplace.json` lives at `.claude-plugin/marketplace.json` at the
repo root. Each plugin has its own `.claude-plugin/plugin.json` and
`plugin.json`.

## Self-host Den steps

The desk runs the following once. Repeat on every plugin version bump.

1. **Bundle the plugins.** Each plugin ships as the directory under
   `plugins/<plugin-name>/`. The bundle is the directory itself; no
   archive is needed.

2. **Publish to Den.**

   ```bash
   den marketplace add ./plugins/sgc-proposal-engine
   den marketplace add ./plugins/sgc-commercial-desk
   den marketplace publish --name sgc-proposal-engine-marketplace \
     --plugin ./plugins/sgc-proposal-engine \
     --plugin ./plugins/sgc-commercial-desk
   ```

3. **Verify the manifest.**

   ```bash
   den marketplace show sgc-proposal-engine-marketplace
   ```

   The output should list both plugins with their version, manifest
   path, and tags.

4. **Connect the repo for sync.** Configure the Den GitHub connector
   (this connector is **not yet configured** — see "Open RESOLVE
   fields" below). Once configured, every commit to a plugin path
   triggers the GitHub Actions workflow at
   `plugins/sgc-proposal-engine/ci/github-actions-workflow.yml`,
   which runs the diff gate, the forbidden-strings gate, the
   secrets gate, and the acceptance test. A failure on any of
   these blocks the release.

5. **Assign RBAC.** The Den admin runs:

   ```bash
   # SDR team assignment
   den rbac grant --plugin sgc-proposal-engine --role user --to group:sdr-team

   # Approver-only assignment
   den rbac grant --plugin sgc-commercial-desk --role user --to user:ali.iqbal
   ```

   `user:ali.iqbal` is the Den user account for `Ali Asghar Teli
   Muhammad Iqbal Teli`. RBAC is the confidentiality boundary; the
   plugin content is a subset of the desk's knowledge, redacted.

6. **Verify RBAC.** Confirm that an SDR account cannot load
   `sgc-commercial-desk` and that the approver can load both.

## Plugin content model

The plugin content is a **subset** of the desk's knowledge, redacted.
A user with both plugins sees the full knowledge; a user with only
the SDR plugin sees the redacted subset.

The plugin content is **read-only** and **version-synced**. Local
edits to any plugin file are overwritten on sync. The desk's
`redacted-derivative-release` skill is the only authorised writer of
the redacted derivatives.

A plugin upgrade **must never** touch anything under
`<workspace>/sgc-proposals/`. The upgrade ships a manifest hash;
if the on-disk `sgc-proposals/` tree differs from a fresh bootstrap
in any place other than `04-issued/` and `05-approval/`, the upgrade
logs a warning but **never overwrites**.

## Sync

The plugin content is in this repo. Den pulls from the repo on a
schedule. The plugin is published as a directory bundle; the
bundle is a snapshot of `plugins/<plugin-name>/` at the moment of
publish.

The plugin is consumed by Den users via `den plugin install
<plugin-name>`. The install is per-user; the plugin's content is
read-only on the installer's disk.

## Versioning protocol

Any rate, formula, gate, or clause change is a version bump with
the author recorded. The version is in `plugin.json`; the
`CHANGELOG.md` records the change.

Because SDRs receive updates by sync rather than copy, a bad
version reaches everyone at once. The CI gates run on every
commit to a plugin path; a failure blocks the release.

The semantic-version scheme:

- **Patch** — additions only (new cells in the published-floor table, new clause-library files).
- **Minor** — value changes within existing cells. A minor bump triggers a re-issue of the SDR plugin via sync.
- **Major** — schema change (e.g. a new axis on the published-floor table, a guardrail re-numbering). Breaks existing readers; the new version ships only after all readers are updated.

## Open RESOLVE fields (block issue)

The following items block the first go-live of the plugin. The desk
authorises each before any SDR receives the plugin.

1. **SGC licence authority and number — RESOLVED 2026-08-04**. The
   entity file `06-brand/entity/legal-identity.yaml` resolves to
   FZCO, IFZA (Dubai Integrated Economic Zones Authority, operating
   via IFZA — Dubai Silicon Oasis), Licence No. 45160, and the
   registered address at Maseed Building, Office No. 304, 119/12
   St, Al Rigga, Dubai. The root MSA
   `subscription_mode_sla_msa.htm` and the Order Form template have
   been updated to use the resolved values verbatim. Both plugin
   copies (`plugins/sgc-proposal-engine/contracts/msa-sla.html` and
   `plugins/sgc-commercial-desk/contracts/subscription_mode_sla_msa.htm`)
   mirror the resolution.

2. **Single registered address — RESOLVED 2026-08-04**. The
   registered address is Maseed Building, Office No. 304, 119/12
   St, Al Rigga, Dubai, United Arab Emirates. The drift documented in
   `06-brand/entity/legal-identity.yaml:28-43` is closed at both
   the entity file and the MSA / Order Form / signing block.

3. **Den deployment status** — whether Den is fully configured for
   this team's RBAC and sync is unknown. The plugin manifest is
   authored; deployment is a Den-side concern.

4. **GitHub connector configuration — WORKFLOW IN PLACE**. The
   GitHub Actions workflow is at
   `.github/workflows/plugin-gates.yml` (with a mirror at
   `plugins/sgc-proposal-engine/ci/github-actions-workflow.yml`).
   It runs the four gates (`diff-redacted-derivatives`,
   `forbidden-strings`, `secrets-scan`, `acceptance`) on every
   commit and PR to a plugin path; the combined
   `plugin-gate-status` job blocks the PR if any gate fails. The
   release job publishes to Den on a tag push, gated by the
   combined status. Configure the Den token as a repository
   secret (`DEN_TOKEN`) to enable automated publish; until then
   the release job skips and the desk runs
   `den marketplace publish` by hand.

5. **Countersignatory — RESOLVED 2026-08-04**. The SGC authorised
   signatory is `Ali Asghar Teli Muhammad Iqbal Teli`, Company
   Manager, per `06-brand/entity/legal-identity.yaml: contact.name`
   and `10-signature/send-protocol.md:88`. The Order Form template
   carries the signatory block with the resolved name, title,
   organisation, address, and contact. The G53 enforcement matches.

6. **Odoo `sgc_crm_fields` module** — not installed. The
   `signature-dispatch` skill degrades gracefully per the brief
   Part 3; the `signature-handler-monitor` skill reconciles when
   the module is deployed. The deal is not blocked. **See the
   install procedure below** ("`sgc_crm_fields` install").

## `sgc_crm_fields` install

The `sgc_crm_fields` module is a reference Odoo module skeleton at
`10-signature/sgc-crm-fields/`. It adds the 17 custom fields on
`crm.lead` that the Zoho Sign webhook handler writes to. The
`signature-dispatch` skill detects the module at runtime via an
`ir.model.fields` lookup on `crm.lead.x_envelope_id`. Until the
module is deployed, the handler appends intended writes to
`<workspace>/sgc-proposals/<CLIENT-CODE>/05-approval/pending-odoo-writes.yaml`
and the deal is not blocked.

### Pre-install verification

Before installing, confirm:

1. Target Odoo version is 17.0 or 18.0 (the manifest's field types are
   standard; `version` in `__manifest__.py` must be bumped to match).
2. The Odoo instance has `base`, `crm`, and `account` modules
   installed (the manifest's `depends` list).
3. The deployment user has access to Apps → Update Apps List and
   can install custom modules.

### Install steps

1. **Port the module** to the target Odoo addons directory
   (`/opt/odoo/addons/` on a typical install; or the Odoo
   addons path configured for the instance).

   ```bash
   cp -R 10-signature/sgc-crm-fields /opt/odoo/addons/
   ```

2. **Adjust `__manifest__.py`** if needed:
   - `version` — bump to match the target Odoo (e.g. `17.0.1.0.0`)
   - `depends` — `base`, `crm`, `account` (standard)
   - `license` — `LGPL-3` (matches SGC's Odoo Community usage)
   - `author` — `Scholarix Global Consultants FZCO`

3. **Update the Apps list** in the Odoo UI (Settings → Technical →
   Modules → Update Apps List) or via CLI:

   ```bash
   odoo-bin -u sgc_crm_fields -d <database>
   ```

4. **Install the module** (Apps → search "SGC CRM Fields" →
   Install). Or via CLI:

   ```bash
   odoo-bin -i sgc_crm_fields -d <database> --stop-after-init
   ```

5. **Verify the fields exist** in Developer mode → Settings →
   Technical → Database Structure → Models → `crm.lead` →
   Fields. The 17 fields listed in `knowledge/10-signature/send-protocol.md`
   and the `signature-dispatch` skill body should all be present.

6. **Configure the form view** (optional) — add the 17 fields to
   the Opportunity form view so SDRs see them. The fields are
   `copy=False` and most are `tracking=True`, so changes appear
   in the chatter.

### Runtime verification

After install, the `signature-dispatch` skill's `ir.model.fields`
lookup returns `count > 0`. The handler performs the native Odoo
write-back per `knowledge/10-signature/odoo-mapping.yaml` instead
of appending to `pending-odoo-writes.yaml`.

Test the integration end-to-end:

```bash
# From a deal's workspace folder
cd <workspace>/sgc-proposals/<CLIENT-CODE>/
ls 05-approval/pending-odoo-writes.yaml  # should not exist after a fresh send
# Or, for an existing pending-writes file, run the desk-side reconciler
den-plugin sgc-commercial-desk invoke skill signature-handler-monitor \
  --reconcile-pending-odoo-writes \
  --client <CLIENT-CODE>
```

### Reconciliation of pending-odoo-writes.yaml

When `sgc_crm_fields` is deployed, the desk-side
`signature-handler-monitor` skill reconciles. The procedure:

1. Iterate `<workspace>/sgc-proposals/<CLIENT-CODE>/05-approval/pending-odoo-writes.yaml`
   across all active client folders.
2. For each entry with `reconciliation.status: pending`:
   - Replay the Odoo write-back per the intended_writes.
   - Set `reconciliation.status: reconciled`,
     `reconciliation.reconciled_at: <timestamp>`,
     `reconciliation.reconciled_by: "Ali Asghar Teli Muhammad Iqbal Teli"`,
     `reconciliation.notes: "..."`.
3. After successful replay, archive the entry (move to
   `pending-odoo-writes.reconciled.yaml`) or delete it.
4. Notify the SDR of the reconciliation (the original "Day 3
   reminder" activity may have already been created manually).

### Field list (17 + 1 relation)

| Field | Type | Purpose |
|---|---|---|
| `x_envelope_id` | Char | Zoho Sign envelope ID |
| `x_signed_pdf_hash` | Char | SHA-256 of signed PDF |
| `x_frozen_pdf_hash` | Char | SHA-256 of frozen sent PDF |
| `x_sent_date` | Datetime | Envelope sent at |
| `x_completed_date` | Datetime | Fully executed at |
| `x_signing_actor_client` | Char | Client signatory |
| `x_signing_actor_sgc` | Char | SGC signatory |
| `x_decline_reason` | Text | Decline reason |
| `x_contract_term_months` | Integer | Initial term |
| `x_subscription_fee` | Float | Monthly total (AED) |
| `x_platform_fee` | Float | Platform portion (AED) |
| `x_recovery_fee` | Float | Recovery portion (AED) |
| `x_mobilisation_amount` | Float | One-off mobilisation (AED) |
| `x_cadence` | Selection | quarterly/monthly/annual in advance |
| `x_edition` | Selection | community / enterprise |
| `x_upgrade_policy` | Text | Upgrade policy text |
| `x_kickoff_date` | Date | Target kickoff |
| `x_invoice_id` | Many2one `account.move` | Draft mobilisation invoice (G51) |

7. **MSA signatory in-behalf-of relationship — RESOLVED 2026-08-04**.
   The MSA body, Order Form template, entity file, and the
   `guardrails-g42-g53.yaml` mirror all reflect:
   - Named approver (per trade licence): `Ali Asghar Teli Muhammad
     Iqbal Teli`, Company Manager.
   - Actual signer: `Renbran Anthony Madelo`, Founder & CEO,
     signing in behalf of the named approver per documented
     authority.
   The Zoho Sign envelope's `recipient_name` is `Renbran Anthony
   Madelo`; the audit certificate records the in-behalf-of
   relationship. The G53 preflight's `approver.name` check matches
   the actual signer; the legal authority of the named approver is
   documented in the MSA and the Order Form.

## How to verify the publish

After the publish step, run the acceptance test:

```bash
bash plugins/sgc-proposal-engine/tests/acceptance.sh
```

The output should report each of the 10 acceptance items with pass/fail.
A failure on any item blocks the publish.

## How to verify RBAC

1. As an SDR user, attempt to load the `sgc-commercial-desk` plugin
   (e.g. by invoking a skill from that plugin). The Den RBAC must
   refuse the load.

2. As the approver, load both plugins. Both must succeed.

3. As the approver, attempt to invoke a skill from
   `sgc-proposal-engine` (e.g. `proposal-intake`). The skill must
   invoke successfully and the agent must complete a synthetic deal
   end-to-end.

## Troubleshooting

- **Forbidden-strings gate fails** — the diff gate or the
  forbidden-strings gate found a desk-only value in the SDR plugin.
  Re-run `redacted-derivative-release` from the desk plugin to
  re-cut the derivative.

- **Diff gate fails** — the redacted derivative is no longer a
  strict subset of the desk original. Either the original moved
  (the desk must update the derivative) or the derivative
  accidentally added a line (the desk must re-cut).

- **Acceptance test fails** — see `tests/acceptance.sh` for the
  per-item output. The most common failures are:
  - G53 enforcement: the approval-record preflight rejects a
    valid record (G53 has a bug). Fix `signature-dispatch/SKILL.md`.
  - Out-of-order refusal: a skill does not refuse to run out of
    sequence. Fix the skill's "Position in step gate" section.
  - Forbidden string leak: a new desk-only string snuck into the
    SDR plugin. Fix the derivative and re-run the diff gate.
