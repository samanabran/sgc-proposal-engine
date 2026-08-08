# Freeze/no-freeze decision package — Kallat correction notice

For Bran. This file makes no send/no-send or freeze/no-freeze
recommendation — that decision is explicitly yours (standing rule,
2026-08-08). It contains the letter verbatim, every client-facing number
in one place, the `freeze_for_docuseal.py` read-only findings, and every
open objection, prepared to the edge and handed over rather than used as
a reason to stop.

---

## A. The correction letter, in full, verbatim, as it currently stands

Source: `03-draft/KP-2026-SUB-01_CorrectionNotice_Draft1.md`, unedited.

<!--
INTERNAL DRAFT — NOT YET REVIEWED, NOT YET SEND-READY. Revised 2026-08-08
(third pass) after review feedback; see manifest.yaml's 2026-08-08
escalation entries for the full record of what changed and why.

This is not a retraction of an issued revision (01-templates/comms/correction-notice.md's
use case) — Kallat Rev1 was never issued to the client (manifest.yaml:
issued_date: "", prior_versions_issued_to_client: false). This is the
written correction manifest.yaml's decision #9 (2026-08-07) and
HANDOVER.md §14.4 require before or with the priced offer, addressing
verbal exposure from the 2026-07-16 discovery/demo call
(00-intake/call-transcript-2026-07-16-discovery-demo.md,
00-intake/verbal-promises.md rows 9-13, HANDOVER.md §14.1-14.3 gap
register).

PROVENANCE — AED 3,900 / AED 3,400, reconciled fully. Two separate
artifacts, two separate version numbers, same commit (525940d,
2026-08-05), easy to misread as one: `00-knowledge/pricing/policy.yaml`
is at v3.1, with "v3.0" naming the 2026-08-05 change that deleted
`overlays.rollout_hours_per_user`; `00-knowledge/pricing/
phase2-catalogue.yaml` is at v2.1 (bumped from v2.0 the same day, same
commit) — its own "REPLACED 2026-08-05 (v3.0)" comment is citing
policy.yaml's v3.0 change as the reason `additional_user` was replaced,
not claiming the catalogue itself is v3.0. The portal_sync figures
themselves are unaffected by either change: `git log -p` on
phase2-catalogue.yaml shows portal_sync_property_finder (3900) and
portal_sync_bayut_dubizzle (3400) were added in commit 1633e44
(2026-08-03, v2.0) and have not been touched since — the 525940d diff
only touches the additional_user/onboarding block, portal_sync_* lines
appear as unchanged context. Pre-2026-08-03: no phase2-catalogue.yaml
existed at all — the whole repo's first commit (cb2f194) is dated
2026-08-03, and that first version (v1.0) didn't have portal_sync items
either (different AI-vendor-comparison content, replaced 22 minutes
later in 1633e44). So the honest timeline: this rate card, and this
repo's governance generally, is ~2.5 weeks younger than the 2026-07-16
call being corrected. There was no rate card for Johnny or the
Consultant to be accurate against at the time they spoke — this letter
is stating SGC's current, governed position, not asserting what was
secretly true in July. Reflected in the client-facing wording below
("our current position is different," not "that's not accurate").
Cross-checked against the rest of the corpus: these exact figures,
same 5-precondition dependency note, appear identically for VGE, MRD,
and PRO — a repo-wide governed rate, not a one-off invented for Kallat.

ACCREDITATION / FEE RECONCILIATION. `phase2-catalogue.yaml`'s
`portal_dependency_note` (unchanged since 2026-08-03): the AED
3,900/3,400 fee is for SGC building the sync, contingent on precondition
(5) — "the client's own portal subscription contract includes feed/API
access." Under this model SGC never needs its own accreditation or
partner status with Property Finder/Bayut/Dubizzle — the client (a
RERA-licensed agency) holds the portal-side access, SGC builds against
it. That resolves the logical tension: charging a fee and disclaiming
accreditation are not actually contradictory once the fee is understood
as build labor, not a pass-through of a partnership SGC doesn't have.
Item 3 revised again 2026-08-08 (third pass): added the AED 7,300
combined total (Sadique asked about all three portals on the call, not
one at a time — splitting the figure and leaving the addition to him
would repeat the soft-pedalling this letter exists to correct). Broken
the feed/API-access precondition out into its own paragraph with an
explicit admission that we don't know whether Kallat's current
subscriptions include it or what each portal charges to add it — that
clause was a trailing subclause in the prior version, which quietly
introduced a second unquantified cost in the same paragraph as the
correction of the first one.

