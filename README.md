# SGC Proposal Engine

A layered repository for building Odoo subscription proposals for SGC
TECH AI's UAE real estate brokerage clients — commercially defensible,
cash-risk aware, and unable to lose money if the gates are respected.

## Start here

Read `AGENTS.md` in full before touching anything. New SDRs: follow
`05-ops/onboarding-new-sdr.md`.

## The three-number model (for a new SDR, in one read)

Every proposal reduces to three numbers, computed in order.

**Number 1 — Cost to Serve.** What it costs SGC every month to keep this
client running: licences (zero on Community edition, the default),
hosting, tooling, support labour, account management. Multiply by 1.25 —
that's the platform floor. The recurring subscription price must never
sit below it.

**Number 2 — Build Value.** The one-time cost of implementation: hours
from the work-package catalogue, times a rate that must exist on the rate
card, plus project management and contingency loading. This is what the
client eventually pays for, whether upfront or over time.

**Number 3 — Financing Uplift.** If the client doesn't pay the full build
value at kickoff, the deferred portion carries a disclosed financing
uplift, recovered through the subscription over the term. Settling in
full at kickoff removes this number entirely.

Assemble: mobilisation (33% of build value, by default) plus a monthly
subscription of platform floor plus recovery. Two options only —
mobilisation-paid or nothing else; zero-upfront is currently withdrawn.
Every deal runs through 41 gates before it can be drafted. If one fails,
you reduce scope — you never discount past it.

## Why it's laid out this way

Drift is the enemy: a copied rate card that gets edited becomes three
different truths within months. `00-knowledge/` is read-only and single-
sourced; `02-clients/` references it, never duplicates it. See
`00-knowledge/failure-modes/known-defects.md` for what happens when this
discipline slips — twenty defects, with the arithmetic, from a real
revision history.

## Layout

| Layer | Who writes | Purpose |
|---|---|---|
| `00-knowledge/` | Commercial Desk only | Every rate, gate, and clause |
| `01-templates/` | Commercial Desk only | Structure and prose skeletons |
| `02-clients/` | SDR + agent | Deal execution, `05-issued/` immutable |
| `03-library/` | SDR, reviewed | Shared craft |
| `04-governance/` | Sales leadership | Approval authority |
| `05-ops/` | Commercial Desk | How to run the repository |
| `06-brand/` | Commercial Desk only | Visual identity, entity facts |
| `07-protection/` | Commercial Desk + Finance | Exposure limits, walk-away pricing |

## Live examples

`02-clients/VGE-vongeyern-realestate/` — v1, a clean 12-user smb build.
`02-clients/MRD-meridianview-realty/` — v2, a 5-user Community-edition
build whose first two revisions were retracted for documented defects,
corrected in Rev3. Read the second one to see the gates catch a real
failure pattern, not just pass a clean deal.

## Starting a new deal

Copy `02-clients/_SCAFFOLD/` and follow
`00-knowledge/runbook/subscription-proposal-runbook.md` from §1.
