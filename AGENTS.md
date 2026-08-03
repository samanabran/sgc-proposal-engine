# Agent Operating Contract

Read this file before touching any file in this repository. It is the operating
contract for any agent (or human) drafting a proposal here. It overrides
default behavior — follow it exactly.

## Load order (mandatory)

1. `00-knowledge/runbook/subscription-proposal-runbook.md`
2. `00-knowledge/pricing/policy.yaml` + every file in `00-knowledge/pricing/*.yaml`
3. `00-knowledge/commercial-rules/`
4. `00-knowledge/market-data/vertical-notes/` for the client's vertical
5. The client's `00-intake/client-brief.yaml`

Do not draft a single line of client-facing prose before all five have been read.

## Absolute rules

- **NEVER** write to `00-knowledge/` or `01-templates/`. If a rate, module, hour
  figure, clause, or template doesn't exist, that is an escalation — log it in
  the client's `manifest.yaml` under `escalations` and stop. Do not improvise
  around the gap.
- **NEVER** invent a rate, hour figure, or percentage. Every number in a
  proposal must trace to a value in `00-knowledge/pricing/*.yaml`. If you
  cannot cite the source file and key, delete the number.
- **NEVER** edit anything inside a client's `05-issued/` folder once a revision
  has been sent. Issue a new revision (`_RevN+1`) instead. `05-issued/` is
  immutable.
- **ALWAYS** complete `02-calc/pricing-worksheet.yaml` in full before drafting
  any prose. Prose without a completed worksheet is not a proposal — it is a
  liability.
- **ALWAYS** write `02-calc/gate-report.md` after the worksheet. If any gate
  fails (see `commercial-rules/subscription-guardrails.md`, G1–G10), **STOP**
  and escalate in `manifest.yaml`. Do not discount your way around a failed
  gate — see "On uncertainty" below.
- **ALWAYS** pin `knowledge_version_used` in the client's `manifest.yaml` to
  the version in `CHANGELOG.md` that was active when the worksheet was built.
  If pricing changes later, existing worksheets are not silently revalued.
- **Tax, VAT, and legal wording** must be copied verbatim from
  `00-knowledge/clause-library/`. Never paraphrase a tax or legal clause. Flag
  every proposal containing one for human review before issue.
- Anything said aloud on a call is scope. Log verbal promises in the client's
  `00-intake/verbal-promises.md` the same day, and reflect them in the brief.

## Sequence

```
intake → calc → gate check → draft → QA checklist → human review → issue
```

Do not skip the calc step to "save time" on a simple-looking deal. There is no
such thing as a proposal without a passing gate report behind it.

## On uncertainty

When a gate fails, a rate is missing, or scope is ambiguous: **reduce scope,
never price.** Cutting scope to fit the client's budget is a legitimate sales
move. Cutting margin below the gate to fit the client's budget is not — it is
how six-month-old rate cards happen. Log the escalation in `manifest.yaml`
under `escalations` and route it to the Commercial Desk.

## Access model

| Layer | Who writes | Agents may |
|---|---|---|
| `00-knowledge/` | Commercial Desk only | Read only |
| `01-templates/` | Commercial Desk only | Read only |
| `02-clients/<client>/` | SDR + agent | Read + write, except `05-issued/` |
| `03-library/` | Any SDR, reviewed | Append, via review |
| `04-governance/` | Sales leadership | Read only |
| `05-ops/` | Commercial Desk | Read only |

See `04-governance/access-model.md` for the full rationale.