Fourth pass, 2026-08-08: heading changed from "two corrections" to "two
corrections, and one thing to check on your side" — the feed/API
paragraph added in the third pass is a disclosure of something never
mentioned in July, not a correction of something that was; Sadique will
count, and the heading should match what he'll read. Accreditation
paragraph changed "the sync is built" to "the sync would be built" —
present tense implied a track record that, per the DEFERRED-status
finding above, doesn't exist for any client. One conditional, but it's
the tense that has to be right in this letter specifically.

**COMMERCIAL RISK, not just a caveat** — raised to that level 2026-08-08
per instruction. No file anywhere in this repo records a completed
portal_sync delivery for any client — VGE, MRD, and PRO all show this
item at DEFERRED/proposal stage, none at delivered. The
portal_dependency_note reconciles the *accreditation* contradiction (SGC
needs none under this model), but it is governed provenance for the
*number*, not evidence the number covers labour SGC has ever actually
performed. This letter's whole purpose is correcting a previous
under-quote; converting an unproven catalogue rate into a written,
client-facing price in that same letter is a real risk of repeating the
pattern it exists to fix, not a hypothetical. Two changes made because
of this: (1) the letter now presents the figures as the *current
catalogue rate*, not a stated fixed all-in cost for demonstrated work;
(2) this is logged as a commercial risk for Bran in the review request,
not filed as a background note about outside instances — flagged, not
resolved, since no one in this session can confirm delivery capability
from repo files alone.

DECISION #9 STATUS — OPEN, NOT CLOSED, now annotated at the source too
(see 03-draft/KP-2026-SUB-01_Rev1/07-options-inclusions.md:10, marked
SUPERSEDED inline today per instruction, pending the Stage 5 fix). Full
grep evidence: 03-draft/KP-2026-SUB-01_Rev1/07-options-inclusions.md:10
(live, non-quarantined) plus the expected matches in
04-draft/_quarantine/KP-2026-SUB-01_Rev1_Internal.html:218 and .pdf (via
pdftotext) — the quarantined copies are already frozen/stale by design,
the 03-draft instance was the live exposure. That line (07-options-
inclusions.md:10) pairs a per-user rate we're not supposed to charge
with the unsourced 40-headcount figure in one sentence — worse than
either alone. Dereferenced to path:line rather than quoted verbatim
2026-08-08 (fourth pass): the literal string was tripping
check_20_per_user_rate_leak (validate.py) against this file itself —
correctly, since it's a true hit, but a permanent self-inflicted one a
reader would learn to scroll past. The finding is unchanged; only the
citation method is.

REVIEW GATE — re-verified by actually running the code (not just
reading it), 2026-08-08:
  review_stamp_check('KP-kallat-properties') -> refuses: stamp's
  reviewed_commit (025dc0864be9c4c0d6c56b52c5683ca263d2474b) does not
  match current commit touching reviewed material (e922641, as of this
  revision).
  pre_render_gate('KP-kallat-properties') -> refuses, FOUR independent
  reasons: not in ALLOWED_CLIENTS; T12 headcount unsourced; T12
  unrequested-scope delta (AED 19,652); T12 segment classification
  depends on the unverified headcount. Stamp invalidity is a fifth.
  review_stamp_check('MRD-meridianview-realty') -> refuses: no stamp
  file exists at all right now.
RECONCILED against the "Kallat stamp passes / MRD refuses" note this
review flagged as a possible contradiction (CHANGELOG.md:1953, dated to
the 025dc08 commit): that note is about review_stamp_check() in
isolation, snapshotted the day the stamp was written — not about
ALLOWED_CLIENTS, which was set to MRD-only on 2026-08-06 (commit
b3e8cd3, "Add R11/R12 renderer, scoped to MRD only") and has never
changed since, predating Kallat's stamp entirely. Both statements are
true, about two different, independent gates, at two different points
in time — not a contradiction. No new information changes this letter's
status: Kallat could not render through R11/R12 then and cannot now,
independent of stamp validity, and the stamp is separately invalid too.

