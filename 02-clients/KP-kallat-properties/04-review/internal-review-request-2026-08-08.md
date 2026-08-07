# Internal review request — Kallat correction notice (decision #9)

**For:** Bran. **Routing:** Bran review → [signatory — HANDOVER.md §2
decision #10, not yet recorded: is Johnny Gurrera the "John" in the
stamp-SDR-John-stamp sequence?] → back to Bran for final instruction to
send. Nothing goes to Sadique Abbas until that full sequence completes.
The correction notice's signature block currently carries no name —
your earlier chat instruction was that Johnny is not the signatory here,
which an intervening question-and-answer in this session incorrectly
overrode; withdrawn, see decision #10.

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

## Two things need your input

1. **Signatory — HANDOVER.md §2, decision #10 (added 2026-08-08).** Is
   Johnny Gurrera the "John" in manifest.yaml's "stamp-SDR-John-stamp"
   sequence? No file in this repo answers it. This is a fact about SGC's
   own people — record it in that row on your next pass, not something
   further search here can resolve.

2. **Commercial risk: undelivered portal integration.** No file anywhere
   in this repo records a completed portal_sync instance for *any*
   client — VGE, MRD, and PRO are all still at DEFERRED/proposal stage.
   `phase2-catalogue.yaml`'s dependency note resolves the accreditation
   contradiction (SGC needs none — the client holds portal-side access,
   SGC builds against it), but it's governed provenance for the *number*,
   not evidence the number covers labour SGC has ever performed. This
   letter's purpose is correcting a previous under-quote; putting an
   unproven catalogue rate into that same letter as a written,
   client-facing price risks repeating the pattern it exists to fix. The
   letter now frames the figures as the *current catalogue rate*, not a
   stated fixed cost for demonstrated work — but the underlying risk
   (has this integration ever actually been built, by anyone, under
   current access terms?) is not resolved by that wording change and
   needs your call before this goes to Sadique.

Security paragraph is now a strict two-sentence retraction (no
substitute claim) and the "everything at your disposal" tension is left
alone entirely, per your prior round's instructions — no open question on
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

`pre_render_gate('KP-kallat-properties')` returns `False` with **four
independent reasons**, run live 2026-08-08 (not inferred from reading
the source):

1. **Not in `ALLOWED_CLIENTS`.** That list is `["MRD-meridianview-realty"]`
   only, set 2026-08-06 (commit `b3e8cd3`, "Add R11/R12 renderer, scoped
   to MRD only") and unchanged since. Kallat has never been eligible to
   render through R11/R12 — this predates everything else on this list.
2. **T12 headcount unsourced.** `users_now=40` re-affirmed UNSOURCED
   2026-08-07 (Bran, direct ruling) — Sadique's own answer ("approximately
   40 or 15, approximate") is double-hedged and off-the-cuff, and Kallat
   is a multi-business group, so even a precise number wouldn't establish
   which entity it counts. Hard block, unchanged by this pass.
3. **T12 unrequested scope.** AED 19,652 of the quoted build value (35.0%)
   comes from 4 work packages — `discovery`, `invoicing_trn`,
   `property_unit_register`, `tenancies_contracts_reminders` — not in the
   client's brief and with no `approved_scope_exceptions` field recording
   authorization. The client is being billed for scope with no record of
   having asked for it.
4. **T12 segment classification depends on the unverified headcount.**
   The `mid_market` segment (and the rate that follows from it) rests on
   `users_now`, which check 2 above has never cleared — so the segment
   itself is unverified, not just the headcount number in isolation.

Plus a fifth, independent of all four: the review stamp itself is
invalid (`reviewed_commit` doesn't match the current commit touching
reviewed material). `review_stamp_check('MRD-meridianview-realty')` also
refuses right now — but for a different reason again: no
`_review-stamp.yaml` file exists for MRD at all.

**What this means plainly**: Kallat has never once cleared this gate.
Anything described elsewhere in this repo's history as "verified,"
"clean," or "passes" for Kallat refers to one sub-check in isolation at
one point in time (e.g. `CHANGELOG.md:1953`'s "Kallat's stamp passes
clean," which was `review_stamp_check()` alone, snapshotted at commit
`025dc08`) — never the full gate, and never a real render. `ALLOWED_CLIENTS`
being MRD-only predates that snapshot and made the full gate a fail
throughout, independent of stamp status. Two different, independent
gates, both statements true at their respective times — not a
contradiction, but also not evidence anything on Kallat has ever
actually rendered clean end-to-end.

A fresh, hash-matched `04-draft/_review-stamp.yaml` entry is required
before this letter is ever send-ready, once you've reviewed it — and
even then, `ALLOWED_CLIENTS` would need to be widened before Kallat
could render through this pipeline at all, which is out of scope here.
