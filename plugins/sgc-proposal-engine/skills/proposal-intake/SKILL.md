---
name: proposal-intake
description: Step 1 of the SDR proposal pipeline. Interrogates a vague SDR request, never improvises. Read this first whenever a request is anything less than a complete, sourced brief.
version: 1.0.0
owner: SDR
position: 1
---

# proposal-intake

The intake skill. The only skill that talks to the SDR.

## When to use

- An SDR types anything about a potential client — a name, a vertical, a request for a proposal, a one-liner.
- Trigger phrases: "draft a proposal for", "we have a new client", "quote this", "send me a proposal", "intake for", "new opportunity", anything that names a client or asks for a proposal.

If a more specific step (e.g. pricing on an existing client folder) is requested, route there instead.

## Position in step gate

Step 1 of 13. The fixed sequence:

```
intake → fact ledger confirmed → risk assessment → pricing worksheet →
payment-plan worksheet → exposure calculation → walk-away card →
gates G1–G41 → brand resolution → draft → consistency map → validate →
QA → PDF + hash → approval gate → envelope
```

This skill **refuses to run** if it is invoked after any step in the sequence has already been started. The skill's first action is to check `<workspace>/sgc-proposals/<CLIENT-CODE>/00-intake/client-brief.yaml` and refuse if it already exists with content from a prior skill — the SDR has re-opened an existing client, and that flow is not intake.

## Bundled knowledge files to read, in order

1. `knowledge/step-gate.md` — the 14-step non-skippable sequence
2. `knowledge/fabrication-rules.md` — the absolute prohibition
3. `knowledge/intake-interview.md` — the 6-step protocol
4. `knowledge/question-bank.yaml` — the tiered question bank
5. `knowledge/sufficiency-rules.yaml` — what blocks what
6. `knowledge/session-log.template.md` — the audit trail format

Read in this order. Never paraphrase or skip the protocol steps.

## What it writes, where

After SDR confirmation at step 6 of the protocol:

- `<workspace>/sgc-proposals/<CLIENT-CODE>/00-intake/client-brief.yaml` — the canonical brief
- `<workspace>/sgc-proposals/<CLIENT-CODE>/00-intake/verbal-promises.md` — the mandatory verbal-promises log (table format per `intake-interview.md` step 4)
- `<workspace>/sgc-proposals/<CLIENT-CODE>/00-intake/session-log.md` — copy of the session-log template with all Q&A, fact ledger, unknowns, defaults applied, and gate results

`<CLIENT-CODE>` is the PREFIX-slug per `05-ops/naming-conventions.md` (desk reference; for SDR use: `{VERTICAL-3LETTER}-{lowercase-slug}` where the slug is the client's trading name in lowercase, hyphenated, no spaces).

## What it refuses

- **Out-of-order invocation** — refuses if step 1 has already been run for this client, or any other step in the sequence is already in flight.
- **Skip requests** — if the SDR says "skip the tier", "just use a typical figure", "we'll fill that in later", "use the previous client's numbers" — refuse by name and cite `intake-interview.md:79-87` and `fabrication-rules.md`.
- **Plausible defaults** — never fills a missing fact with a representative example. The only permitted handling of a missing fact is `ask` (Tier 0) or `RESOLVE:` (Tier 1). Tier 2 may default conservatively, with mandatory disclosure in the deal card and gate report.
- **Pasted values without an origin tag** — every fact must trace to `sdr`, `document:<file>#<loc>`, or `client-words`. `unknown` is permitted only in the fact ledger and session log.
- **Insufficient Tier 0 closure** — refuses to allow `subscription-pricing` to run until every Tier 0 field is answered, escalated per `sufficiency-rules.yaml: tier_0`, or rejected as still-unknown.
- **Skipping the verbal-promises question** — `t1_verbal_promises` is the one question with `unknown_ok: false`. "None" is a valid, complete answer; silence is not.

## Escalation path

For each missing Tier 1 fact: emit `RESOLVE:` and write the field to the client brief and session log. The next skill (`subscription-pricing`) carries the `RESOLVE:` forward.

For three or more Tier 1 fields still `RESOLVE:` at the end of step 2 (fact ledger confirmed), emit one batched escalation in `<workspace>/sgc-proposals/<CLIENT-CODE>/00-intake/escalations.md` and refuse to proceed until the SDR resolves the field set.

For Tier 2 missing: apply the conservative risk-band default per `sufficiency-rules.yaml: tier_2.on_incomplete`. Disclosure is mandatory in `02-calc/deal-card.md` and `02-calc/gate-report.md`; the desk's `walk-away-authoring` skill will refuse to author a deal card without that disclosure.

For a vague request like "proposal for a Dubai brokerage, 8 users" — refuse to price. Route to step 1: ask the Tier 0 batch. The single most common refusal of this skill is "I cannot price this without answering the Tier 0 batch. Here are the nine questions. Please answer in one batch."

## The absolute rule

The agent must never generate a client name, contact name, user count, budget figure, pain point, quote, objection, incumbent system, or requirement that the SDR did not supply or that does not appear in an attached source document. Every client-attributed statement must trace to one of three origins: `sdr`, `document:<file>#<loc>`, `client-words`. Missing fact → ask, or emit `RESOLVE:`. Never a plausible default. (Source: `fabrication-rules.md:9-12`.)

## Acceptance check (self-test)

Before writing the three intake files, the skill must be able to answer YES to each:

1. Is the fact ledger printed and confirmed by the SDR per `intake-interview.md:58-77`?
2. Is every client-attributed fact origin-tagged?
3. Is the verbal-promises log populated (even if every row is `none`)?
4. Are Tier 0 fields all answered or escalated?
5. Are Tier 1 fields either answered or `RESOLVE:`-tagged with the placeholder in the file?

If any answer is NO, fix it before allowing the next skill to run.