Routing per instruction, 2026-08-08: Bran review -> [signatory, per
HANDOVER.md §2 decision #10, not yet recorded] -> Bran final instruction
to send. Not authorized for client contact until that sequence
completes, decision #10 is recorded, and a fresh, hash-matched
04-draft/_review-stamp.yaml entry exists.

SIGNATORY — corrected 2026-08-08 (second correction). The previous
revision kept Johnny Gurrera signed on the strength of an AskUserQuestion
answer ("Same person — Johnny Gurrera"). Bran's follow-up: that basis
points the wrong way — the instruction being cited is the same one where
he separated Johnny's headcount lane from the formal signing lane and
said in terms that Johnny is not the signatory here. No documentary
mapping exists either (checked 10-signature/ in full, render_r11_r12.py,
every John-adjacent mention in HANDOVER.md/CHANGELOG.md/manifest.yaml —
nothing). Rather than infer again, this is now recorded as
HANDOVER.md §2, decision #10 (added 2026-08-08), for Bran to answer on
his own next pass: is Johnny Gurrera the "John" in the
stamp-SDR-John-stamp sequence, yes or no. Until that row is filled in,
the signature block below carries no name.

SECURITY PARAGRAPH — revised per instruction to a strict two-sentence
retraction: withdraws the claim, states nothing else. The prior version's
second sentence (pointing at the Priority SLA tier as if it answered the
security concern) is removed — it asserted an unrecorded reason for that
tier's selection and risked reading as "a response-time SLA is a
security control," which it isn't. Cut entirely, no substitute.
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
price them separately; they won't be bundled into the base offer by
default.

**2. On security, we overstated it.**
On the call we described cyberattacks against our system as "completely
implausible." That was wrong to say, and we're withdrawing it —
especially since data security was the first thing you raised.

**3. On portal connections (Bayut, Property Finder, Dubizzle) — two corrections, and one thing to check on your side.**
First, cost: we told you the only cost involved is the portal's own API
fee, with the connection itself being "one click" at no charge from us.
Our current catalogue rate is different: AED 3,900 one-time for
Property Finder, and AED 3,400 one-time for Bayut/Dubizzle together —
AED 7,300 one-time in total if you want all three connected. That's for
the integration work itself, separate from whatever subscription each
portal charges you directly.

On that point: connecting any of the three also requires your own
portal account to already include feed or API access, not just a
standard listing account. We don't know whether your current
subscriptions include that, or what each portal charges to add it if
they don't — that's a question for your own portal account managers,
not something we can price from our side.

Second, accreditation: we referred to our system as "already accredited
by" all three portals. That's not something we hold — the sync would be
built against your own portal access, not a partnership status on our
side — and we shouldn't have described it as an existing accreditation.

We'd rather send you this correction now than have you discover any of
it after signing. The priced proposal, including how we've structured
the monthly fee, will follow separately once we've confirmed a couple of
scoping details with you directly.

Best regards,
[[signatory pending — see HANDOVER.md §2, decision #10]]
SGC TECH AI

---
Internal note (do not send as-is): log this correction in
02-clients/KP-kallat-properties/manifest.yaml under a new escalation
entry, and route per instruction — Bran review first, then whoever
HANDOVER.md §2 decision #10 identifies (confirming commitment and
signing), then back to Bran for final instruction to send to Sadique
Abbas (sales@kallatproperties.com / +971 54 791 6003). Do not send to
the client until that full sequence completes, decision #10 is
recorded, and a fresh 04-draft/_review-stamp.yaml entry is written
hash-matched to the commit containing this file.

---

## B. Every client-facing number in the letter — single block

Extracted from the Subject line through the "SGC TECH AI" sign-off only
(the internal note and header above are never sent, so their contents —
including the AED 19,652 Stage-5 figure and the phone/email in the
routing note — are excluded from this block on purpose).

| Figure | Context | Appears |
|---|---|---|
| **16 July** | Date of the discovery/demo call being referenced | Subject line, and again in "the time on 16 July" |
| **AED 3,900** | Property Finder portal-sync integration fee, one-time | Item 3, paragraph 1 |
| **AED 3,400** | Bayut/Dubizzle portal-sync integration fee combined, one-time | Item 3, paragraph 1 |
| **AED 7,300** | Sum of the two above, stated explicitly as the all-three-portals total | Item 3, paragraph 1 |
| 1 / 2 / 3 | Item numbers (structural, not commercial) | Section headings |

**That's the complete set.** No headcount figure (40), no Stage-5
pricing figure, no per-user rate, and nothing else numeric appears
anywhere in the sendable text. The AED 19,652 unrequested-scope figure
and the 40-headcount figure — both still live, unresolved findings on
this deal — are Stage-5/pricing-worksheet matters and do not appear in
this letter at all.

---

## C. `freeze_for_docuseal.py` — read-only findings

Read in full: `02-clients/PRO-prosper-realestate/04-draft/freeze_for_docuseal.py`
(78 lines). Not run. No Kallat variant created.

- **Client-generic or Prosper-specific?** Entirely Prosper-specific.
  `DRAFT_DIR` is a hardcoded absolute path into
  `PRO-prosper-realestate/04-draft`; the `DOCS` list hardcodes two exact
  Prosper filenames (`PRO-2026-SUB-01_Rev3_Offer.html`,
  `PRO-Requirements-Answered_2026-08-06.html`); the footer template
  hardcodes the string `"PRO-2026-SUB-01"`. Nothing in the script is
  parameterized by client — no CLI argument, no config file, no
  client-name variable.
- **What it takes as input:** Two pre-existing **HTML** files at those
  hardcoded paths. It does not parse or accept Markdown at all — it
  opens each HTML file via a `file:///` URL in a headless Chromium page
  and prints that to PDF. If the HTML doesn't already exist at the
  hardcoded path, the script has no fallback; it will simply fail to
  find the file.
- **Gated render, or will it accept a hand-reviewed file?** No gate of
  any kind. It does not import `render_r11_r12.py`, does not check
  `ALLOWED_CLIENTS`, does not call `review_stamp_check()` or any T10-T12
  check. It will freeze whatever HTML happens to be sitting at the
  hardcoded path — hand-reviewed, machine-rendered, or hand-edited
  afterward, the script cannot tell the difference and doesn't try. Same
  shape as Kallat's own `assemble_and_render.py`, found two rounds ago.
- **Template/account configuration expected:** None. The script contains
  no DocuSeal API call, template ID, or account reference anywhere. It
  is purely a local step: HTML → PDF (via Playwright) → SHA-256 hash →
  printed instructions to record the hash in `manifest.yaml` "before
  submitting to Docuseal." The actual DocuSeal upload/template/signer
  assignment is a separate, undocumented-in-this-script step — not
  investigated further, since only this file was authorized to be read.
- **What it dispatches, and to which addresses:** Nothing. No email, no
  API call, no network request of any kind — confirmed by reading the
  full file; the only I/O is local file writes and a hashlib digest. It
  does not send anything to Sadique, Bran, or anyone else.
- **Does a Kallat path exist, or would one need to be created?** No
  Kallat equivalent exists — the only script under
  `02-clients/KP-kallat-properties/` is `04-draft/assemble_and_render.py`.
  Creating a Kallat freeze script would require (a) a client-specific
  copy of this file with Kallat's paths and filenames substituted, per
  the same pattern, and (b) — a gap that exists independent of the
  script — **an HTML rendering of the correction letter itself, which
  does not currently exist.** The letter lives only as Markdown
  (`03-draft/KP-2026-SUB-01_CorrectionNotice_Draft1.md`). Nothing in
  this repo converts that specific file to HTML today; `assemble_and_render.py`
  only assembles the 13 numbered `KP-2026-SUB-01_Rev1/*.md` proposal
  sections, not this correction notice. Neither of these two things was
  created this pass, per the read-only instruction.

---

## D. Objections — logged, not acted on

Each entry: what it is, what it blocks, what would clear it, and whether
it is agent judgment or a configured constraint already on record.

1. **No HTML rendering of the correction letter exists, and no
   Kallat-specific freeze script exists.** Blocks: any freeze-to-PDF
   step today, by anyone, through any tool — this is a literal capability
   gap, not a policy one. Clears with: someone writing/adapting a
   render step (Markdown → HTML) and either adapting
   `freeze_for_docuseal.py` for Kallat or running an equivalent manual
   Playwright HTML→PDF+hash step. **Configured constraint** in the sense
   that it's a real absence, not agent judgment — nothing to override.

2. **`review_stamp_check()`/`ALLOWED_CLIENTS` do not gate
   `freeze_for_docuseal.py`-style scripts at all.** Not a blocker to
   freezing technically — confirmed by reading the code, the freeze step
   has no dependency on either. It is a blocker only in the sense that
   Kallat's standing render-pipeline status (fails all 4
   `pre_render_gate()` grounds, stamp invalid) means nothing about this
   deal has ever passed the *governed* path — freezing via a
   hand-reviewed route would be explicitly outside that path, which is
   consistent with your prior decision that Kallat ships (if it ships)
   hand-reviewed, not through `ALLOWED_CLIENTS`. **Configured
   constraint** — your own standing decision, restated here, not new
   agent judgment.

3. **Commercial risk: no completed `portal_sync` delivery is recorded
   for any client in this repo.** The letter states AED 3,900 / 3,400 /
   7,300 as governed catalogue rates; provenance for the *number* is
   solid, but there's no record anywhere of the *work* having been
   performed. Blocks: nothing mechanically — the letter already frames
   this as a "current catalogue rate," not a claim of prior delivery, per
   your last round's instruction. Still a real commercial risk if
   Sadique later asks "have you done this before." Clears with: your own
   knowledge of whether this has been delivered outside this repo, or a
   decision that the risk is acceptable as framed. **Agent judgment** —
   flagged, not resolved by anyone in this session.

4. **Security paragraph is a commercial retraction, not a legally
   reviewed one.** Blocks: nothing about freezing. Relevant if this
   letter is ever expected to carry weight in a dispute. Clears with:
   counsel review, if and when that matters to you. **Agent judgment,**
   stated explicitly as outside agent competence.

5. **Signature block is a literal placeholder bracket in the current
   text:** `[[signatory pending — see HANDOVER.md §2, decision #10]]`.
   If frozen to PDF today as-is, that bracketed text would appear
   verbatim in the frozen artifact (which is explicitly an *internal
   review* copy per the freeze script's own footer convention, so this
   may be exactly the right state to freeze in — noted as fact, not
   pushed either way). Clears with: decision #10. **Your own open item,
   explicitly not the agent's**, per your instruction.

6. **Stage 5 pricing remains held** (T12 headcount unsourced; T12
   unrequested-scope delta, AED 19,652; T12 segment classification
   depends on the unverified headcount) — none of these figures appear
   in this letter, but the letter's own closing line promises "the
   priced proposal... will follow separately," and that follow-up is
   currently blocked on these. Not a blocker to freezing *this* letter.
   Carried forward from prior rounds, not new. **Configured
   constraint/prior ruling**, restated for completeness, not re-litigated
   here.

7. **`check_20_per_user_rate_leak` (validate.py) cannot see rendered
   HTML/PDF or anything under `04-draft/`** — confirmed by reading
   `gather_draft_files()` two rounds ago. Relevant here specifically:
   freezing this letter would produce exactly the kind of artifact
   (`04-draft/`, PDF) this check can never inspect. Drafted as candidate
   defect #24 for `known-defects.md`, not yet added (Commercial Desk
   action, per `AGENTS.md`). **Agent-identified structural gap**, logged,
   not blocking.

---

## E. Standing constraints — not objections, still enforced

These are not on the table for freeze/no-freeze judgment; they remain
hard stops regardless of what this package recommends (it recommends
nothing):

- **Sending anything to Sadique Abbas.** Your trigger only.
- **Accessing `mail.sgctech.ai`/SOGo.** Your own earlier instruction;
  decision #8 (HANDOVER.md §2) is still open.
- **Writing into `00-knowledge/`.** `AGENTS.md`'s absolute rules; not
  overridden by any instruction short of you changing the rule itself.

---

Decisions #8 and #10 remain yours. Signature block unchanged. Nothing
sent, nothing frozen, no client contacted, `ALLOWED_CLIENTS` unchanged.
