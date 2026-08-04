# Intake Interview Protocol

An SDR types something vague. This protocol interrogates, not improvises.
Read `fabrication-rules.md` first — nothing here overrides it. Questions
come from `question-bank.yaml`; blocking behavior comes from
`sufficiency-rules.yaml`.

Tone: brisk and specific. Never more than one batch of questions per turn.
Never ask for something already supplied.

## 1. Restate and confirm

Before asking anything else, restate what you understood from the SDR's
request in one short paragraph — client, vertical, rough scale, anything
already stated — and ask the SDR to confirm or correct it. Do not proceed
to Tier 0 until this is confirmed or corrected.

## 2. Tier 0 — single batch

Ask every unanswered Tier 0 question from `question-bank.yaml` as one
numbered batch, each with its one-line reason. Do not drip-feed one
question per turn. Skip any question whose field was already supplied in
the original request or a confirmed source document.

## 3. Accept "I don't know"

"I don't know" is a real answer. Record it as `unknown` in the fact ledger.
Do not ask the same question more than once more after the first "I don't
know" (see `sufficiency-rules.yaml: shared_rules.ask_once`). If still
unknown after that one retry, escalate per the field's tier: Tier 0 blocks
pricing outright; Tier 1 becomes a `RESOLVE:` placeholder; Tier 2 defaults
the risk band one step more conservative.

## 4. Tier 1 — second batch

Only after Tier 0 is fully closed (every field answered or explicitly
escalated per step 3), ask the Tier 1 batch. This batch always includes
the verbal-promises question verbatim:

> "Has anyone at SGC told this client anything about price, timeline,
> inclusions, discounts, or exclusivity that isn't in writing?"

Log every answer — including "none" — to `00-intake/verbal-promises.md`,
in the table format already in use on both live clients:
`| Date | Promised by | Item | Classification | Where it's reflected |`,
classification always `PRICED` / `DEFERRED` / `EXCLUDED`. This question is
mandatory and cannot be skipped, regardless of how confident the SDR is
that nothing was promised.

## 5. Tier 2 — last batch

Ask the Tier 2 batch only after Tier 1 is closed. State plainly, before
asking: "Skipping these means the risk assessment defaults to the more
conservative band, and the gate report and deal card will say so." Do not
frame this as optional filler — it is a real trade-off the SDR is making
by skipping.

## 6. Fact ledger — print and confirm

Before drafting anything, print the fact ledger: every fact gathered
across all three tiers, its value, and its origin tag from
`fabrication-rules.md`:

| Fact | Value | Origin |
|---|---|---|
| e.g. `scale.users_now` | 8 | `sdr` |
| e.g. `client.legal_name` | unknown | `unknown` |
| e.g. `scope_signals.incumbent_system` | "SAP Business One" | `document:call-transcript-2026-08-03.md#00:14:22` |

The SDR confirms this ledger — correcting any misattributed origin or
misheard value — before drafting starts. **This confirmation step is where
fabrication gets caught**: any fact the agent cannot place in this table
with a real origin has no business being anywhere in the draft.

Once confirmed, write the ledger into `00-intake/session-log.md` per
`session-log.template.md`, and proceed to `step-gate.md`'s next step (risk
assessment) — never directly to drafting.

## Refusing a skip request

If the SDR asks to skip a tier or the fact-ledger confirmation, refuse and
name the specific rule that forbids it (`sufficiency-rules.yaml` for tiers,
this file's step 6 for the ledger, `fabrication-rules.md` for anything
resembling "just use a typical figure"). This mirrors the tone of
`AGENTS.md`: "Refuse to skip the calc step. Prose without a passing gate
report is not a proposal." — the same discipline applies one step earlier,
at intake.
