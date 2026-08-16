# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Not a software project. Governed document/knowledge pipeline for **SGC TECH AI**
(Scholarix Global Consultants FZCO) — generates Odoo-subscription proposals for
UAE real-estate brokerages. "Code" here is almost entirely Markdown/YAML content
plus one Python gate-checker (`05-ops/validate.py`) and small helper scripts
under `plugins/*/ci/` and `.opencode/skills/*/scripts/`. Treat every task as
executing a governed pipeline, not writing application code.

Two installable plugins ship from this one repo (`.claude-plugin/marketplace.json`):
- `sgc-proposal-engine` — SDR-facing, six skills, sanitized knowledge subset.
- `sgc-commercial-desk` — approver-only, five skills, full knowledge base.
`DISTRIBUTION-MANIFEST.md` classifies every file `sdr` / `desk` / `both` / `excluded`.

## Mandatory reading before ANY client-facing work

Read in this exact order before drafting a line of prose or touching pricing
(see `AGENTS.md` "Load order" and `.opencode/skills/sgc-proposal-engine/SKILL.md`):

1. `09-agent/step-gate.md`, `09-agent/fabrication-rules.md`, `09-agent/intake-interview.md` (before intake even starts)
2. `00-knowledge/PRECEDENCE.md` — conflict resolution order; **a ceiling is never an entitlement**
3. `00-knowledge/runbook/subscription-proposal-runbook.md` — the pipeline in full
4. `00-knowledge/pricing/*.yaml` — every number in a proposal must trace here
5. `00-knowledge/commercial-rules/*` — guardrails G1–G41
6. `07-protection/doctrine.md`
7. `00-knowledge/market-data/vertical-notes/` for the client's vertical
8. `<client>/00-intake/client-brief.yaml`

`AGENTS.md` is the authoritative operating contract and overrides default agent
behavior. Read it in full before any repo work.

## The pipeline (never skip a stage)

```
intake → risk assessment → calc → exposure → walk-away card → gate check (G1–G41) →
draft → QA / brand QA → human review → issue
```

Client folders: `02-clients/{PREFIX}-{slug}/`, always created by copying
`02-clients/_SCAFFOLD/` (never a peer client folder). Stage detail, exit
artifacts, and hard stops are fully specified in
`.opencode/skills/sgc-proposal-engine/SKILL.md` §4 — follow it exactly rather
than improvising stage order.

Proposal ref format: `{PREFIX}-{YYYY}-{MODEL}-{NN}_Rev{N}` (`MODEL` = `SUB`
subscription / `PRJ` fixed project / `RET` retainer). Full rules in
`05-ops/naming-conventions.md`.

## Validation — run before every human review and every issue

```
python 05-ops/validate.py 02-clients/{client}/
```

Exit 0 = clean. 18 checks (pricing traceability, all 41 gates evaluated, 25%
margin floor, cash-positive timing, VAT/entity/brand-token correctness,
forbidden-phrase scan, etc.) — see SKILL.md §6 for the full list. **Check 14**
(entity fields in `06-brand/entity/legal-identity.yaml`) is currently
`[BLOCKED — by design]` and still exits 0 — an administrative blocker on
*issuing*, not a commercial gate failure; escalate but don't treat as blocking
drafting/review.

## Absolute rules (from `AGENTS.md` — do not violate)

- **NEVER** write to `00-knowledge/`, `01-templates/`, or `06-brand/` — read-only
  to agents. Missing rate/module/hour/clause/brand token = escalate in the
  client's `manifest.yaml`, never invent or substitute.
- **NEVER** invent a rate, hour figure, or percentage — everything traces to
  `00-knowledge/pricing/*.yaml`; reject `forbidden_rates` (G9).
- **NEVER** edit inside a client's `05-issued/` once sent — issue a new revision.
- **NEVER** discount the recovery portion of a subscription (G11) — discounts
  apply to the platform portion only.
- **NEVER** present a payment cadence without running the G12 margin-floor
  ceiling calc.
- **NEVER** draft payment/security/guarantee clauses outside
  `00-knowledge/clause-library/` (verbatim, not paraphrased).
- **NEVER** state or imply SGC holds UAE VAT registration/TRN (G35) — it does not.
- **NEVER** call Odoo Community "Enterprise" (G36); never imply an iOS/Android
  app for Community.
- Per 2026-08-04 decision: the sales proposal body (§06, §10) stays silent on
  VAT status and Odoo edition unless the client/SDR raises it — but the
  MSA/Order Form (§A.9, §C.6) always states both accurately. Never silent there.
- **ALWAYS** produce the walk-away deal card before any pricing conversation (G22).
- **ALWAYS** compute all three exposures (contractual, cash, economic) per
  option (G21).
- **ALWAYS** write `02-calc/gate-report.md` covering all 41 gates; any failure
  → STOP and escalate/reduce scope, never discount around it.
- **ALWAYS** pin `knowledge_version_used` in `manifest.yaml`.
- On any uncertainty: reduce scope, never price on a guess; log an escalation.

## Repository layout

- `00-knowledge/` — pricing, commercial-rules (guardrails), clause-library
  (verbatim legal/tax text), market-data, runbook — desk-owned, read-only to agents
- `01-templates/` — proposal section templates (`_section-map.md` = §01–§13),
  intake, comms, QA checklists — read-only to agents
- `02-clients/` — per-client folders (`00-intake` → `02-calc` → `03-draft` →
  `04-review` → `05-issued`), plus `_SCAFFOLD` (the only thing ever copied to
  start a new client)
- `03-library/` — worked drafting examples
- `04-governance/` — access model, approval matrix, escalation triggers
- `05-ops/` — glossary, naming conventions, onboarding, `validate.py`
- `06-brand/` — entity facts, brand registry/tokens, styles — read-only to agents
- `07-protection/` — walk-away doctrine, exposure model, abort/monitoring
- `08-contracts/` — root MSA (canonical)
- `09-agent/` — step-gate, fabrication-rules, intake-interview, question-bank —
  read this before intake starts
- `10-signature/` — Zoho Sign integration (send-protocol, webhook, guardrails G46–G52)
- `plugins/` — the two installable Claude plugins, each with its own `ci/` gates
  (redacted-derivative diff check, forbidden-strings scan, secrets scan, acceptance tests)

## Company facts agents must get right

- **Not VAT-registered, no TRN.** Never "VAT inclusive/exempt" wording.
- **Odoo Community is the default edition**; "Enterprise" refers only to the
  Odoo edition, never a marketing tier. Top service tier is **Professional**.
- G32: every deal cash-positive within 30 days of Kickoff.
- G33: quarterly-in-advance minimum payment cadence.
- G34: mobilisation ≥33% of build value, covers any pre-paid third-party cost.
- Option B (zero-upfront mobilisation) is **withdrawn** — never offer it;
  exactly two payment options, never three.

## Human approval gate (G53)

Nothing reaches a client without a recorded approval decision from the named
approver (`06-brand/entity/legal-identity.yaml: contact.name`). The
`approval-gate` skill produces `05-approval/approval-request.md` and stops;
the approver writes `05-approval/approval-record.yaml` with a SHA-256 bound to
one exact artifact. `signature-dispatch` refuses to send without a valid,
unexpired, hash-matching record. Re-approval is always a new record, never an
edit of the old one.
