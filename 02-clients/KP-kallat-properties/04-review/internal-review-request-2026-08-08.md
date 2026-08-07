# Internal review request — Kallat correction notice (decision #9)

**For:** Bran. **Routing:** Bran review → [signatory — pending, see open
item below] → back to Bran for final instruction to send. Nothing goes
to Sadique Abbas until that full sequence completes.

**No longer using Gmail drafts for internal routing on this deal** — this
replaces what would have been a third draft in a mailbox already
confirmed unreliable for Kallat/Prosper correspondence (HANDOVER.md
§8.1). This file is the review request; the letter itself is at
`03-draft/KP-2026-SUB-01_CorrectionNotice_Draft1.md`.

## What this is

The written correction decision #9 (manifest.yaml, 2026-08-07) called
for, addressing verbal exposure from the 16 July discovery/demo call —
three items demoed live with no catalogue basis (commission calc,
payment auto-reconciliation, landlord/client portals), the unqualified
"completely implausible" cybercrime claim, and the portal
accreditation/fee overstatement.

## Two things need your input before this can move to the next step

1. **Signatory.** manifest.yaml's own "stamp-SDR-John-stamp" phrasing
   doesn't establish whether that "John" is Johnny Gurrera in a more
   formal capacity than his headcount-question lane, or a distinct
   second person. Left unsigned in the letter rather than guessed.
2. **Security paragraph.** Rewritten as a pure retraction of "completely
   implausible" — states only what's already on record (Priority SLA
   tier) and invents nothing new. Flagging explicitly: this is a
   commercial judgment, not a legal one. If it needs to hold up in a
   dispute, it should go to counsel before it goes to Sadique.

## Also surfaced this pass — not part of this letter, but relevant

Grepping the full Kallat draft set for a leaked per-user figure (the
check decision #9 actually needs) found one:
`03-draft/KP-2026-SUB-01_Rev1/07-options-inclusions.md:10` — "AED
250/user/month" for "Additional users beyond 40." Stale against the
2026-08-05 v3.0 pricing model, which deleted that exact line item. It's
in the live, non-quarantined draft path, not the quarantined render, so
it isn't caught by `04-draft/_quarantine/NOTICE.md`. **Decision #9 is
reopened by this finding** — full detail in manifest.yaml's 2026-08-08
entry. Not fixed here (Stage 5 pricing content, out of scope for this
letter and for the still-held Stage 5) — flagging so it doesn't get
missed when Stage 5 resumes.

## Provenance for the corrected figures

AED 3,900 (Property Finder) and AED 3,400 (Bayut + Dubizzle combined):
`00-knowledge/pricing/phase2-catalogue.yaml` v2.1, effective_from
2026-08-05, items `portal_sync_property_finder` and
`portal_sync_bayut_dubizzle`. Governed rate card, versioned and dated —
not memory, not a live lookup.

## Review gate

Checked against the actual `review_stamp_check()` code
(`05-ops/render_r11_r12.py:104-132`) rather than assumed: `03-draft/` is
inside its `REVIEWED_MATERIAL_SUBPATHS`, so this letter was never
outside the gate — the check is commit-hash-based, not location-based.
The existing 2026-08-07 stamp was already invalidated by later commits
before this session started; Kallat has been correctly refused as
send-ready since 2026-08-07. Also: `ALLOWED_CLIENTS` in that script is
`["MRD-meridianview-realty"]` only, so Kallat can't render through
R11/R12 at all right now, independent of the stamp.

A fresh, hash-matched `04-draft/_review-stamp.yaml` entry is required
before this letter is ever send-ready, once you've reviewed it.
