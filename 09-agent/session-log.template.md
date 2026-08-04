<!--
Session Log — copy to 02-clients/{client}/00-intake/session-log.md
This is the audit trail that proves no fact was invented. It sits
alongside verbal-promises.md, client-brief.yaml, pricing-worksheet.yaml,
and gate-report.md as one of the artifacts 07-protection/evidence/
evidence-file-standard.md expects before go-live (G29).
-->

# Session Log — {PROPOSAL-REF}

**SDR:** {name}
**Date:** {YYYY-MM-DD}

## Original request (verbatim)

> {paste the SDR's original request exactly as typed, no paraphrasing}

## Questions asked and answers given

Every question from `question-bank.yaml`, in the order and batches actually
asked (per `intake-interview.md`), with the SDR's answer exactly as given.

### Tier 0

| Question ID | Question | Answer | Recorded as |
|---|---|---|---|
| t0_users_now | ... | ... | `sdr` / `unknown` / `document:...` |

### Tier 1

| Question ID | Question | Answer | Recorded as |
|---|---|---|---|

### Tier 2

| Question ID | Question | Answer | Recorded as |
|---|---|---|---|

## Confirmed fact ledger

The exact table printed and confirmed at `intake-interview.md` step 6 —
copy it here unchanged after SDR confirmation.

| Fact | Value | Origin |
|---|---|---|

## Unknowns

List every field still `unknown` after the one permitted retry
(`sufficiency-rules.yaml: shared_rules.ask_once`), and which escalation
applied (Tier 0 blocked pricing / Tier 1 became `RESOLVE:` / Tier 2 forced
a conservative risk-band default).

- {field}: {escalation applied}

## Defaults applied, and why

Any conservative default taken because of an incomplete Tier 2 field, per
`sufficiency-rules.yaml: tier_2.on_incomplete` — state the field, the
default applied, and the specific reasoning.

- {field}: {default applied} — {why}

## Gate results

Summary pointer to `02-calc/gate-report.md` for this revision — pass/fail
count, and any gate that failed and how it was resolved (scope reduction,
concession-ladder application) rather than discounted around.

- Gate report: `02-calc/gate-report.md`
- Result: {all 41 pass / N failed, resolved by ...}
- `validate.py` run: {date, exit code, RESULT summary}
