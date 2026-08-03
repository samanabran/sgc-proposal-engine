<!--
Use to retract an issued revision that was sent with an error — e.g. a
number that didn't match the worksheet, a wrong clause version. Never
silently edit a 05-issued/ folder — see known-defects.md #5. Issue this
notice, then issue a corrected revision through the normal runbook sequence.
-->

Subject: Correction — [Proposal ref] [Revision N]

Dear [Decision maker],

We're writing to flag an error in [Proposal ref] [Revision N], sent
[date]. [One sentence, plain language: what was wrong — e.g. "The support
tier pricing in §11 did not match the commercial summary in §10."]

Please disregard [Revision N]. A corrected version, [Revision N+1], is
attached. [State explicitly what changed, if the correction affects any
commercial figure the client may have already noted.]

We apologize for the inconvenience and appreciate your patience. Happy to
walk through the correction on a call if useful.

Best regards,
[SDR name]
SGC TECH AI

---
Internal note (do not send): log this correction in
02-clients/{client}/manifest.yaml under the superseded revision's `notes`
field, and in 04-governance/review-log.md.
