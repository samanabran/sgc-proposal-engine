<!--
INTERNAL DRAFT — NOT YET REVIEWED, NOT YET SEND-READY. Revised 2026-08-08
after review feedback; see manifest.yaml's 2026-08-08 escalation entries
for the full record of what changed and why.

This is not a retraction of an issued revision (01-templates/comms/correction-notice.md's
use case) — Kallat Rev1 was never issued to the client (manifest.yaml:
issued_date: "", prior_versions_issued_to_client: false). This is the
written correction manifest.yaml's decision #9 (2026-08-07) and
HANDOVER.md §14.4 require before or with the priced offer, addressing
verbal exposure from the 2026-07-16 discovery/demo call
(00-intake/call-transcript-2026-07-16-discovery-demo.md,
00-intake/verbal-promises.md rows 9-13, HANDOVER.md §14.1-14.3 gap
register).

PROVENANCE — AED 3,900 / AED 3,400 (point 3 below): `00-knowledge/pricing/
phase2-catalogue.yaml`, version 2.1, `effective_from: 2026-08-05`, items
`portal_sync_property_finder` (price_aed: 3900, Property Finder only) and
`portal_sync_bayut_dubizzle` (price_aed: 3400, Bayut + Dubizzle combined,
one line covers both). Governed rate-card values with a version and an
effective date, not a memory or a live lookup. Also worth carrying into
any final version: the catalogue's own `portal_dependency_note` makes
both prices conditional on 5 client-side preconditions (valid RERA/DLD
licence, agency RERA ID, portal-side verification, image-standard
compliance, client's own portal API subscription) — this letter states
the fee, not the precondition list; flag if that omission matters before
send.

DECISION #9 STATUS — OPEN, NOT CLOSED. Grepped the full Kallat draft set
(03-draft/ non-quarantined tree, 04-draft/_quarantine/ HTML+PDF) for
per-user figures. Found one live, non-quarantined instance:
03-draft/KP-2026-SUB-01_Rev1/07-options-inclusions.md:10 — "Additional
users beyond 40 | Per-user, non-discountable | AED 250/user/month". This
is stale against the 2026-08-05 v3.0 pricing model, which deleted
`additional_user` (the AED 250/mo line) entirely and replaced it with
`onboarding_fee_per_marginal_user` + `platform_capacity_fee`
(phase2-catalogue.yaml, "REPLACED 2026-08-05 (v3.0)" comment). It sits
in the live current-revision path (manifest.yaml: current_revision
KP-2026-SUB-01_Rev1, path 03-draft/KP-2026-SUB-01_Rev1/), not the
quarantined render — so it is not covered by 04-draft/_quarantine/NOTICE.md
and would carry forward into any future render untouched. This is a
per-user rate in a client-facing-path document, which is exactly what
decision #9's ruling (HANDOVER.md §14.4: "flat monthly, no per-user rate
anywhere in the document, no per-user derivation even as a labelled
illustration") was meant to prevent. Because of this, the version of
this letter below no longer asserts that the no-per-user promise is
honoured — that claim was premature and has been removed. Fixing
07-options-inclusions.md:10 is Stage 5 pricing content, out of scope for
this correction-notice task and for the still-held Stage 5 — logged
separately in manifest.yaml as its own finding, not fixed here.

REVIEW GATE — checked against the actual review_stamp_check() code
(05-ops/render_r11_r12.py:104-132), not assumed. Its
REVIEWED_MATERIAL_SUBPATHS is `("00-intake", "02-calc", "03-draft",
"manifest.yaml")` — 03-draft IS in scope; the gate is not location-based
in the way "outside 04-draft" would suggest, it's commit-hash-based: it
refuses unless 04-draft/_review-stamp.yaml exists, decision=="approved",
and reviewed_commit matches the most recent commit touching those four
paths. The current stamp's reviewed_commit (025dc0864be9c4c0d6c56b52c5683ca263d2474b)
was already stale before this session touched anything — three later
commits (08d2880, 7b91df2, 067ff04) touched manifest.yaml after that
hash, so review_stamp_check() has been refusing Kallat as send-ready
since 2026-08-07, independent of this file's existence. This letter
does not need a separate "instance two" ungoverned-document log entry —
it was already structurally inside the gate. Separately, and worth
noting: `ALLOWED_CLIENTS` in that same script is `["MRD-meridianview-realty"]`
only — Kallat cannot render through R11/R12 at all right now regardless
of stamp status.

Routing per instruction, 2026-08-08: Bran review -> [signatory role,
see below] -> Bran final instruction to send. Not authorized for client
contact until that sequence completes and a fresh, hash-matched
04-draft/_review-stamp.yaml entry exists.

OPEN ITEM — signatory. Previous version signed this "Johnny Gurrera" —
wrong on inspection: Johnny's un-gated lane (351de57 -> 025dc08) was
scoped specifically to the no-figure/no-commitment headcount question,
and this letter carries several figures. manifest.yaml's own language
elsewhere ("stamp-SDR-John-stamp sequence") is the source of "John" in
this document's routing, but nothing in this repo establishes whether
that's Johnny Gurrera acting in a different, more formal capacity, or a
second, distinct person. Left unsigned pending that answer — do not
default to Johnny Gurrera without confirming.

OPEN ITEM — security paragraph. Revised to a pure retraction: withdraws
the "completely implausible" claim and states only what's already on
record elsewhere in this repo (the Priority SLA tier), with no new
security claim invented to fill the gap. This is a commercial judgment,
not a legal one — if this paragraph is expected to carry weight in a
dispute, it needs counsel's review before send, not just Bran's.
-->

Subject: Kallat Properties — a few things from our 16 July conversation, before we send pricing

Dear Sadique,

Thank you again for the time on 16 July — it was a genuinely useful
conversation, and the platform walkthrough clearly landed on the right
priorities (property management and portal integration, as you flagged
toward the end of the call). Before we come back to you with numbers, we
want to put a few things from that conversation in writing, precisely,
so nothing is a surprise later.

**1. Three items we demonstrated live aren't in the package we're pricing for you.**
Commission calculation, automatic reconciliation of client/landlord
payments, and client/landlord payment portals all came up in the demo
and generated real interest — but none of them are part of our standard
real-estate platform configuration today. We got ahead of ourselves
showing them working. If you'd like these included, we can scope and
price them as a distinct addition once the core system is defined; they
won't be bundled into the base offer by default.

**2. On security, we overstated it.**
On the call we described cyberattacks against our system as "completely
implausible." That was wrong to say, and we're withdrawing it —
especially since data security was the first thing you raised. We won't
replace it with a different guarantee here; what we can point to is that
the proposal's Priority support tier (4-hour response SLA) is paired
with this deal specifically because of the data-security sensitivity you
raised, not offered as a generic upsell.

**3. On portal connections (Bayut, Property Finder, Dubizzle) — two corrections.**
First, cost: we told you the only cost involved is the portal's own API
fee, with the connection itself being "one click" at no charge from us.
That's not accurate — connecting to Property Finder is a one-time AED
3,900 integration fee, and Bayut/Dubizzle together are a one-time AED
3,400 integration fee, separate from whatever subscription each portal
charges you directly. Second, accreditation: we referred to our system
as "already accredited by" all three portals. We don't currently hold
formal accreditation or partnership status with Bayut, Property Finder,
or Dubizzle — connections use their published integration channels, the
same as any other CRM vendor's.

We'd rather send you this correction now than have you discover any of
it after signing. The priced proposal, including how we've structured
the monthly fee, will follow separately once we've confirmed a couple of
scoping details with you directly.

Best regards,
[[signatory pending — see internal note]]
SGC TECH AI

---
Internal note (do not send as-is): log this correction in
02-clients/KP-kallat-properties/manifest.yaml under a new escalation
entry, and route per instruction — Bran review first, then [signatory
role — pending], then back to Bran for final instruction to send to
Sadique Abbas (sales@kallatproperties.com / +971 54 791 6003). Do not
send to the client until that full sequence completes, the signatory
question is resolved, and a fresh 04-draft/_review-stamp.yaml entry is
written hash-matched to the commit containing this file.
