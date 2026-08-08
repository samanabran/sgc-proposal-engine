# Internal review request — Kallat correction notice (decision #9)

**For:** Bran. **Chain:** Bran reviews and stamps → John signs → back to
Bran for final go-ahead → Sadique. **Signatory:** [HANDOVER.md §2
decision #10, not yet recorded: is Johnny Gurrera the "John" in the
stamp-SDR-John-stamp sequence?] — an intervening question-and-answer in
this session incorrectly inferred "yes" from a chat answer; withdrawn.
Nothing goes to Sadique Abbas, and no DocuSeal envelope is prepared,
until that full sequence completes.

**Send path: DocuSeal — amended 2026-08-08, prerequisites below still
unmet, none built this pass.** This file is the review mechanism, not
the send mechanism — it's how Bran reads and stamps the letter, the
same role a Gmail draft would have played (Gmail was tried for that role
two rounds ago and stopped — HANDOVER.md §14.6, both draft ids recorded
there, marked superseded, history unedited). The intended dispatch
mechanism once the chain clears is DocuSeal, matching how Prosper's
Rev3 internal review moved. **That path is not usable for Kallat today**
— see "DocuSeal prerequisites" below for exactly what's missing, checked
live, not assumed. Nothing built to close the gap this pass: no Kallat
script variant, no run, no `ALLOWED_CLIENTS` change.

## DocuSeal prerequisites — what would have to be true, checked live, not assumed

Checked directly against the repo and the connected DocuSeal account
this session (`search_templates`, `search_documents` — read-only, no
template created, nothing sent), not written on the assumption that a
working Kallat path exists:

1. **No Kallat template found on an account whose identity is
   unverified — downgraded 2026-08-08, decision #11.** `search_templates("Kallat")`
   and `search_templates("KP-2026")` both returned empty via the
   MCP-connected `mcp__docuseal__*` tools; `search_templates("2026")`
   returned exactly two templates, both Prosper's:
   `PRO-2026-SUB-01_Rev3_Proposal` (id 3) and
   `PRO-2026-SUB-01_Rev3_Offer_InternalReview` (id 2). But a separately
   supplied API token for the same host (`docuseal.sgctech.ai`,
   confirmed matching `10-signature/deploy-docuseal/.env`'s
   `DOCUSEAL_API_TOKEN`) returned zero templates and zero submissions on
   the identical query — a different token than the one the MCP tools
   use (`C:\Users\USER\.claude.json`, `mcpServers.docuseal`). Same host,
   two tokens, two different visible states, not reconciled — see
   decision #11 (HANDOVER.md §2). Absence of a Kallat template proves
   nothing until that identity question is settled; stated as "not
   found on an unverified account," not as "doesn't exist."
