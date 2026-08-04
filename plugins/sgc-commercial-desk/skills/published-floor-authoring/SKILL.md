---
name: published-floor-authoring
description: Desk-only skill. Authors and maintains the published-floor table consumed by the SDR plugin's G42 guardrail.
version: 1.0.0
owner: Commercial Desk
position: desk-side; runs whenever the floor table needs authoring, re-issue, or cell-tightening
---

# published-floor-authoring

The desk's authoring skill for the published-floor table. The SDR
plugin treats the table as read-only; the desk authors and re-issues
it.

## When to use

- Trigger phrases: "set the published floor", "tighten a floor cell", "add a cell to the table", "re-issue the floor table", "what's the published floor for (users, edition, term, cadence)", "publish a new floor version".

If the floor needs to be lowered for a specific deal (rare, requires
joint sign-off), this skill lowers it as a one-cell exception and
emits a `RESOLVE:` for the SDR's `subscription-pricing`. If the floor
needs a permanent re-issue, this skill bumps the version and
publishes a new file.

## Position in the workflow

- The skill runs in the desk plugin only. The SDR plugin never invokes it.
- The output is `plugins/sgc-proposal-engine/knowledge/published-floor-table.yaml` (mirror copy in the desk plugin) and the corresponding `plugins/sgc-commercial-desk/knowledge/published-floor-table.yaml`.
- A new version of the floor table triggers a plugin version bump per the versioning protocol.

## Bundled knowledge files to read, in order

1. `knowledge/policy.yaml` (full, desk-only) — segments, gates (min_gross_margin 0.30, target_gross_margin 0.35, default_mobilisation_pct 0.33, cash_positive_within_days 30, min_cadence quarterly_in_advance, absolute_margin_floor 0.25)
2. `knowledge/hosting.yaml` (full) — list prices
3. `knowledge/payment-plans.yaml` (full) — cadence table, hard_caps
4. `knowledge/07-protection/walkaway/reservation-pricing.md` — desk floor formula
5. `knowledge/07-protection/exposure/portfolio-limits.yaml` — runway target_months
6. `knowledge/04-governance/approval-matrix.md` — sign-off levels
7. The current `plugins/sgc-proposal-engine/knowledge/published-floor-table.yaml` (the version the SDR plugin is reading)

## What it writes, where

- `plugins/sgc-commercial-desk/knowledge/published-floor-table.yaml` (canonical)
- `plugins/sgc-proposal-engine/knowledge/published-floor-table.yaml` (mirror; same content, desk pushes via sync)

The skill is the only authorised writer of the SDR plugin's
`published-floor-table.yaml`. The SDR plugin sees the file as
read-only.

## What it refuses

- **Lowering a floor below the desk's reservation price** — the published floor is the desk's *padded* minimum, not the desk's true floor. Lowering a cell to the reservation price strips the padding and silently transfers margin risk to SGC. Cite G42.
- **Lowering a cell without founder + Commercial Desk joint sign-off** — cell-lowering (not just a temporary deal-specific exception) requires joint sign-off per `approval-matrix.md`. Cite the matrix.
- **Removing a cell** — refuses to remove a cell that has been used in any prior deal. The cell becomes deprecated (no new quotes against it) but stays in the table for audit.
- **Re-issue without a version bump** — refuses to publish a new file at the same version. The schema is stable across minor versions; only additions are allowed in patch releases.
- **Pushing a change that fails the diff gate** — refuses to push a change that introduces any forbidden string or removes any required key. Cite `plugins/sgc-proposal-engine/ci/diff-redacted-derivatives.py` and the `DISTRIBUTION-MANIFEST.md` forbidden-strings list.

## How the desk authors a cell

For each (users, edition, term_months, cadence) cell, the floor AED/mo must be:

1. **Above the desk's reservation price for the same cell** — the reservation price is `revenue_floor(target_gross_margin=0.35)` per `07-protection/walkaway/reservation-pricing.md`. The published floor must be ≥ the reservation price; otherwise the desk is publishing a number below its own floor.
2. **Above the absolute margin floor when worst-case concessions are applied** — the desk applies G31's worst-case calculation (max concessions + max guarantee credit) and verifies the cell is still ≥ 25% margin.
3. **Padded for SDR negotiation room** — the desk adds a padding factor to the reservation price so the SDR can discount within the published cadences and the ceiling calculation (G12) still binds tighter than the table value. Padding is the desk's choice; the SDR never sees the padding.
4. **Consistent with the published cadences** — the cell is consistent with `payment-plans.yaml: cadences` (the platform_adj_pct is a ceiling under G12, not an entitlement).

## What this skill does NOT do

- It does not compute the per-deal margin floor for an in-flight deal. The desk's `walk-away-authoring` does that.
- It does not invoke the SDR plugin's `approval-gate`. The SDR plugin invokes its own gate; the desk does not.
- It does not change the canonical MSA. The desk's `redacted-derivative-release` does.

## Versioning

The published-floor table follows the plugin's semantic-version protocol:

- **Patch** — additions only (new cells). The schema is stable.
- **Minor** — value changes within existing cells. The skill is the only authorised writer; a minor version triggers a plugin version bump on the SDR plugin.
- **Major** — schema change (e.g. new axis, new cadence). Breaks existing SDR plugin readers; the new version ships only after all readers are updated.

## Escalation path

- **A one-cell exception for a specific deal** — `RESOLVE: <cell> = <exception_aed>`. The exception is logged to the deal's `manifest.yaml: escalations` and ratified by the approver via `approval-gate`. The published table is unchanged.
- **A permanent re-issue** — bump the version, run the diff gate, push the new file via the desk's `redacted-derivative-release` skill, sync the SDR plugin. The desk's `PUBLISHING.md` describes the sync mechanism.
- **A cell that would require lowering below the reservation price** — refuse and route to founder + Commercial Desk for joint sign-off. If they sign, the cell is lowered with a `RESOLVE:` explaining the joint-sign-off and the specific deal it covers.
