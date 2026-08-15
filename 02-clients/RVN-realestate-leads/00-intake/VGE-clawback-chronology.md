# VGE Clawback Chronology — Facts Only

Prepared 2026-08-15 as part of an RVN closing-pass audit; concerns a
different client (VGE-vongeyern-realestate) surfaced as a side finding.
No adjudication of enforceability or remediation is made in this file —
that is for counsel. Every line below is a direct citation to a file in
this repository.

## Document facts

**VGE-2026-SUB-01 Rev1** — `02-clients/VGE-vongeyern-realestate/05-issued/VGE-2026-SUB-01_Rev1/VGE-2026-SUB-01_Rev1.md`
- Header: `ISSUED 2026-06-15. SUPERSEDED by Rev2 (2026-07-10).` (line 2)
- Body: `**Issued**: 2026-06-15 · **Status**: Superseded 2026-07-10 (see Rev2)` (line 10)
- Commercial: Option A mobilisation AED 17,301 at 25% of build value → implied build value ≈ AED 69,204, implied deferred/financed remainder ≈ AED 51,903 (line 62-64; 25% mobilisation stated directly, remainder computed from that stated percentage, not separately labelled in the document).
- Clawback: the **entire and only** reference to clawback in this document is the six-word fragment on line 58: `"...hrs each, billed once). Clawback clause included."` There is no `## Clawback` heading, no clause body, no quoted contractual text anywhere in the file. Confirmed by full-text search of the document — no other occurrence of the string "clawback".

**VGE-2026-SUB-01 Rev2** — `02-clients/VGE-vongeyern-realestate/05-issued/VGE-2026-SUB-01_Rev2/VGE-2026-SUB-01_Rev2.md`
- Header: `ISSUED 2026-07-10. SUPERSEDED by Rev3 (in 03-draft/, pending issue).` (line 2)
- Body: `**Issued**: 2026-07-10 · **Status**: Superseded (Rev3 pending, term extension requested 2026-08-03)` (line 9-10)
- Commercial: Option A mobilisation AED 27,255 at 25% of build value → implied build value ≈ AED 109,020, implied deferred/financed remainder ≈ AED 81,765 (line 60-62; same basis as Rev1 — percentage stated, remainder not separately labelled).
- Clawback: the **entire and only** reference is line 54-55: `"18-month initial term. Adoption clause included. Clawback clause included."` Same pattern as Rev1 — no heading, no clause body, no quoted text. Confirmed by full-text search.

## Contrast with this repo's own clawback clause standard

