# Internal review request — Kallat correction notice (decision #9)

**For:** Bran. **Routing:** Bran review → Johnny Gurrera (confirms
commitment, signs — the stamp-SDR-John-stamp sequence, distinct from his
un-gated headcount-question lane) → back to Bran for final instruction
to send. Nothing goes to Sadique Abbas until that full sequence
completes.

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

## One thing still needs your input

1. **Portal delivery confirmation.** The letter states the AED
   3,900/3,400 integration fee and explains why no SGC accreditation is
   needed (client holds the portal-side access; SGC builds the sync
   against it — `phase2-catalogue.yaml`'s own dependency model). What it
   does NOT claim is that this has been delivered before: no file in
   this repo records a completed portal_sync instance for any client
   (VGE, MRD, PRO are all still at DEFERRED/proposal stage). If you know
   of a completed instance outside this repo, worth adding before send —
   not assumed here.

Security paragraph is now a strict two-sentence retraction (no
substitute claim) and the "everything at your disposal" tension is left
alone entirely, per your last round's instructions — no open question on
either of those.

## Also surfaced this pass — not part of this letter, but relevant

Grepping the full Kallat draft set for a leaked per-user figure (the
check decision #9 actually needs) found one:
`03-draft/KP-2026-SUB-01_Rev1/07-options-inclusions.md:10` — "AED
250/user/month" for "Additional users beyond 40," pairing the per-user
rate we're not supposed to charge with the unsourced 40-headcount figure
in the same line. Stale against the 2026-08-05 v3.0 pricing model, which
deleted that exact line item. **Decision #9 is reopened by this
finding** — full detail in manifest.yaml's 2026-08-08 entries. Quarantined
in place today (not deferred to Stage 5): the row is struck through and
marked SUPERSEDED inline, with a NOT SEND-READY banner at the top of the
file, so it can't go out by accident during the gap. The actual pricing
fix (replacing it with the current Class A-D model) is still Stage 5
work, still held.

## Provenance for the corrected figures — fully reconciled

AED 3,900 (Property Finder) and AED 3,400 (Bayut + Dubizzle combined):
`00-knowledge/pricing/phase2-catalogue.yaml` v2.1, effective_from
2026-08-05. `git log -p` confirms these two figures were actually added
2026-08-03 (commit 1633e44, v2.0) and untouched by the 2026-08-05 change
— that change (commit 525940d) only touched the `additional_user` /
onboarding-fee block. Two separate version numbers exist because two
separate files were touched by one commit: `policy.yaml` is at v3.1
("v3.0" = the 2026-08-05 overlay deletion), `phase2-catalogue.yaml` is
at v2.1 — the catalogue's own "(v3.0)" comment cites policy.yaml's
change as the reason, not its own version. No phase2-catalogue.yaml
existed before 2026-08-03 (the repo's first commit is that date), so
there was no rate card at all on 2026-07-16 when the call being
corrected happened — this letter states SGC's current position, not
what was secretly true in July (wording changed accordingly: "our
current position is different," not "that's not accurate"). Same
figures, same dependency note, appear identically for VGE, MRD, and
PRO — a repo-wide governed rate, not Kallat-specific.

Accreditation vs. fee: reconciled via the catalogue's own
`portal_dependency_note` — the fee is for SGC's build labor, contingent
on the *client's* own portal subscription including feed/API access.
SGC never needs its own portal accreditation under this model. Checked
and not claimed: no completed portal_sync delivery is recorded in this
repo for any client — flagged above as something only you'd know.

## Review gate — re-verified by running the actual code, not just reading it

```
review_stamp_check('KP-kallat-properties') -> refuses (stamp hash mismatch)
pre_render_gate('KP-kallat-properties')    -> refuses, 4 independent reasons
  (ALLOWED_CLIENTS, T12 headcount, T12 unrequested scope, T12 segment)
review_stamp_check('MRD-meridianview-realty') -> refuses (no stamp file exists)
```

`ALLOWED_CLIENTS = ["MRD-meridianview-realty"]` only, set 2026-08-06
(commit b3e8cd3) and unchanged since — Kallat cannot render through
R11/R12, independent of stamp status. This doesn't conflict with
`CHANGELOG.md:1953`'s "Kallat's stamp passes clean" — that note is about
`review_stamp_check()` alone, snapshotted the day the stamp was written
(commit 025dc08), before this session's edits invalidated it. Two
different, independent gates, both statements true at their respective
times.

A fresh, hash-matched `04-draft/_review-stamp.yaml` entry is required
before this letter is ever send-ready, once you've reviewed it.
