# Naming Conventions

Formalizes the naming patterns used throughout this repository. Consistent
naming is what makes the gate-report audit trail, the review log, and
cross-references between files actually work — a proposal ref that doesn't
follow the pattern breaks every file that expects to parse or cite it.

## Client folder: `{PREFIX}-{slug}`

- **`PREFIX`**: a short, stable, uppercase identifier for the client —
  typically an abbreviation of the company name, 2–4 letters.
- **`slug`**: lowercase, hyphenated, descriptive of the company —
  usually the company name in lowercase with the industry appended if the
  company name alone is ambiguous.
- Location: `02-clients/{PREFIX}-{slug}/`.
- Always created by copying `02-clients/_SCAFFOLD/` — never a peer's
  folder (`known-defects.md #2`).

**Worked examples:**

- `VGE-vongeyern-realestate` — real, existing client folder. `VGE` from
  "Von Geyern" (the client name), `vongeyern-realestate` as the slug
  since the plain name alone doesn't convey the vertical.
- `ANC-anchorlogistics-3pl` — a fictional 3PL client named "Anchor
  Logistics"; `ANC` prefix, slug disambiguates the vertical.
- `BKF-brightkidsfurniture` — a fictional furniture retailer "Bright Kids
  Furniture"; `BKF` prefix, slug is the company name alone since it's
  already unambiguous.

## Proposal reference: `{PREFIX}-{YYYY}-{MODEL}-{NN}_Rev{N}`

- **`PREFIX`**: same client prefix as the folder.
- **`YYYY`**: four-digit year the proposal was first drafted.
- **`MODEL`**: one of `SUB` (subscription), `PRJ` (fixed project), `RET`
  (retainer) — see below.
- **`NN`**: two-digit sequence number, `01`, `02`, ... — increments per
  *distinct proposal* to the same client in the same year (a second,
  unrelated proposal to an existing client, not a revision of the first).
- **`_Rev{N}`**: revision number, starting at `Rev1` for the first issued
  version, incrementing on every subsequent issue. Never reused, never
  decremented — a correction to `Rev1` becomes `Rev2`, not a rewritten
  `Rev1` (`AGENTS.md`; `known-defects.md #5`).
- Location as a draft: `02-clients/{client}/03-draft/{PROPOSAL-REF}_RevN/`.
  Once approved and sent: `02-clients/{client}/05-issued/{PROPOSAL-REF}_RevN/`
  (immutable from that point).

**Worked examples:**

- `VGE-2026-SUB-01_Rev1` and `VGE-2026-SUB-01_Rev2` — real, existing,
  both in `05-issued/`; `VGE-2026-SUB-01_Rev3` is the current draft, in
  `03-draft/`. Same proposal (`01`), three revisions.
- `ANC-2026-PRJ-01_Rev1` — a fictional first fixed-project proposal to
  Anchor Logistics in 2026.
- `VGE-2027-SUB-02_Rev1` — a fictional *second, distinct* subscription
  proposal to the same Von Geyern client, in a later year — `02`
  increments because it's a new proposal, not a revision of `01`.

## Model codes

| Code | Model | Assembly pattern |
|---|---|---|
| `SUB` | Subscription | Mobilisation + recurring monthly subscription, two options (with/without mobilisation) — `runbook` §5 |
| `PRJ` | Fixed project | Single fixed fee = `build_value_aed`, typically 40/40/20 staged payment — `runbook` §5 |
| `RET` | Retainer | Monthly retainer sized from `support-training.yaml` tiers + capped usage pool, no mobilisation line — `runbook` §5 |

## Calc file

Always named `pricing-worksheet.yaml`, always at
`02-clients/{client}/02-calc/pricing-worksheet.yaml` — one worksheet per
client folder, rebuilt (not appended to) for each new proposal ref within
that client. Never rename it, never version it in the filename (`-v2`,
`-final`, etc.) — the worksheet's own `knowledge_version_used` field is
the version record, and the proposal ref tracks which proposal it fed.

**Worked example**: `02-clients/VGE-vongeyern-realestate/02-calc/
pricing-worksheet.yaml` — same filename regardless of which revision or
proposal it's currently supporting.

## Knowledge version

Semver (`MAJOR.MINOR.PATCH`, or the `MAJOR.MINOR` form seen in
`policy.yaml: version: 1.0`) recorded in `CHANGELOG.md` under a heading
naming the layer and version, e.g. `## pricing v1.0 — 2026-08-03`. Every
change to `00-knowledge/` or `01-templates/` gets a `CHANGELOG.md` entry
in the same commit as the change — never a silent edit. Client worksheets
pin the version active when built (`manifest.yaml: knowledge_version_used`)
so a later bump never silently revalues an in-flight proposal
(`known-defects.md #14`).

**Worked examples:**

- `## pricing v1.0 — 2026-08-03` — real, existing, the initial seed.
- `## pricing v1.1 — 2026-09-15` — fictional future entry, e.g. a rate-card
  revision.
- A worksheet built while `v1.0` is current records
  `knowledge_version_used: "1.0"` in that client's `manifest.yaml`,
  regardless of what version is current by the time the deal closes.