2. **The closest existing script doesn't reach DocuSeal at all.**
   `freeze_for_docuseal.py` (Prosper's copy, read in full two rounds ago)
   is entirely Prosper-specific (hardcoded paths/filenames) and contains
   no DocuSeal API call, template ID, or account reference anywhere — it
   only freezes local HTML to a hashed PDF. The actual DocuSeal
   submission step, for Prosper or anyone else, isn't in that file and
   wasn't investigated further.
3. **No HTML rendering of the correction letter exists.** It lives only
   as Markdown (`03-draft/KP-2026-SUB-01_CorrectionNotice_Draft1.md`).
   `assemble_and_render.py` (Kallat's only render script) assembles the
   13 numbered proposal sections, not this letter. Nothing to submit to
   a template even if one existed.
4. **No signer-role mapping exists.** Grepped `10-signature/` in full for
   `bran@sgctech.ai` and `john@sgctech.ai` — zero matches. The
   Bran-stamps/John-signs/Bran-final-go-ahead chain isn't configured
   anywhere as DocuSeal signer roles; it would need to be built into
   whatever template gets created.
5. **SMTP/dispatch status for the DocuSeal instance is contested, not
   confirmed.** `10-signature/deploy-docuseal/README.md` states SMTP is
   configured via Resend, then immediately hedges: "Not yet confirmed by
   an actual sent [email]." A separate, earlier check (this session's
   own memory, not independently re-verified this pass — no
   settings-check tool available here) found SMTP not actually
   configured, contradicting the README. Not resolved either way.
6. **Signature block is blank — decision #10.** A DocuSeal envelope
   needs a named signatory field. Nothing can be prepared until that row
   is recorded.
7. **Both addresses sit behind decision #8.** `bran@sgctech.ai` and
   `john@sgctech.ai` are on the domain the mail-access question (#8,
   still open) is about. The send mechanism runs directly through the
   same access question the Gmail path did — moving to DocuSeal doesn't
   route around it.

All seven are prerequisites, not objections to argue past — none are
being worked this pass. Decisions #8 and #10 are the two that are
explicitly yours to clear; the rest (template, HTML render, signer-role
config, SMTP confirmation) are build/verification work nobody has done
yet, for Kallat specifically.

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

**Precision on what this means, narrower than "never cleared end-to-end"**:
ground 1 (`ALLOWED_CLIENTS`) is an allowlist — it fails Kallat before
grounds 2–4 are ever load-bearing. That means the substantive checks (T12
headcount, T12 unrequested scope, T12 segment) have never once been the
thing actually holding this deal back — the allowlist has always gotten
there first. Practical consequence: **if anyone ever adds Kallat to
`ALLOWED_CLIENTS` to unblock a render, three checks that have never run
to green against this client's real data become the only thing standing
between Kallat and a render** — not three checks with a track record of
catching problems here, three checks that have simply never been tested
against this deal because ground 1 always short-circuited first.

**Decision, recorded here**: nobody adds Kallat to `ALLOWED_CLIENTS` —
not to test, not to render this correction letter. This letter ships, if
and when Bran approves it, as a **hand-reviewed document outside the
render path entirely** — it is not going to touch `review_stamp_check()`
or `pre_render_gate()` before going to Sadique, because those gates are
not going to be opened for Kallat to let it. That needs to be explicit
and on record, because otherwise this becomes a client-facing artifact
that never touched the gate and nobody wrote that down — exactly the
"ungoverned document" failure shape this repo has flagged elsewhere
(HANDOVER.md §11), just self-aware about it this time instead of
discovered after the fact.

## How were the quarantined Kallat renders actually produced?

Checked directly, not assumed. `04-draft/_quarantine/KP-2026-SUB-01_Rev1_Internal.html`
and `.pdf` were produced by
`02-clients/KP-kallat-properties/04-draft/assemble_and_render.py` — a
**separate, standalone script**, unrelated to `render_r11_r12.py`. It
reads the 13 section files directly from
`03-draft/KP-2026-SUB-01_Rev1/*.md`, converts them with its own small
markdown-to-HTML function, and writes straight to
`04-draft/KP-2026-SUB-01_Rev1_Internal.html`/`.pdf` via Playwright. Read
the whole file: it imports nothing from `render_r11_r12.py`,
`test_pricing_engine.py`, or `pricing_engine.py` — no `ALLOWED_CLIENTS`
check, no `review_stamp_check()`, no T10/T12 gate, nothing. It's run by
hand (`python assemble_and_render.py`) by anyone with repo access and
Playwright installed, whenever they choose.

Timing rules out "there was a window when the allowlist was open":
`assemble_and_render.py` was added 2026-08-05 (commit `525940d`);
`ALLOWED_CLIENTS` didn't exist until the next day, 2026-08-06 (`b3e8cd3`),
and has been MRD-only since the moment it was created. There was never a
time the allowlist included Kallat — it's simpler and worse than that:
**Kallat's renders were never subject to that gate at all**, because
they go through a completely different pipeline that has no gate of its
own. Confirms your hypothesis directly: the gate's coverage is nominal —
`render_r11_r12.py` governs only its own pipeline, and Kallat's actual
client-shaped artifacts were, and still can be, produced entirely
outside it.

**Is the quarantine set the full population?** Checked, as of 2026-08-08:
a repo-wide search for any `KP-2026-SUB-01`-named file outside
`02-clients/KP-kallat-properties/` found nothing; `git status` shows no
untracked Kallat files anywhere; the live `04-draft/` directory
(outside `_quarantine/`) contains only the script itself and
`_review-stamp.yaml`, no stray render. So as a snapshot, yes — the
population already grepped (`03-draft/` plus `04-draft/_quarantine/`) is
complete, and the per-user-figure finding stands as reported. **This is
a snapshot fact, not a structural guarantee**: `assemble_and_render.py`
is live and re-runnable at any moment by anyone, independent of any gate
in this repo. One mitigating detail, checked rather than assumed: its
markdown converter handles `**bold**`, headers, tables, and blockquotes,
but not `~~strikethrough~~` — so if someone re-ran it today, the tildes
around the superseded row would print literally rather than rendering as
strikethrough, but the bold "**SUPERSEDED 2026-08-08 — DO NOT QUOTE**"
text and the blockquote banner at the top of
`07-options-inclusions.md` would both render correctly and stay visible.
The annotation would survive a re-render; the gate around whether a
re-render should happen at all still doesn't exist.

A fresh, hash-matched `04-draft/_review-stamp.yaml` entry is required
before this letter is ever send-ready through the governed path — moot
for this specific letter per the decision above, since it isn't taking
that path, but still the standard for anything that does.
