# Agent Operating Contract

Read this file before touching any file in this repository. It is the
operating contract for any agent (or human) drafting a proposal here. It
overrides default behavior — follow it exactly.

## Start here for any new client request (mandatory, before anything else)

Before the load order below, before `00-knowledge/PRECEDENCE.md`, before
anything else in this repository: read `09-agent/step-gate.md`,
`09-agent/fabrication-rules.md`, and `09-agent/intake-interview.md`, in
that order. An SDR's request — however vague — must go through the
intake/orchestration layer in `09-agent/` before a single fact is treated
as known. The load order below still governs the drafting phase itself
once intake is complete; `09-agent/` governs everything before that phase
is allowed to start.

## Load order (mandatory)

1. `00-knowledge/PRECEDENCE.md`
2. `00-knowledge/runbook/subscription-proposal-runbook.md`
3. `00-knowledge/pricing/*.yaml`
4. `00-knowledge/commercial-rules/*`
5. `07-protection/doctrine.md`
6. `00-knowledge/market-data/vertical-notes/` for the client's vertical
7. The client's `00-intake/client-brief.yaml`

Do not draft a single line of client-facing prose before all seven have
been read.

## Absolute rules

- **NEVER** write to `00-knowledge/`, `01-templates/`, or `06-brand/`. If a
  rate, module, hour figure, clause, or brand token doesn't exist, that is
  an escalation — log it in the client's `manifest.yaml` under
  `escalations` and stop.
- **NEVER** invent a rate, hour figure, or percentage. Every number in a
  proposal must trace to a value in `00-knowledge/pricing/*.yaml`.
- **NEVER** edit anything inside a client's `05-issued/` folder once a
  revision has been sent. Issue a new revision instead.
- **NEVER** discount the recovery portion of a subscription (G11) —
  discounts apply to the platform portion only.
- **NEVER** present a payment cadence to a client without running the
  margin-floor ceiling calculation (G12) — a cadence table value is a
  ceiling, not an entitlement.
- **NEVER** draft a payment, security, or guarantee clause outside the
  clause library — see `00-knowledge/clause-library/`.
- **NEVER** state or imply a tax registration status SGC does not hold
  (G35). As of this version, SGC is **not** VAT-registered and holds no
  TRN — see `pricing/policy.yaml: vat`.
- **NEVER** describe Odoo Community as Enterprise, in writing or verbally
  (G36) — see `pricing/editions.yaml`.
- **ALWAYS** produce the walk-away deal card
  (`07-protection/walkaway/deal-card.template.md`) before any pricing
  conversation with the client (G22).
- **ALWAYS** complete `02-calc/pricing-worksheet.yaml` in full before
  drafting any prose.
- **ALWAYS** compute all three exposures — contractual, cash, economic —
  for every option in the worksheet (G21, see
  `07-protection/exposure/exposure-model.md`).
- **ALWAYS** write `02-calc/gate-report.md` covering all 41 gates. If any
  gate fails, **STOP** and escalate — do not discount around it.
- **ALWAYS** pin `knowledge_version_used` in the client's `manifest.yaml`.
- Tax, VAT, and legal wording must be copied verbatim from
  `00-knowledge/clause-library/`. Any clause flagged
  `requires_counsel_review: true` is drafted for review, not issued as
  final, until a human reviewer signs off.

## Sequence

```
intake → risk assessment → calc → exposure → gate check →
walk-away card → draft → QA checklist → brand QA → human review → issue
```

Refuse to skip the calc step. Prose without a passing gate report is not
a proposal.

## On uncertainty

Reduce scope, never price. Log an escalation in `manifest.yaml`. See
`00-knowledge/failure-modes/known-defects.md` for what happens when this
rule is skipped.

## Access model

| Layer | Who writes | Agents may |
|---|---|---|
| `00-knowledge/` | Commercial Desk only | Read only |
| `01-templates/` | Commercial Desk only | Read only |
| `02-clients/<client>/` | SDR + agent | Read + write, except `05-issued/` |
| `03-library/` | Any SDR, reviewed | Append, via review |
| `04-governance/` | Sales leadership | Read only |
| `05-ops/` | Commercial Desk | Read only |
| `06-brand/` | Commercial Desk only | Read only |
| `07-protection/` | Commercial Desk + Finance | Read only |
| `08-contracts/` | Commercial Desk only | Read only, except a per-deal consistency map, which is agent-writable like `02-clients/` |
| `09-agent/` | Commercial Desk only | Read only |

See `04-governance/access-model.md` for the full rationale.

## Tools

**validate.py** — gate enforcement (18 checks):
```
python 05-ops/validate.py 02-clients/{client}/
```
Exit 0 = clean (all checks pass, or only the expected entity-resolution blocker).
Exit 1 = real failure. Exit 2 = usage error. Requires PyYAML: `pip install pyyaml`.

## Skill

The `sgc-proposal-engine` skill auto-loads from `~/.config/opencode/skills/`
whenever proposal-related keywords are detected. It embeds the full pipeline
contract and runbook. The skill and this AGENTS.md are kept in sync — if one
diverges, treat this file as the source of truth and flag the discrepancy.
