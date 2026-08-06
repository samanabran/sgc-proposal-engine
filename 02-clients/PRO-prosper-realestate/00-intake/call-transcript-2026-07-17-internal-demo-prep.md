# Internal Demo-Prep Call — Prosper Intl Real Estate

**Date:** 2026-07-17 · **Source:** Otter.ai transcript ("Scholarix Global's
Meeting Notes_otter_ai (1)"), Scholarix internal team rehearsal
**Participants:** Speaker 1 (SGC consultant, demo lead), Speaker 2 ("John,"
SGC — being trained to co-present), Speaker 3/4 (brief interjections)
**Not present:** any Prosper representative — this is an internal rehearsal
ahead of a client demo, not a client call itself.

## Identification basis (flagged, not fully confirmed)

The transcript repeatedly references presenting to "Diane" and rehearsing
the questions to ask her about her challenges. No company name is stated in
the transcript itself. Identification as Prosper rests on:

- Prosper's CRM record (Lead 8407) names **Dian Sajulga** as the Operations
  contact, and `x_bant_authority` explicitly describes "Diane" as "the
  coordinator responsible for business operations and is the final
  decision-maker for this purchase" — matching phonetically and by role.
- The rehearsed demo flow (attendance check-in/check-out with mobile
  geolocation, payroll/WPS processing, AI-assisted lead/status reporting,
  role-based admin hierarchy) maps directly onto Prosper's own
  `x_bant_need` items logged in CRM: agent check-in/check-out, accounts
  integration incl. salary structure, ChatGPT/AI integration, multiple
  admins.
- No other open lead in this pipeline run has a contact plausibly matching
  "Diane."

This is a reasonable inference, not a confirmed fact — flagged the same way
this repo flags any unconfirmed intake input (see risk-assessment.yaml).

**Provenance upgraded 2026-08-06** — first independent external
corroboration found for any transcript in this four-client corpus.
Gmail search turned up two Otter.ai meeting-summary notification emails,
both dated 2026-07-17, to `scholarixglobal@gmail.com`: one snippet reads
"focused on Scholarix Global's system functionalities and addressing
client needs," the other "focused on demonstrating... system features,
particularly employee check[-in]..." — matching this file's own summary
(system walkthrough, attendance/check-in demo) precisely. This is
corroboration from a third-party system (Otter.ai's own automated
notification, surfaced via Gmail) independent of this repo's own
authored content — not another SGC document repeating the same claim.
See `HANDOVER.md` §8.7 for the full search record. Does not resolve the
identification-basis question above (still a reasonable inference, not a
confirmed client identity) — it confirms the meeting happened on this
date and covered these topics, which was not independently established
before.

## Summary

An internal rehearsal for a live product demo: the presenter (Speaker 1)
walks a colleague (Speaker 2, "John") through the exact flow planned for
Prosper's demo — ask about a challenge, then show the system solving it —
covering three of the client's own named pain points in order:

1. **Attendance** — mobile check-in/check-out with geolocation ("view in
   the map where I checked in"), red-dot notification indicator, admin vs.
   employee visibility rules (employees see their own leave/lateness only
   once payroll is processed, not the attendance module itself).
2. **Payroll** — attendance feeding directly into payroll computation,
   contract-based salary calculation, pay-slip generation, and WPS (Wage
   Protection System) bulk-submission file generation — explicitly framed
   as "very tough to explain," to be shown briefly rather than walked
   through step-by-step live with the client.
3. **AI capability** — the platform's built-in "SGC AI" chat assistant
   (natural-language queries against CRM data, e.g. "generate the lead
   status grouped by salesperson"), offered as evidence AI integration is
   "not an issue," alongside acknowledging ChatGPT-style integration would
   depend on the client's specific need.
4. **Admin hierarchy** — role-based permission setup (user vs.
   administrator, document-level visibility restricted to own records),
   rehearsed as the answer to "how the medical admins can use the system"
   (transcription is imperfect here — likely "the admins," not a
   medical-specific reference; no other part of the call mentions a
   medical context).

## Relevance to this revision

No commercial terms, pricing, or commitments were discussed in this
call — it is purely a product-demo rehearsal. Useful here only as
corroborating evidence for the BANT need items already logged in CRM
(`x_bant_need`), and as the source for classifying attendance/payroll/AI
items in `verbal-promises.md` — none of which have a priceable basis in
this repo's `hour-lookup.yaml` or `phase2-catalogue.yaml` (real-estate
brokerage catalogue covers property/CRM/invoicing domains only, not HR/
attendance or payroll). Full raw transcript retained at
`C:\Users\USER\Downloads\Scholarix Global's Meeting Notes_otter_ai (1)\`.
