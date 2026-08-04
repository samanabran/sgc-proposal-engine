# Fabrication Rules — the absolute prohibition

Read this before `intake-interview.md` or any other file in this folder.
Nothing downstream — no sufficiency rule, no step-gate, no SDR request to
"just move faster" — overrides what's below.

## The absolute rule

The agent must never generate a client name, contact name, user count,
budget figure, pain point, quote, objection, incumbent system, or
requirement that the SDR did not supply or that does not appear in an
attached source document.

Every client-attributed statement in a proposal must trace to exactly one
of three origins, recorded per statement:

| Origin tag | Meaning |
|---|---|
| `sdr` | An intake answer the SDR gave directly, logged in `00-intake/session-log.md` |
| `document:<file>#<location>` | An attached source document, with a precise location (page, section, transcript timestamp, or CRM field name) — not just a filename |
| `client-words` | The client's own written or transcribed words, quoted or closely paraphrased, sourced to a named transcript/email/message |

A fourth value, `unknown`, exists **only** inside the fact ledger
(`intake-interview.md` step 6) and `session-log.md`. It is never permitted
in a drafted proposal, worksheet, or any client-facing artifact.

## What to do when a fact is missing

The only two permitted outputs:

1. **Ask the SDR** — via the tiered interview (`question-bank.yaml`,
   `intake-interview.md`), following the "ask once" rule in
   `sufficiency-rules.yaml`.
2. **Emit a `RESOLVE:` placeholder** — the same token this repo already
   uses in `06-brand/entity/legal-identity.yaml` and checked by
   `05-ops/validate.py: check_14_entity`. This file does not invent a new
   token; it extends the existing one from "unresolved SGC entity fields"
   to **any** unresolved client-attributed fact.

Never a plausible default. Never a representative example. Never "typical
for this segment." A number that is directionally reasonable but not
sourced is exactly as prohibited as one that is wrong.

## Why this exists — grounded in this repo's own history

`00-knowledge/failure-modes/known-defects.md` is the record of what
happens when this discipline slips:

- **Defect #20** — "AED 1.15 billion in client value," "104% Year-1 ROI,"
  "5.9-month payback" were presented as track record with no source, no
  client consent, and no basis found anywhere in the repository. This rule
  exists specifically so that class of statement can never be generated
  again, by construction rather than by review.
- **Defect #21** — a "don't invent numbers" instruction was once read
  narrowly, as governing only fabricated *market data*, and was used to
  justify leaving a known-wrong rate in place with just an inline comment.
  On review, that reading didn't hold: the instruction governs fabricating
  data of any kind, not preserving a value already known to be wrong. The
  lesson generalizes directly to this file's absolute rule — "don't
  fabricate" covers every client-attributed fact (a name, a pain point, an
  objection), not only pricing figures. A rule only a human might read
  before drafting is weaker than a rule the interview protocol and
  sufficiency gates enforce structurally — prefer the latter.
- **Defect #12** — two different registered addresses for the same entity
  were issued weeks apart, because nothing forced a single source of truth
  until `06-brand/entity/legal-identity.yaml` existed. The three-origin
  provenance rule above is the same fix, applied to every client-side fact
  instead of just SGC's own entity data.

## Demo and fixture data

- Demo/fixture data lives **only** under a folder whose name starts
  `DEMO-` (e.g. `02-clients/DEMO-<slug>/`).
- Every file inside a `DEMO-` folder carries a visible header marking it
  fictional, e.g.:
  ```
  <!-- FICTIONAL DATA — for demonstration/training only. Never a source
       for a real client build. See 09-agent/fabrication-rules.md. -->
  ```
- A `DEMO-` folder is **never** a valid input to a real client build. No
  fact in a real proposal may carry a `document:` origin that resolves to
  a path under `DEMO-`. `step-gate.md`'s fact-ledger checkpoint and
  `sufficiency-rules.yaml` both enforce this explicitly.

**Aside, not fixed by this task**: `03-library/worked-examples/
boutique-brokerage-5users-24mo.md` is fictional and says so in its own
text, but doesn't live under a `DEMO-` prefixed path. It predates this
convention. Worth a cheap rename in a future pass; not required for this
layer to function, since the rule above is what's enforced at intake time
going forward.

## Interaction with `05-ops/validate.py`

`validate.py` already separates two failure categories and reports them
separately, never conflated: gate failures (checks 1–13, 16–18 — commercial
soundness) and the entity-resolution blocker (check 14 — administrative,
expected to fail on a fictional or in-progress build). This file's
`RESOLVE:` usage for client-attributed facts is checked the same way: a
`RESOLVE` hit blocks `issue-ready`, but is not itself a gate failure. Don't
conflate the two categories when reporting status to an SDR or reviewer.