`00-knowledge/clause-library/clawback.md` (the approved verbatim text used elsewhere in this repo — e.g. KP, MRD Rev3, PRO, and RVN's own draft all quote it in full under a `## Clawback` heading) reads:

> If this subscription is terminated before the end of the committed term
> for any reason other than SGC TECH AI's material breach, the unrecovered
> balance of the implementation value becomes immediately due and payable.

Neither VGE Rev1 nor Rev2 contains this text, or any substitute clause text, anywhere in the document.

## Git history of these specific files

```
git log --follow -- 02-clients/VGE-vongeyern-realestate/05-issued/VGE-2026-SUB-01_Rev1/VGE-2026-SUB-01_Rev1.md
git log --follow -- 02-clients/VGE-vongeyern-realestate/05-issued/VGE-2026-SUB-01_Rev2/VGE-2026-SUB-01_Rev2.md
```
Both return a single commit: `cb2f194 2026-08-03 "Initial build: layered proposal-engine repo for SGC TECH AI"`. This is a squashed initial-import commit that added the whole repository structure at once, including these already-dated files. Git history cannot independently corroborate the in-document "Issued 2026-06-15" / "Issued 2026-07-10" dates — those dates exist only as text inside the documents themselves, not as separate commit timestamps from those actual dates.

## What the repo cannot establish

- Whether either document was actually transmitted to the client (email, portal, hand-delivery, or otherwise) — no transmittal log, sent-mail record, or delivery confirmation exists in this repository.
- Whether either document was countersigned by the client. No signature file, signed PDF, or e-signature platform record (e.g. from the Zoho Sign integration referenced elsewhere in this repo at `10-signature/`) exists for either VGE revision.
- Whether SGC's accounting recognised any revenue against the deferred/financed amounts implied above. No accounting or ledger records exist in this repository at all.
- Whether the in-document "Issued" dates reflect the date of actual client transmission or merely the date the document was finalized internally.

## Three factual questions for counsel

1. Do SGC's records (email, CRM, or signature platform, outside this repository) show that VGE-2026-SUB-01 Rev1 and/or Rev2 were transmitted to and/or countersigned by Von Geyern Real Estate Brokerage LLC, and if so, on what dates?
2. Has SGC recognised or invoiced any revenue against the deferred/financed remainder implied by either revision's 25%-mobilisation structure (approximately AED 51,903 for Rev1, AED 81,765 for Rev2), and if so, under what terms was that revenue secured absent visible clause text in the client-held document?
3. Rev2's own status line states a term extension was requested by the client on 2026-08-03, implying an ongoing relationship past both revisions — does any communication from that request or afterward reference, replace, or otherwise address the missing clawback clause text?

---

## KP / MRD / PRO — explicit status check for the same defect

Checked for the identical pattern: a deferred/financed amount present, paired with clawback represented only as a label with no clause body.

- **KP-kallat-properties — CLEAN.** `03-draft/KP-2026-SUB-01_Rev1/09-partnership-terms.md` has a `## Clawback` heading followed by the full quoted clause text (verified verbatim match to `clause-library/clawback.md`). `05-issued/` is empty for KP — nothing has been issued, draft-only. Worksheet shows `financed_remainder_aed: 33643` (`02-calc/pricing-worksheet.yaml:129`), a real deferred amount, correctly paired with real clause text in the draft. No exposure — never sent, and the draft itself is not defective.

- **MRD-meridianview-realty — MIXED, but not a new finding.** `05-issued/MRD-2026-SUB-01_Rev1/` and `05-issued/MRD-2026-SUB-01_Rev2/` are both issued and both **do** have the identical defect — but this is not new: it is defect #8 in `00-knowledge/failure-modes/known-defects.md` ("No clawback. Full build delivered before a single invoice..."), already documented, and both revisions carry `RETRACTION-NOTICE.md` files stating they were retracted. The current, unissued `03-draft/MRD-2026-SUB-01_Rev3/09-partnership-terms.md` **has** the full clause text under `## Clawback`, correctly. MRD's issued-and-defective revisions are a known, already-retracted, already-documented case — distinct from VGE, where no known-defects entry, retraction notice, or any other acknowledgment of the same defect exists anywhere in this repository.

- **PRO-prosper-realestate — CLEAN.** `03-draft/PRO-2026-SUB-01_Rev1/09-partnership-terms.md` has the full clause text under `## Clawback`. `05-issued/` is empty — nothing issued. `04-draft/render_offer.py:167` explicitly cites `00-knowledge/clause-library/clawback.md:19-21 -- approved verbatim text` as its source when rendering, i.e. the rendering pipeline itself pulls the real clause rather than a placeholder label.

**VGE is therefore the only client in this repository with (a) documents actually issued to a client, (b) a real deferred/financed amount, (c) no clawback clause text in the issued document, and (d) no existing acknowledgment of the defect anywhere in the repo's own known-defects log.** That combination is what makes it a new finding rather than a repeat of an already-known, already-retracted case.

---

## MRD — second section, same discipline (facts only, no adjudication)

Added 2026-08-15, on request, to sit alongside VGE with matching rigor rather than as a one-line status note above.

**MRD-2026-SUB-01 Rev1** — `02-clients/MRD-meridianview-realty/05-issued/MRD-2026-SUB-01_Rev1/MRD-2026-SUB-01_Rev1.md`
- Commercial: `"Blended delivery rate: **AED 690/hour**. Total: 33 hours. Recurring subscription: **AED 879/month**, covering platform, hosting, and support. No mobilisation required to start."` (lines 15-17, quoted verbatim). No mobilisation payment of any kind is stated — the full build (33 hours at the quoted rate) was represented as delivered before any invoice. This is a different shape from VGE's partial deferral: here the document itself states zero upfront payment, meaning the full build value is the unsecured amount, not a percentage remainder.
- Clawback: no occurrence of the word "clawback" anywhere in the document (confirmed by full-text search). Not a label-with-no-body, as at VGE — no reference at all.

**MRD-2026-SUB-01 Rev2** — `02-clients/MRD-meridianview-realty/05-issued/MRD-2026-SUB-01_Rev2/MRD-2026-SUB-01_Rev2.md`
- Commercial: `"Blended delivery rate: AED 690/hour. Recurring subscription: AED 879/month. No mobilisation required."` (lines 22-23, quoted verbatim). Same zero-mobilisation shape as Rev1.
- Clawback: same — no occurrence of the word "clawback" anywhere in this document either.

**RETRACTION-NOTICE.md, both revisions** — `02-clients/MRD-meridianview-realty/05-issued/MRD-2026-SUB-01_Rev1/RETRACTION-NOTICE.md` and the Rev2 equivalent. Quoted verbatim, unedited, per instruction not to tidy the phrasing:

> "Retracted as part of the v2 hardening rebuild, logged retrospectively in `manifest.yaml`. This revision's arithmetic and clauses do not reflect current knowledge-layer policy and must never be used as a template." (Rev1, lines 3-5)

> "8. No clawback clause — full build delivered before a single invoice." (Rev1, line 19, one item in a numbered defect list)

> "This revision was never corrected and sent to the client at the time — Rev2 was drafted next and introduced a different VAT error rather than fixing this one. Both are retracted together as part of this rebuild." (Rev1, lines 36-38)

> "Retracted alongside Rev1 as part of the v2 hardening rebuild. Rev2 corrected nothing about the pricing arithmetic, PM/QA/documentation omission, missing clawback, or the go-live-anchored term." (Rev2, lines 3-5)

Both notices are framed throughout as an internal repository record — `manifest.yaml` logging, defect enumeration against `known-defects.md`, instruction not to use as a template. Neither notice states, or implies, that a correction, retraction, or notice of any kind was communicated to the client. The phrase "was never corrected and sent to the client at the time" describes the document's own history, not an outbound communication about the retraction.

**Git history**: both `RETRACTION-NOTICE.md` files, like the revision documents themselves, show a single commit — `a405109 2026-08-03` — the same squashed initial-import pattern as VGE. Git cannot independently corroborate when Rev1/Rev2 were actually issued, retracted, or (if ever) communicated about; only the documents' own text states dates, and the retraction notices state no date for the retraction itself.

**What the repo cannot establish (MRD, mirroring the VGE list)**:
- Whether either revision was actually transmitted to the client.
- Whether either revision was countersigned.
- Whether SGC's accounting recognised revenue against the (here, effectively full) unsecured build value.
- Whether the client was ever informed that Rev1/Rev2 were retracted, defective, or superseded — the retraction notices read as internal-only artifacts with no addressee.
- The actual date the retraction occurred (only "as part of the v2 hardening rebuild" is stated, no date).

**Contrast with VGE, stated plainly**: MRD's defect is already named in `known-defects.md` (#8) and the documents carry retraction notices; VGE's does not and do not. But "internally retracted" is not the same fact as "client informed" — the repo has no evidence of the latter for either client. Two clients, not one, currently sit in the state: *issued, deferred/unsecured, defective on clawback, no repo evidence the client was ever told.* That is a pattern, not an isolated incident, and is handed to counsel as such below.

## Three factual questions for counsel — restated to cover both clients

1. Do SGC's records (email, CRM, or signature platform, outside this repository) show that VGE-2026-SUB-01 Rev1/Rev2 and/or MRD-2026-SUB-01 Rev1/Rev2 were transmitted to and/or countersigned by their respective clients, and if so, on what dates?
2. Has SGC recognised or invoiced any revenue against the deferred/unsecured amounts implied by any of these four documents (VGE: ≈AED 51,903 / ≈AED 81,765; MRD: the full stated build value, ≈33 hours × AED 690/hour ≈ AED 22,770, per each revision), and if so, under what terms was that revenue secured absent visible clause text in the client-held documents?
3. For MRD specifically: was Von Geyern's counterpart at Meridianview Realty ever informed, in any form, that Rev1 and/or Rev2 had been retracted or superseded — and if not, what is that client's current understanding of which document (if any) governs their relationship with SGC?
