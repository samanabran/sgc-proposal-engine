# SGC Proposal Engine

A layered repository for building Odoo/ERP subscription (and project /
retainer) proposals for SGC TECH AI's UAE and GCC clients, with a strict
separation between pricing truth, document structure, and deal execution.

## Start here

- **If you're an agent or SDR about to build a proposal**: read
  `AGENTS.md` first, in full. It is the operating contract for this
  repository and overrides default behavior.
- **If you're a new SDR**: follow `05-ops/onboarding-new-sdr.md`.
- **If you're the Commercial Desk maintaining pricing**: your changes go
  in `00-knowledge/` and `01-templates/` only, logged in `CHANGELOG.md`.

## Why it's laid out this way

The most common failure in a shared proposal repo is drift — someone
copies a rate card into a client folder, edits it, and six months later
three different rate cards exist. This repo is layered strictly to
prevent that: a read-only knowledge layer (`00-knowledge/`) that only the
Commercial Desk can change, a template layer (`01-templates/`) that
renders from it, and a per-client workspace (`02-clients/`) that
references upward and never duplicates. Change one rate, and every future
proposal inherits it.

The second design decision: an agent's arithmetic must be auditable and
separate from the prose. Every client folder keeps a `02-calc/` worksheet
showing ten gates (G1–G10) passing before a single word of client-facing
prose gets drafted. That's what makes a proposal defensible when a client
pushes back, and what lets a human reviewer check an SDR's — or an
agent's — work in minutes, not hours.

## Layout

| Layer | Who writes | Purpose |
|---|---|---|
| `00-knowledge/` | Commercial Desk only | Single source of truth for every rate, gate, and clause |
| `01-templates/` | Commercial Desk only | Structure and prose skeletons |
| `02-clients/` | SDR + agent | Deal execution — one folder per opportunity, `05-issued/` immutable once sent |
| `03-library/` | Any SDR, reviewed | Shared craft — worked examples, objection handling |
| `04-governance/` | Sales leadership | Approval authority and escalation |
| `05-ops/` | Commercial Desk | How to run the repository itself |

See `04-governance/access-model.md` for the full rationale, and
`00-knowledge/failure-modes/known-defects.md` for fifteen concrete
failures this structure exists to prevent.

## The live example

`02-clients/VGE-vongeyern-realestate/` is a real, worked-through deal — a
Dubai real estate brokerage moving from Rev1 (CRM + Sales) through Rev2
(added trust/commission accounting) to Rev3 (term extended for cash
flow), with a full passing gate report at every stage. Read it end to end
before running your first deal.

## Starting a new deal

Copy `02-clients/_SCAFFOLD/` — never a peer client's folder — and follow
`00-knowledge/runbook/subscription-proposal-runbook.md` from §1.
