# Monday Meeting Flow — RVN Onsite Demo

**When**: 11:30 AM, Monday
**Where**: Burjuman Business Towers, Office 56, 13th floor, Dubai
**Attendees (client side)**: Ms. Dia (assigns leads, would be a CRM user);
Mr. Nazim, Owner — **final approval authority for funds and charges**;
possibly a third stakeholder — Ms. Dia said she would "schedule at least
the three of them" for a proper time (transcript 13:12).
**Attendees (SGC side)**: SDR (call attendee) + demo lead.

## Objective

1. Show RVN a working demo of the CRM configured for their actual
   workflow — not a generic walkthrough.
2. Present the quotation (§10 of `03-draft/RVN-2026-SUB-01_Rev1/`) with
   full honesty about what's priced and what isn't.
3. Get explicit buy-in from Nazim, or a clear list of what's blocking it.
4. Lock in the follow-up decision meeting — the action item RVN itself
   proposed ("schedule a follow-up meeting with Nazim and at least two
   other relevant stakeholders... to review the CRM proposal and decide
   on implementation").

## Pre-meeting checklist (before 11:30)

- [ ] Demo environment (`https://demo.sgctech.ai`, `editions.yaml:
      demo_environment`) confirmed to be running **Community edition** —
      G41 requires this check every time, and it matters doubly here
      because RVN has already seen 5-6 other vendors' pitches and will
      notice if the demo doesn't match what's quoted.
- [ ] Demo data pre-loaded to resemble RVN's real shape: a lead list with
      Meta/Google source tags, 2-3 agents with assigned leads, at least
      one logged call with an outcome (answered/not answered/follow-up)
      and notes.
- [ ] `03-draft/RVN-2026-SUB-01_Rev1/` printed or ready to screen-share —
      lead with §01 Executive Summary and §10 Commercial Terms bookmarked.
- [ ] Confirm attendee count on arrival — if a third stakeholder shows up
      unannounced, that's fine; don't restart the pitch, fold them in.

## Running agenda

**1. Opening (5 min)**
Thank them for the time, introduce anyone new on the SGC side, confirm
who's in the room and their role (especially if a third stakeholder is
present). Set expectations: demo first, quotation second, questions
throughout.

**2. Recap of pain points (5 min)** — anchor the whole meeting here
Reflect back, in their own words, what Dia described on the call: leads
landing in a shared Google Sheet and being manually shuffled into
per-agent sheets; no reliable way to know if a lead's been called,
answered, or followed up; a 250-calls/day target nobody can verify;
attendance tracked by a logbook that "doesn't make sense." This isn't
filler — it's the frame that makes the demo land as "solving your
problem" instead of "generic CRM tour."

**3. Live demo — lead distribution (10 min)**
Show a lead entering the system (simulating a Meta/Google Ad lead),
automatic distribution rules, and the one-click manual assignment
override Dia specifically asked about ("if whoever is doing it, I will
be assigning for them, right?" — yes, exactly this).

**4. Live demo — call logging & activity (10 min)**
Show an agent logging a call: answered / not answered / follow-up flag /
notes field. Be explicit and honest here: **this is manual logging by
the agent**, not automatic call detection — do not let the demo imply
otherwise. This is the single highest-risk moment for over-promising in
the whole meeting; see the objection note below.

**5. Live demo — reporting dashboard (5 min)**
Show the dashboard aggregating logged calls per agent per day against
the 250-calls/day target. Frame it as "what Dia currently has to chase
manually, now automatic" — the exact language she used describing her
own biggest time cost.

**6. Address attendance/sensor tracking directly, don't dodge it (5 min)**
Do not demo something you don't have. State plainly: this requires
knowing their sensor system's vendor and whether it has an API — SGC
will scope and quote it separately once that's known. Ask, right there
in the room, what sensor system they use — getting that answer today
unblocks pricing it for the follow-up meeting.

**7. Address call-analyzer/telephony integration directly (5 min)**
Same honesty. Ask what phone system agents actually use beyond personal
SIM cards — if there's no PBX/VOIP, say plainly that automated call
tracking needs that infrastructure decision made first, and that manual
logging (already demoed) is what's priced today.

**8. Present the quotation (10 min)**
Walk through §10 Commercial Terms: mobilisation AED 5,058 + refundable
deposit AED 1,680, subscription AED 1,680/month quarterly, Year 1 AED
25,218. Be direct that this is a single option (no zero-mobilisation
alternative currently offered) and explain why (§10 financing
disclosure — settling in full at kickoff removes the recovery
component entirely, if Nazim prefers that).

**9. Q&A / objection handling (10-15 min)** — see below

**10. Close: lock the follow-up meeting (5 min)**
Explicitly ask: "Can we schedule the follow-up meeting with Mr. Nazim
[and the third stakeholder, if not already in the room] to make the
implementation decision?" Get a date before leaving the room — this was
RVN's own stated next step; don't leave it as an open action item on
your side alone.

## Anticipated objections and how to handle them

- **"We've talked to 5-6 other CRM vendors already."** (fatigue/
  skepticism) — Don't compete on being the first or newest. Lean on
  auditability: every number in this proposal traces to a worksheet that
  passed 41 checks, and the two features we can't price yet, we're
  telling you that instead of guessing. See `03-library/objection-handling/price-too-high.md`
  for the specialist-boutique positioning language if price comes up.
- **"Will my team actually use this?"** — Adoption objection.
  `03-library/objection-handling/team-wont-adopt.md` has the full
  script: SGC delivers a trained, documented system (2 sessions bundled,
  §11); RVN owns the internal rollout cadence; §09's adoption clause
  makes this a checkable day-30/day-60 commitment, not a vague promise.
- **"Why isn't attendance/call-analyzer included — I asked for that."**
  Do not get defensive or apologize for not pricing it. Reframe as
  honesty: "We'd rather ask you two questions today than hand you a
  number we made up. Tell me your sensor vendor and your phone setup,
  and that becomes real scope for the next meeting, not a guess in this
  one." This is a credibility moment, not a gap to smooth over.
- **"What about VAT / is this Enterprise-grade?"** — Only answer if
  asked (per SGC policy). If VAT is raised: SGC is not currently
  VAT-registered, no VAT is charged (`clause-library/vat-uae.md`
  verbatim). If Enterprise/mobile-app expectations come up: this is
  Odoo Community — state what's included/excluded per
  `editions.yaml`, do not imply Enterprise features are included.

## Close-the-loop ask (explicit)

By the end of this meeting, have on record: (1) Nazim's initial reaction
— approve, need-time, or specific blockers; (2) their sensor-system
vendor and phone/telephony setup, to unblock Phase 2 scoping; (3) a
confirmed date for the follow-up decision meeting with Nazim + at least
two other stakeholders, per RVN's own stated plan.
