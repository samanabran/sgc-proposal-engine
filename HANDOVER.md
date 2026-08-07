# MRD-2026-SUB-01 — Handover Register

**As of 2026-08-06.** This file assembles findings already produced across
this session's audit passes — it contains no new analysis. Where a claim
needed a one-line verification to state accurately, that's noted inline;
nothing here required opening a new investigation thread.

**Headline: MRD is not clear for issue, independent of any gate/check
status.** See §1 below — no artifact in this repo, and no artifact found
by this session's mailbox search, documents that the client was ever
told Rev1/Rev2's figures were wrong. **That mailbox search is now known
to be unsafe — see §13: it searched `scholarixglobal@gmail.com`, which
is not where this deal's client correspondence lives.** Not established
either way, not ruled out. On the evidence this repo can actually stand
behind (its own files), the client's last communicated understanding is
still AED 879/month — that part doesn't change, only the confidence
behind "no retraction exists anywhere" does.

---

## 1. Per-client status

### MRD-meridianview-realty

| Revision | Issued | Headline monthly figure | Status |
|---|---|---|---|
| Rev1 | 2026-06-15 | AED 879/mo | Retracted (repo-internal only — see below) |
| Rev2 | 2026-07-02 | AED 879/mo (unchanged from Rev1 — only the VAT clause differs) | Retracted (repo-internal only) |
| Rev3 | Not issued (`issued_date: ""`) | AED 1,680/mo, Year-1 AED 25,440, 24-month total AED 45,600 | Draft, all 41 gates pass |

**Retraction evidence, stated plainly**: `05-issued/MRD-2026-SUB-01_Rev1/RETRACTION-NOTICE.md`
and the Rev2 equivalent exist and are thorough — but they are internal
engineering post-mortems (defect lists, written as part of this rebuild).
**Neither records a date or a channel by which the client was told Rev1
or Rev2 was withdrawn.** No email log, no call note, no client-facing
correction exists anywhere in this repo's own files.

**The mailbox-search leg of this finding is downgraded, not reversed
(2026-08-07 — see §13).** This session's negative Gmail search results
all came from `scholarixglobal@gmail.com`, an account now confirmed to
not be where this deal's client correspondence lives (§13's SMTP-header
evidence points at `mail.sgctech.ai`/SOGo). **Correct statement: "no
retraction artifact found" is NOT ESTABLISHED as "no retraction artifact
exists" — the search covered this repo's own files (still solid) and one
Gmail account (not solid, wrong mailbox).** Per the instruction that
prompted this check, the practical conclusion is unchanged for now — MRD
is still not clear for issue on the evidence actually in hand — but the
reason has narrowed: it's not "no retraction exists," it's "this repo
cannot currently prove one does or doesn't." A read path to
`mail.sgctech.ai`/SOGo (§13, §2 decision #8) is the one thing that
resolves this cleanly either way.

**Current gate/check status (Rev3, in-repo only)**: all 41 pricing gates
pass (manifest.yaml). Renderer (R11/R12): T10, T12, spec-binding,
legal-identity, and all four T11 sub-checks (drift, label-binding,
reconciliation, display-name) pass. `validate.py`'s
`check_r11_r12_deliverables` fails by design (globs `*.pdf`, we emit
Markdown — logged as an open question, §3). `issue_promotion_gate()`
reports exactly one remaining blocker: `manifest.yaml` `issued_date` is
empty. The signature-block RESOLVE blocker is fixed (commit `21c843e`).

**Blockers to issue, in order**: (1) resolve the Rev1/Rev2 client-notice
gap above — either produce the missing evidence or treat this as a live
correction, not housekeeping; (2) a human sets `issued_date` and sends;
(3) PDF-vs-Markdown question (§3) if PDF is the required deliverable
format.

### KP-kallat-properties

Zero issued revisions — `manifest.yaml` lists one revision entry
(`KP-2026-SUB-01_Rev1`) with `issued_date: ""`; `05-issued/` contains
only `.gitkeep`. Current draft (`03-draft/KP-2026-SUB-01_Rev1/`, this
*is* the current revision, status `draft`) is stale against its own
worksheet by a wide margin (mobilisation printed AED 48,686 vs. current
AED 22,429) — see the prior session's cross-client count. T10: 3/3 pass.
T12: 2 of 3 assertions fail (`users_now` unsourced; billing-exposure
scope padding, AED 19,652 — see §2). Not rendered by R11/R12
(`ALLOWED_CLIENTS` is MRD-only). No work performed on this client's
figures this pass beyond the earlier read-only count.

**Updated 2026-08-07** — the stale 04-draft render is now quarantined
(`04-draft/_quarantine/`) and `02-calc/gate-report.md` is marked
SUPERSEDED in place; `02-calc/risk-assessment.yaml:18`'s citation is
corrected (value/band unchanged, still `raw_score: 52`, `elevated`);
`validate.py` gained check_19 (internal-vocabulary leak — Kallat's
`03-draft/` currently fails it, correctly, on 3 hits). Unlike Prosper's
T12, **Kallat's T12 stays hard-blocking — no non-blocking rationale, no
illustrative figure** — see §12. Also now a confirmed instance of §11's
ungoverned-PRJ-anchor class (SGC-KP-2026-07, sent 2026-07-23).

### PRO-prosper-realestate

Zero issued revisions of this repo's own SUB-model — same pattern as
Kallat (`PRO-2026-SUB-01_Rev1`, `issued_date: ""`, `05-issued/` empty).
Current draft stale against its own worksheet (mobilisation printed AED
38,544 vs. current AED 22,002). T10: 3/3 pass. T12: 2 of 3 assertions
fail (`users_now` unverified; same-pen scope match, not independently
corroborated — no billing exposure, since 8/8 packages match the brief).
Not rendered by R11/R12.

**Added 2026-08-06, same shape as MRD's finding above**: this repo's own
SUB-model was never sent — but a *different*, ungoverned document was,
and the client has already rejected it. **The client's only live
commercial understanding of "SGC's price" rests on a document no gate in
this repo has ever inspected**: "PROSPER x SGC Implementation Proposal -
2026" (CRM attachment 5306), sent 22 Jul 2026 09:44 UTC, quoting AED
45,000 fixed Phase 1 + AED 1,450/mo mandatory Platform Care Plan at AED
690/hr and AED 650/hr — both on `rate-card.yaml`'s forbidden-rates list
(`rate-card.yaml:37`, `:52`). Rejected 27 Jul 2026: *"the cost is
currently too high for us, and we are not planning to use a CRM at the
moment"* (`00-intake/_source-documents/
email-2026-07-27_rejection_fwd-2026-07-28.eml`). **Client holds figures
we no longer stand behind — same framing as MRD's AED 879/month, but
where MRD's stale figure is this repo's own prior work, Prosper's stale
figure was never this repo's to begin with.** Worse: even this repo's
most stripped-down traceable-scope configuration (AED 67,086 Year-1, see
`manifest.yaml` 2026-08-06 entry) still prices above what was already
rejected as too expensive (AED 60,950–62,400 Year-1). Trimming scope
alone does not close this gap.

### VGE-vongeyern-realestate

**Two issued revisions**, both status `superseded` (not `retracted` —
their own manifest notes say they were "built from invented data,"
i.e. placeholder figures from before real client facts were gathered):
Rev1 (2026-06-15, AED 7,681/mo Option A) and Rev2 (2026-07-10, AED
8,311/mo Option A). Current Rev3 draft (not yet issued) uses the brief
§3-pinned real figures: AED 4,900 mobilisation, AED 1,650/mo
subscription. **Noted in passing (not chased further)**: VGE's own
`03-draft/VGE-2026-SUB-01_Rev3/10-commercial-terms.md` shows mobilisation
AED 27,255 — this is not a fresh drift, it's Rev2's already-superseded
mobilisation figure, meaning this file may never have been updated past
a Rev2 copy at all. T10: mobilisation is a HARD FAIL (stored 4,900,
derived 4,884, uncited). T12: scope-match fails (7/7 packages
undocumented against an empty brief request list — delivery-commitment
exposure, not billing, AED 7,562).

---

## 2. Human-owned decisions

Each needs a named owner and is resolved by exactly one external
artifact or answer — not by more in-repo analysis.

| # | Decision | Owner | Single resolving document/answer |
|---|---|---|---|
| 1 | Kallat: is the AED 19,652 unrequested-scope delta (4 packages, 35% of quoted build value) authorized, and is `users_now=40` real? | ______ | A written client confirmation (email/chat) naming the 4 extra packages as agreed, OR a scope trim to the 4 originally-requested packages. Separately: any timestamped client-side statement of headcount (both call transcripts are internal-only or lack a figure). |
| 2 | VGE: is the brief-pinned AED 14,800 Implementation Value / AED 1,650 Subscription Fee (and the four figures downstream of it) a deliberate, client-confirmed quote, or an authoring artifact? | ______ | The original brief document itself (not in this repo — `01-source/README.md:1`: "No raw client materials were provided") or a client-side re-confirmation at Rev3 issue. |
| 3 | Prosper: is `users_now=31` (CRM Lead 8407's `x_employee_count`) an accurate, current headcount? | ______ | Direct confirmation from Louai Khzam (Owner) or Dian Sajulga (authorized operational contact), in a timestamped medium. |
| 4 | MRD: what is Rev1/Rev2's actual retraction status vis-à-vis the client? **Updated 2026-08-07**: this repo's own files show no correction; a Gmail search of `scholarixglobal@gmail.com` also found none, but that account is confirmed (§13) not to be where this deal's correspondence lives — the Gmail leg is not established, not a real "checked, clean" result. | ______ | Evidence of the correction communication (if one happened, likely on `mail.sgctech.ai`/SOGo per §13 — see decision #8) — or, if none exists, a decision on whether Rev3's issue must be framed as a price correction rather than a first quote. |
| 5 | Prosper: the client's only live commercial understanding rests on a document (attachment 5306, AED 45,000 + 1,450/mo, forbidden rates) that no gate in this repo has inspected, and it was already rejected on cost. Even the most stripped-down traceable-scope reconfiguration (AED 67,086 Year-1) still prices above the rejected figure (~AED 61,000). | ______ | A decision on commercial strategy before any further client-facing work: whether to pursue a Must Have-only build (pending scope-removal authorization — none of the 7 gaps are priceable regardless), a different rate/margin structure, or hold. Not resolvable by more in-repo analysis — the unit economics (structural overlays + 18% financing uplift) are the actual driver, not the per-hour rate or scope size — see §8 below. |
| 6 | Prosper: attachment 5306 (the actual rejected PRJ document) could not be retrieved this session — see §8. **Updated 2026-08-07**: the retrieval attempt searched `scholarixglobal@gmail.com`, now confirmed (§13) not to be the mailbox this thread lives in — "not retrieved" was never "not retrievable." Every PRJ figure used in this repo's comparisons (AED 45,000, 1,450/mo, the 690/650 rates, the Care Plan start month) remains a secondhand account, not a verified extraction. | **Talha Sheraz** | Named human action, not a dead end: the thread lives on SGC's own mail server (`mail.sgctech.ai`, SOGo webmail) in **Talha's own mailbox** — the sender of record on both the 22 Jul send and the 27 Jul rejection reply. Artifact to produce: "PROSPER x SGC Implementation Proposal 2026," CRM attachment 5306, sent 22 July 2026 09:44 UTC. Every PRJ figure stays UNVERIFIED until produced. See decision #8 — a general mailbox read path may make this individual ask unnecessary. |
| 7 | Prosper: the platform/CTS floor (AED 3,648/mo, headcount-driven, `policy.yaml:70-87`) does not move when scope is cut — see §8.5. At the theoretical limit of zero build value, the floor alone over 24 months (AED 87,552) still exceeds the PRJ document's entire 24-month figure (~AED 79,800, itself unverified per #6). No configuration this repo is authorized to build can beat the rejected number on price. | ______ | A pricing-model decision (rate, uplift, or platform-floor structure) — explicitly out of this pass's constraint. See §9 recommendation. |
| 8 | **Highest-value open item (added 2026-08-07, §13).** Client correspondence for these deals lives on `mail.sgctech.ai` behind SOGo webmail, not in the `scholarixglobal@gmail.com` account this session is connected to (confirmed by the attachment-5306 rejection reply's own SMTP headers, §8.1/§13) — and possibly also not in `renbranmadelo@gmail.com`, the account this session's own setup notes as intended but never actually connects to. Every negative finding in this repo built on a Gmail search (MRD's retraction search, decision #4; Prosper's attachment-5306 search, decision #6) is unsafe until this is resolved — both are downgraded to "not established," not reversed, pending it. **Known unknown riding on the same access (added 2026-08-07, owner Bran): an unidentified 32-minute Otter recording, 2026-07-16 4:13pm, sitting between the Kallat discovery call and the internal prep call, matches no transcript in this repo (§14) — could be internal or client-present, undetermined. Not pursued beyond flagging it; resolves with whatever gives read access to the real record of that day, same as the rest of this row.** | **Bran** | A read path (webmail login, IMAP, or an export) to `mail.sgctech.ai`/SOGo — or confirmation of what `renbranmadelo@gmail.com` actually contains, if that's the intended account. Resolving this potentially unblocks MRD outright (if a retraction communication exists there), recovers attachment 5306 directly without needing Talha specifically (decision #6), and identifies the 4:13pm recording above. |
| 9 | **Kallat — RESOLVED IN PRINCIPLE by Bran 2026-08-07, blocked in practice on drafting the correction (not requested yet).** On a client-present call (2026-07-16), Sadique was told, as a differentiator: "Our system, when you pay for it, you have everything at your disposal... right from the get go." **Ruling: the per-user promise is the smaller half of the exposure** — the gap register (§14.3: commission calc, payment auto-reconciliation, landlord/client portals, all demoed live, none in the catalogue) contradicts "everything right from the get-go" far more sharply than any seat-band structure would. A written correction to Kallat is required regardless of pricing shape, and must land before or with the price, never after. **Pricing shape follows from that**: flat monthly, no per-user rate anywhere in the document, no per-user derivation even as a labelled illustration, capacity stated as an operational ceiling rather than a pricing tier. Honours the "everything from the get-go" promise, bounds seat exposure across an unknown number of Kallat Group entities without needing headcount precision, and doesn't require walking back the one thing Sadique was told most emphatically. | **Bran** | The written correction to Kallat (addressing the gap-register features and the per-user framing together) — not drafted this pass, not requested yet. Once drafted, this decision is fully closed; the pricing *shape* itself needs no further decision. |

---

## 3. Open questions

- **PDF generation vs. amending `validate.py`'s R11/R12 check.**
  `check_r11_r12_deliverables` globs `*.pdf`; this pass emits Markdown by
  explicit constraint. Amending the check to accept Markdown would mirror
  the Kallat scope-padding defect from the other direction — there,
  inputs were moved to clear a check; this would move the check to clear
  an unchanged output. Needs a human: authorize PDF generation, or
  amend the check's own definition, but not both silently.
- **The 0.30 margin floor (`policy.yaml:88: gates.min_gross_margin`)
  has no stated denominator.** It carries no comment naming which of
  the two formulas in active use (build-margin vs. lifetime-commitment,
  see the prior session's CHANGELOG entry) it was calibrated against.
  Per-client G8 verdicts are therefore not comparable to each other even
  though they're checked against the same nominal number.
- **Hypercare's linear term is unbounded.** `hypercare.hours =
  ceil(N/5) × 2` has no documented ceiling — cost scales linearly with N
  forever. Not evaluated for whether that's intended at large N; flagged
  only.
- **`monthly_billing_deviation.surcharge_pct` remains uncited** to any
  `policy.yaml` field — this is why R11/R12 still withholds it (internal
  render log only, never client-facing).
- **`base_scope_hours=47` default, and the retired global
  `CHECK_4_STRUCTURAL_BREACH_N` constant.** `a_hours_for_n()`'s
  `base_scope_hours` default (47) is Kallat/Prosper's own package-hour
  total, not a policy-cited constant. `per_client_check4_breach_n()` was
  added to replace the hardcoded repo-global breach point but the global
  constant itself was never formally retired/removed — both live in the
  codebase simultaneously.
- **The internal-vocabulary scanner is a proposal, not a build.** No
  automated check currently scans client-facing output for field paths,
  commit hashes, check names, or policy filenames (the class of defect
  fixed by hand in R11/R12's Withheld-section removal). Proposed, not
  implemented.
- **13-section prose set has no renderer.** See §6 — logged there in
  full since it's this handover's largest single open item.

---

## 4. Unsourced figures register (12)

From `05-ops/audit_draft_drift.py`'s classification run (pre-fix,
15 matched / 7 stale / 12 unsourced — the 12 unsourced are unchanged by
the fixes, since nothing was done to source them). Contractual = a term
of the deal (SLA, notice period, guarantee). Descriptive = illustrative/
narrative, not itself a binding commitment.

| File:line | Figure | Contractual / Descriptive |
|---|---|---|
| `04-as-is.md:5` | AED 1,100 (lower bound of the PropSpace market range) | Descriptive |
| `01-executive-summary.md:23` | 6 weeks (timeline to go-live) | Descriptive |
| `08-implementation-recovery.md:7` | Week 1 (kickoff) | Descriptive |
| `08-implementation-recovery.md:8` | Week 2 (discovery/data validation) | Descriptive |
| `08-implementation-recovery.md:9` | Weeks 3-5 (configuration/migration) | Descriptive |
| `08-implementation-recovery.md:10` | Week 6 (training) | Descriptive |
| `08-implementation-recovery.md:11` | Week 6 (go-live) | Descriptive |
| `11-support-sla.md:7` | 24 hours (email SLA response time) | **Contractual** |
| `11-support-sla.md:13` | 5% per week / 2 months cap (go-live SLA credit terms) | **Contractual** |
| `09-partnership-terms.md:9` | 30 days (non-renewal notice) | **Contractual** |
| `09-partnership-terms.md:15` | Day 30 (adoption checkpoint) | **Contractual** |
| `09-partnership-terms.md:16` | Day 60 (adoption checkpoint, triggers the free remediation session) | **Contractual** |

5 of 12 are contractual terms with no named source anywhere in this
repo — worth a policy owner's attention ahead of the 7 descriptive ones.

---

## 5. Cross-worksheet contamination

Four instances, assembled in one place:

1. **Kallat's 4 "unrequested" packages are identical, in the same order,
   to the first 4 packages in both MRD's and VGE's worksheets**
   (`discovery`, `property_unit_register`, `tenancies_contracts_reminders`,
   `invoicing_trn`). Kallat's brief requests only `crm_leads`,
   `users_roles_agent_perf`, `reports_dashboard`, `data_migration_500`.
   No commit message or comment in this repo confirms the 4 extra
   packages' origin — the overlap is consistent with a shared template
   being copied in rather than independently derived from Kallat's own
   discovery call, but that's an inference from the data, not a
   documented fact.
2. **Prosper's `disarm_hesitation_tweaks_scope_note` narrates "Kallat —
   AED 4,900 matches their numbers"** — this figure belongs to neither
   Prosper's own worksheet (mobilisation AED 22,002) nor Kallat's
   (AED 22,429). It is VGE's `mobilisation_aed` (4,900), a third,
   unrelated client's field.
3. **A same-file hand-transcription typo in Prosper's worksheet, not
   cross-client contamination** — flagged here because it was raised as
   a contamination instance and the evidence doesn't quite support that
   framing, stated plainly rather than silently reclassified:
   `pricing-worksheet.yaml:90` (Prosper) documents that
   `total_hours_all_in`'s hypercare contribution was "mistyped into this
   sum as 5 instead of 14" during manual authoring — already corrected
   2026-08-05, and the worksheet's own comment explicitly calls it "an
   independent instance, not a shared formula bug" against Kallat's
   separate 4.0h version of the same defect class. Included per
   instruction; characterized accurately rather than folded into the
   cross-client pattern.
4. **All four clients' intake documents trace to one author across one
   or two commits.** Every commit touching every client's
   `00-intake/client-brief.yaml` is authored by `scholarixglobal-ctrl`
   (git log, checked this pass). Kallat's and Prosper's briefs were
   *both first committed in the same commit*, `525940d`. MRD's brief
   originates in `a405109`; VGE's in `cb2f194`/`6ea775b`. No file was
   independently authored by a different person or process.

**Conclusion, stated plainly: these four intake documents are not
mutually independent evidence.** A figure or scope item appearing in
one client's file being consistent with another's is not
corroboration — it may be the same authoring pass or the same template,
not two independent sources agreeing.

---

## 6. Proposal only, no build: render the 13-section prose set

The R11/R12 renderer (`05-ops/render_r11_r12.py`) reads every figure
through `pe._load()` against the live worksheet and fails the build on
drift. The 13-section prose set (`03-draft/*/`) has no equivalent — it
is filled in by hand once and never resynced, which is the entire
mechanism behind every stale figure found this session (§1, and the
prior session's 7-figure fix in commit `21c843e`). `01-templates/
proposal/` itself is clean (bracket placeholders, zero literal AED
figures) — the defect enters at fill time, not from the template.
**Proposed**: render the 13-section set the same way, from the same
`pe._load()` path, so a worksheet correction propagates automatically
instead of requiring a manual resync pass like this one, every time,
for every deal. Not implemented this pass — report only, per instruction.

---

## 7. What is fixed and committed

| Commit | Summary |
|---|---|
| `b3e8cd3` | Add R11/R12 renderer, scoped to MRD only |
| `afacd28` | Guard T11 swap risk with label binding; restate VGE exposure; add empty-comparison-set rule |
| `bd36239` | Fix MRD R11/R12 draft defects: reconciliation, internal-only withhold, spec-binding, display names, legal-identity gate |
| `4d314d6` | Disclose 24-month contract value, add reference number, gate issue-promotion; log MRD sibling-doc reconciliation |
| `3eac410` | Add report-only draft-drift audit + 04-draft hygiene gate; log exposure/provenance/margin/session-material findings |
| `21c843e` | Resync MRD 03-draft's 7 stale figures to the current worksheet; fix RESOLVE signature block |
| *(this commit)* | Correct CHANGELOG's classification/verification labeling and the `tooling_aed` overclaim; derive the SLA credit cap by reference instead of a typed figure; add this handover |

All checks green for MRD's Rev3 (renderer side). **Still not clear for
issue** — see the headline at the top of this file.

---

## 8. Prosper — attachment 5306 retrieval, per-agent finding, catalogue gap register (2026-08-06)

### 8.1 Attachment 5306 — not retrieved, every PRJ figure is now UNVERIFIED

Searched the one Gmail account this session had access to
(`scholarixglobal@gmail.com` — **not** `renbranmadelo@gmail.com` as
requested; that account is not the one connected here) for the proposal
subject, "Prosper," `prosperuae.com`, "5306," "Talha," "Sajulga," and the
22 Jul 09:44 UTC window. Found: two Otter.ai meeting-summary emails from
2026-07-17 (corroborating the *already-logged* internal demo-prep
transcript — one snippet reads "particularly employee check[-in]...",
matching that transcript's own content) and one Otter.ai email
confirming Talha's personal address is `talhasheraz9803@gmail.com`.

**"No trace of the proposal send, attachment 5306, or any Prosper-side
correspondence" — downgraded 2026-08-07, per §13: NOT ESTABLISHED, wrong
mailbox searched.** This was written as a negative finding ("not there")
when it should have been written as an inconclusive one ("not found in
the one account checked, and that account is now confirmed to not be
where this correspondence lives"). Not reversed — attachment 5306 is
still not retrieved, still not read by anyone in this audit — just no
longer treated as evidence of absence.

The reasoning for *why* was correct even when the account-mismatch
framing understated it: the rejection email's own SMTP headers
(`00-intake/_source-documents/
email-2026-07-27_rejection_fwd-2026-07-28.eml`) show the real thread ran
on `mail.sgctech.ai` via SOGoMail — SGC's own private mail server, not
Gmail at all. **Gmail was structurally never going to contain it — not
because of which Gmail account, but because it isn't a Gmail thread.**
See §13 for the account-identity confirmation and §2 decision #8 for the
resulting highest-value open item: a read path to `mail.sgctech.ai`/SOGo.

**Every PRJ-document figure in this repo's comparisons remains
UNVERIFIED, for the same reason as before, now stated more precisely:**
AED 45,000, AED 1,450/mo, the AED 690/650 rates, the Care Plan start
month (11 vs 12 months), and the resulting Year-1/24-month totals are
still a secondhand account (this repo's own prior `deal-card.md`/
`client-brief.yaml` description of a document nobody in this audit has
read), not a verified extraction — that conclusion doesn't depend on
which mailbox was searched and stands unchanged. What changes is only
the framing of the *search itself*: "not found" reads as a completed,
authoritative search; the accurate framing is "not found by a search of
the wrong mailbox," which is a much weaker and more reversible state.

### 8.2 Per-agent finding — rule out as a positioning device for Prosper

Question 11 of the client's own requirements document ("What is the
monthly cost per user?") makes per-agent cost the client's *own chosen*
comparator. Config (ii) (traceable scope only): **AED 147/agent/month**
(31 users, itself unverified — see decision #3 above). Against the PRJ
document's own implied per-agent figure (~AED 58, using its own 25-user
Phase-1 scope cap as denominator, now additionally unverified per §8.1):
**we lose by roughly 2.5×, even on the most favorable configuration we
have.** This holds even accounting for the PRJ figure's own uncertainty
— closing a 2.5× gap would require the PRJ figure to be wrong by a
factor this repo has no basis to assume.

**Per-agent framing is ruled out as a positioning device for this deal.**
It may still be valid framing elsewhere (a different client, a different
segment, a different unit-cost structure) — this finding is specific to
Prosper's numbers, not a general claim about per-agent framing itself.

### 8.3 Catalogue gap register — nine unpriceable requirements

| Requirement | Client priority | Demonstrated on a call? | Any catalogue file references it? |
|---|---|---|---|
| Attendance Tracker | Must Have | Yes — `call-transcript-2026-07-17-internal-demo-prep.md`, rehearsed at length | No — checked `hour-lookup.yaml`, `phase2-catalogue.yaml` in full |
| Employee Records | Must Have | Not specifically | No |
| Task Management | Must Have | Not specifically | No |
| Calendar | Must Have | Not specifically | No |
| Approval System | Must Have | Not specifically (adjacent: commission/allowance approval mentioned in "Talha's Meeting Notes") | No |
| Commission Tracking | Must Have | Yes — "Talha's Meeting Notes," commission engine + clawback logic walked through in depth | No — also confirmed absent from `financing-amortization.md`'s own commission-comp-plan check |
| WhatsApp/Email Integration | Must Have | Partially — Outlook/Gmail sync shown in "Talha's Meeting Notes"; WhatsApp named in the prior PRJ doc's §08 | No — `verbal-promises.md` already logged WhatsApp as DEFERRED, no priceable basis |
| Expense Tracking | Nice to Have | Not specifically | No |
| Payroll Support | Nice to Have | Yes — attendance-to-payroll-to-WPS flow rehearsed in depth in the same demo-prep transcript | No |

**Assessment: this is a catalogue gap, not a Prosper-specific one.** All
nine sit in domains (HR/attendance, payroll/WPS, commission/comp-plan
logic, generic task/calendar/approval workflow) that `hour-lookup.yaml`'s
real-estate-brokerage-uae v2 catalogue never covered at any point in this
corpus — the same absences would surface on any brokerage RFP of this
shape, not just Prosper's. Confirmed by the fact that Kallat's own
`x_bant_need` independently raised attendance/payroll-adjacent asks with
the identical "no priceable basis" outcome, unconnected to this pass.
No other client's files were touched to reach this conclusion — this is
an assessment of the catalogue's coverage, not of any other client's
deal.

### 8.4 Pricing-model contribution, isolated (report only, no repricing)

Delta between config (ii) (AED 67,086 Year-1) and the PRJ document's own
figure (AED 60,950–62,400 Year-1, **now unverified**, see §8.1) ≈
AED 4,686–6,136.

- **Financing uplift, fully isolated within our own model** (build_value
  held constant at 30,916, uplift set to 0% vs. the actual 18%):
  contributes exactly **AED 1,680 to Year-1, AED 3,360 to the 24-month
  total**. This is the one component precisely quantifiable without
  needing PRJ's internals.
- **Rate is not the driver — it runs the other way.** Recomputing config
  (ii)'s same 40 a_side_hours at PRJ's own disclosed rates (690/650,
  averaged to 670) instead of our 525 AED/hr blended rate produces a
  *higher* build_value (AED 37,920 vs. 30,916) — our rate is lower than
  PRJ's, not higher. Whatever makes PRJ's total cheaper, it is not a
  lower hourly rate.
- **The remainder (the larger share of the gap) cannot be cleanly
  isolated into "scope" without PRJ's own internal hour breakdown**,
  which §8.1 establishes we don't have. The likely candidates — PM 15%,
  contingency 5%, hypercare AED 3,920, Class B per-user provisioning, the
  CTS/platform floor — are structural additions in our model that a flat
  Phase-1 fee may or may not have carried; guessing which would be
  inventing PRJ's structure, not reporting it. Flagged as the honest
  limit of what this pass can quantify, not glossed over.

### 8.5 Monthly decomposed, both configurations — the decisive finding

Confirmed (verified by direct execution): the platform/CTS portion is
**AED 3,648/mo in both config (i) and config (ii) — unchanged by scope
reduction.**

| | Config (i) 8 pkg | Config (ii) 4 pkg |
|---|---|---|
| Platform/CTS portion | 3,648/mo | 3,648/mo (**identical**) |
| Recovery portion | 1,623/mo | 912/mo |
| Subscription total | 5,270/mo | 4,560/mo |
| Mobilisation | 22,002 | 12,366 |

**What drives the 3,648 floor — headcount, not edition, not scope**
(`02-calc/pricing-worksheet.yaml:27-34,113`, formula in
`00-knowledge/pricing/policy.yaml:70-87`):

```
hosting_allocation_aed = hosting_node_true_cost_aed(360) × (users/hosting_node_user_capacity(20)) = 360×(31/20) = 558
support_labour_aed     = ceil(users/5) pods × support rate  = 7 × 280 = 1,960
account_mgmt_aed       = tier lookup (policy.yaml:76: tier_5=100/tier_10=200/tier_20=350) — 31 exceeds every band, uses 350
tooling_aed            = 50
cts_total_aed = 558+1960+350+50 = 2,918
platform_floor_aed = cts_total_aed × platform_floor_multiplier(1.25, policy.yaml:87) = 2,918×1.25 = 3,647.5 → 3,648
```

Every input is `users_now` (31) or a fixed policy constant. Community
edition's `licences_aed: 0` is already reflected — the floor isn't an
edition cost, it's what serving 31 users on an ongoing basis (hosting +
support pods + account management) actually costs, marked up 25%. It
cannot go below what 31 users costs to serve regardless of how many
work packages are cut.

**24-month split, against PRJ (all PRJ figures UNVERIFIED, §8.1):**

| | Config (i) | Config (ii) | PRJ (unverified) |
|---|---|---|---|
| Mobilisation | 22,002 | 12,366 | 45,000 |
| Platform total (24×3,648) | 87,552 | 87,552 (**same**) | — |
| Recovery total | 38,945 | 21,889 | — |
| Recurring total (24×1,450) | — | — | 34,800 |
| **24-month total** | **148,482** | **121,806** | **~79,800** |

**The platform line alone (87,552) exceeds PRJ's entire recurring
commitment (34,800) by AED 52,752 — larger than the full 42,006 gap
between config (ii)'s total and PRJ's total.** Confirmed by direct
computation, not estimation. Pushed to the theoretical limit — mobilisation
at zero, i.e. zero implementation value, zero build — the platform floor
alone over 24 months (87,552) still exceeds PRJ's entire 24-month figure
(79,800) by **AED 7,752**.

**Scope reduction structurally cannot close this gap.** We could drop to
a single work package and still lose the 24-month comparison, because
the floor that can't be cut (headcount-driven CTS) already exceeds the
number we're being compared against, before a single hour of build is
added back in. This is a pricing-model question — the rate and the
uplift are both out of this pass's constraint — not a scoping one.

### 8.6 `known-defects.md` #2 — citation is broken, substance predates the contamination

Checked whether the scaffold's "never copy a peer client's folder (see
`known-defects.md` #2)" guidance (`02-clients/_SCAFFOLD/README.md:5`)
predates or postdates the four contamination instances. **Both, in a way
worth stating precisely:**

- In the **first commit** (`cb2f194`, 2026-08-03 23:09), `known-defects.md`'s
  actual #2 **was** "SDR copies a peer's client folder instead of
  `_SCAFFOLD`" — verbatim the guidance the scaffold README cites, and it
  predates the contamination-causing commit (`525940d`, 2026-08-05
  15:06) by about a day and a half.
- The **rewrite commit** (`1a0b990`, 2026-08-04 00:09, "known-defects
  rewrite") replaced the entire list with the current MRD-focused
  20-defect set. The new #2 is "Off-card rate. AED 690/hr blended rate"
  — an unrelated topic. **The scaffold README's citation was never
  updated and is now a dangling reference** — as of this commit, #2 does
  not say what the README claims it says.

Net finding: **the substance of the warning genuinely predates the
contamination and was in force when it happened** — the four instances
occurred despite, not before, written guidance existing. But the live
citation in the repo today is broken and would mislead anyone who
followed it to verify the claim, exactly as it did here. Not fixed in
this pass (`00-knowledge/` is read-only to this agent per `AGENTS.md`'s
access model) — flagged for whoever owns that file to either restore a
#2 entry on this topic or repoint the citation.

### 8.7 Headcount — what population 31 counts, and whether it's the right one

`client-brief.yaml: scale.users_now: 31` traces to CRM Lead 8407's
`x_employee_count` field and this repo's own Rev1 prose ("31 employees
— agents, admin staff, managers, and a partner/founder sponsor") — a
**total team headcount**, not a paid-seat or salaried count.

**Cross-read against "Talha's Meeting Notes"**: "the paid ones are only
like how many... below 10... your agent is commission based... yeah we
are commission based." **Not necessarily a contradiction** — a small
salaried core (<10) plus a larger pool of commission-only agents is a
completely ordinary brokerage structure, and 31 could be the sum of
both. But it raises the real commercial question the client's own
document doesn't resolve: **does every one of the 31 need a paid system
seat?**

One data point cuts toward "yes": the client's requirements document's
§7 "User Roles" Must Have explicitly lists **Agent** as one of four
access-role tiers (Agent, Admin, Manager, CEO) — agents are meant to have
individual logins, not just salaried admin staff. That supports counting
agents in the user population, but doesn't confirm the exact figure 31,
or whether *all* agents (vs. only active/producing ones) would hold an
account.

**This is not a rounding question.** `scale.users_now` (31) directly
sets:
- **Segment** (`policy.yaml:26-29`): 31 exceeds `smb`'s `max_users: 30`
  ceiling **by exactly one**, forcing `mid_market` classification —
  `blended_rate_aed: 525` instead of `smb`'s `395` (a 33% higher rate).
  If the true relevant population is 30 or fewer, the segment flips and
  the rate drops.
- **Hypercare pods**: `ceil(31/5) = 7` pods, driving the AED 3,920
  hypercare cost. A lower N drops both the pod count and this cost.
- **Platform/CTS floor** (§8.5): `hosting_allocation`, `support_labour`,
  and `account_mgmt` in `cts_total_aed` all scale directly with N. A
  lower true population would lower the AED 3,648 floor itself — the one
  line §8.5 shows cannot otherwise be reduced by cutting scope.

**Question to put to Dian, precisely**: *"Of the 31 people on the team,
how many would need their own individual login to the system — every
agent included, since your own requirements document lists 'Agent' as
one of the four access levels — or is it a smaller group (for example,
only actively selling agents, or only salaried staff)?"* This single
answer resolves the T12 provenance gap (decision #3) and directly tests
whether the segment/rate/platform-floor boundary case is real or an
artifact of counting the wrong population. Not resolved further in this
pass — report only, no repricing.

### 8.8 Entity facts — confirmed still open, mobilisation still contingent

Checked the new requirements document against `risk-assessment.yaml`'s
three `RESOLVE` placeholders. It supplies the registered office address
(`Office 3804-05, Concord Tower, Dubai Media City`) — already known,
already matched in `client-brief.yaml`, and touches none of the three
open inputs.

| Placeholder | Status |
|---|---|
| `entity_age_years` | Still `RESOLVE` — nothing in the new document addresses company age |
| `vat_registered` | Still `RESOLVE` — nothing addresses VAT registration status |
| `trade_licence_valid` | Still `RESOLVE` — nothing addresses trade licence validity |

**All three remain open.** Mobilisation is confirmed still contingent
between **AED 22,002** (current, elevated band, 40%) and **AED 18,152**
(if 2-3 placeholders resolve favorably, moderate band, 33%) — see the
2026-08-06 manifest entry for the full computation. Nothing in this pass
changes that finding; it's restated here because item 8 asked for
confirmation, not because new evidence moved it.

### 8.9 Otter.ai/Gmail corroboration — first independent external evidence in the corpus

Gmail search (§8.1) surfaced two Otter.ai meeting-summary notification
emails, both 2026-07-17, to `scholarixglobal@gmail.com`: "Meeting Summary
for Scholarix Global's Meeting Notes" (12:17 UTC, snippet: "focused on
Scholarix Global's system functionalities and addressing client needs")
and a second (12:48 UTC, snippet: "focused on demonstrating... system
features, particularly employee check[-in]..."). Both snippets match the
*already-logged* `00-intake/call-transcript-2026-07-17-internal-demo-prep.md`
content precisely (its own summary covers system-functionality walkthrough
and an attendance/check-in demo). A third Otter.ai email confirms Talha's
personal account, `talhasheraz9803@gmail.com`, requested the full
transcript.

**This is the first time any transcript in the four-client corpus has
independent corroboration from a system outside the transcript file
itself** — a third-party notification service (Otter.ai, via Gmail),
not another document this repo's own SDR authored. Provenance grade for
`call-transcript-2026-07-17-internal-demo-prep.md` is upgraded
accordingly — see that file's own identification section, updated in
this pass. This does **not** extend to "Talha's Meeting Notes" (the
separate, undated transcript underlying Rev2's priority framing) — no
Gmail trace of that recording exists; its provenance stands as already
graded (reasonable inference, not independently confirmed).

---

## 9. Prosper — final recommendation (2026-08-06, this is the last pass)

**The honest set is exactly two options, not three.** §8.5 establishes
that the platform/CTS floor alone — headcount-driven, unrelated to
scope, unrelated to which of the 8 (or 4, or 1) work packages are
priced — exceeds the PRJ document's entire 24-month figure even at the
theoretical limit of zero implementation value. **No configuration this
repo is authorized to build prices below the number that was already
rejected.** A price-based recovery is not available without a rate,
uplift, or platform-floor structural change — all explicitly out of this
pass's authorization. That is the finding, not a hedge around it.

**Option 1 — Return the answered question form
(`03-draft/PRO-Requirements-Answered_2026-08-06.md`), no price attached,
as a relationship move.** Answers all 14 questions honestly (13 of 14 —
Q11 held on headcount), states the nine gaps directly rather than
burying them, and asks the one question (headcount) that's been
genuinely outstanding since intake. Costs nothing, demonstrates the
competence a generic 3-phase template proposal didn't, and matches the
client's own stated posture ("we will keep your details on file... may
reach out to you again") — this doesn't try to reopen a commercial
conversation they've already closed on cost, it just finally answers
what they actually asked.

**Option 2 — Decline directly**, stating plainly which nine
requirements are outside what we can deliver today and that our current
pricing structure doesn't beat their already-rejected number even at
zero scope. More honest than saying nothing; forecloses the relationship
sooner than necessary given they haven't shut the door.

**Option 3 — go back at a materially different price shape** — explicitly
requires authorization this pass doesn't have (rate, uplift, or
platform-floor structure are all out of constraint). Not a real third
option today; naming it as available would be the least-bad-option trap
this recommendation is deliberately not falling into.

**Recommendation: Option 1.** The client hasn't refused future contact,
the answered form costs nothing to send, and it's the first genuinely
honest response this deal has produced — the 22 July proposal answered
none of the 14 questions; this one answers 13 outright and names the
exact question needed to close the 14th. Whether Q12's AED 12,366 figure
travels with it is a judgment call: leaving it in shows we're not
hiding a number; pulling it out keeps the door fully open to have the
headcount conversation first, before any figure is back on the table.
Both are defensible — this is the one open call left, and it's yours,
not the agent's.

---

## 10. Prosper — Rev3 sent, known-state additions (2026-08-07)

The offer and answer form were sent (walk-away held in reserve). Three
items to record as **known state, not resolved state** — the offer is
out the door; these don't block that, but they shouldn't quietly age
into "handled" either.

**T12 shipped non-blocking.** `render_offer.py`'s pre-render gate
reports T12's three failing assertions in full (`users_now` unverified,
package-list not independently corroborated, segment classification
rests on an unverified count) but does not refuse the render on them —
a documented exception, not a silent override, justified by the
2026-08-07 seat-band restructure (the quoted AED 4,560/mo no longer
asserts `users_now` as fact). **The reasoning holds. The fact remains
open.** `users_now=31` is still unverified by this audit
(`USERS_NOW_PROVENANCE` in `test_pricing_engine.py`), and Q11's AED
147/user illustration in the sent answer form rests on it directly,
labelled as an illustration but still built from an unconfirmed number.
An unverified figure is now in the client's hands. Decision #3 in
Section 2 above (confirm `users_now`) remains the resolving action —
this entry doesn't add a new decision, it records that Rev3 shipped
without waiting for that one to close, on the reasoning that the
headline figure doesn't depend on it. If Dian's reply gives a real
headcount, retire this entry; until then it's a live gap, not a footnote.

**Margin gate verified at the band's actual worst case, not just at
N=31.** Revenue is flat across the seat band (full-term commitment
doesn't move with actual headcount inside it); cost isn't — both CTS
and Class B per-user provisioning scale with N, so the top of the band
(35) is where margin is thinnest. Checked directly (`render_offer.py`
`reconciliation_check`, using `pe.b_hours_for_branch` and
`pe.hypercare_hours_for_n`, not a hand-derived shortcut): **margin at
N=35 is 33.18%** (internal_build_cost 9,635, cts_total 2,990) — clears
both `policy.yaml:88` (min_gross_margin 0.30) and `policy.yaml:89` (G23
absolute floor 0.25) with room, though less room than the N=31 basis
case (34.74%).

**Correction, stated plainly**: computing the margin check above
surfaced a real error in this session's own earlier chat output (never
committed to any file — confirmed by a repo-wide grep for the specific
figure before writing this entry). Several turns back,
`internal_build_cost` for config (ii) was reported as **7,362 AED**,
computed by hand as `a_side_hours(40) + class_b(9.081) = 49.081h × 150`
— which omits hypercare hours entirely. The correct figure, matching
the same formula this repo's own worksheets use throughout (and now
verified against the real engine functions, not hand-derived), is
`a_side_hours(40) + class_b(9.081) + hypercare(14) = 63.081h × 150 =
9,462 AED` at N=31. Margin percentages quoted earlier in chat (~36–36.5%)
were correspondingly overstated — the correct N=31 figure is 34.74%.
**Every actual conclusion this session reached still holds** (build
value still clears internal build cost by a wide margin; all margin
gates still pass at every configuration checked, including the platform
floor's own governing gate) — nothing was ever committed to a file with
the wrong number, and no decision was made on the strength of the error.
Recorded here because a chat-only error should still be owned, not
because anything downstream needs correcting.

---

## 11. Cross-client class: ungoverned PRJ-model documents functioning as price anchors (2026-08-07)

Kallat's Stage 0 exposure check (see `CHANGELOG.md` 2026-08-07 entry)
surfaced the same shape of defect §8.1 already logged for Prosper — this
section names it as a class, across both confirmed instances, rather
than treating either as a one-off.

**The pattern**: a proposal document built entirely outside this repo's
governance (different rate card, no gate check, no `manifest.yaml`
record until after the fact) was sent to the client, the client reacted
to it commercially, and this repo's own governed SUB-model rebuild has
never been reconciled against it line-by-line. The client's live
commercial understanding of "SGC's price" rests on a document no check
in this repo has ever inspected.

| Client | Document | Sent | Client reaction | Rate basis | Status |
|---|---|---|---|---|---|
| **Kallat** | SGC-KP-2026-07 | 2026-07-23 | 2026-07-24: general price pushback, no specific figure named as rejected | AED 425/hr flat tiered rate. Real rate-card value (`rate-card.yaml:54`, `qa_engineer` L1) applied as a blanket tier rate, not a wholly off-card number — correction to this repo's own prior "not on rate-card.yaml" framing, which overstated the defect | Confirmed. **Responsiveness checked, §14/§12**: partially responsive to Sadique's own 2026-07-16 requests (portal sync, AI scoring, website/SEO, group roadmap all trace to `verbal-promises.md`'s own sourcing), delivered via a generic tiered structure with at least one untraced addition (WhatsApp) — a mixed case, not confirmed as Prosper's clean "answered none of it" failure, and not confirmed otherwise either (document not retrieved). |
| **Prosper** | "PROSPER x SGC Implementation Proposal - 2026" (CRM attachment 5306) | 2026-07-22 09:44 UTC | 2026-07-27: explicit rejection on cost | AED 690/hr and AED 650/hr, both literally on `rate-card.yaml: forbidden_rates` | Confirmed (§8.1) |
| **VGE** | — | — | — | — | Unchecked. No PRJ-type document referenced in VGE's readable text files this pass, but that's a text-search absence, not a mailbox/CRM check — the same kind of check that took a dedicated retrieval attempt to even attempt for Prosper (§8.1) and still failed. |
| **MRD** | — | — | — | — | Unchecked, same caveat as VGE. Note MRD's own defect (§1, §2 #4) is a different shape — this repo's *own* prior issued figures (AED 879/mo, Rev1/Rev2) never retracted to the client — not an ungoverned foreign document. Worth distinguishing: MRD may have zero PRJ-class exposure and still have live anchor exposure of a different kind. |

**Two confirmed, two unchecked — do not read "two confirmed" as "the
other two are clean."** A dedicated mailbox/CRM search is the only way
to close VGE and MRD, per how hard §8.1's search for attachment 5306
turned out to be even when actively looking (wrong Gmail account tried,
real thread lived on a different mail server entirely).

**Kallat's anchor inverts Prosper's problem, it doesn't repeat it.**
Prosper's PRJ figure sits *below* what this repo's governed model can
price at any configuration — a pure floor problem (§8.5, §9). Kallat's
SUB mobilisation (AED 22,429) sits *below* the PRJ range's one-time
floor (AED 48,450), while the SUB monthly (AED 5,850) sits *inside* the
PRJ's own disclosed monthly-hosting range (AED 2,800–6,300/mo) — not
cleanly above or below either end. Whether the governed model reads
cheaper or dearer than what Sadique Abbas believes he was quoted depends
on which PRJ tier he's anchored to, and the entry/term comparison can
point opposite ways (cheaper on mobilisation, level-to-dearer over 24
months, or the reverse). **When Stage 5 runs, compute the comparison
against both PRJ tier ends (AED 48,450 and AED 123,250) explicitly — a
single midpoint comparison would hide exactly the case that matters,
and this should not be discovered live in a client meeting.**

---

## 12. Kallat — headcount is a hard block, not a sizing question (2026-08-07)

Contrast with §10's Prosper entry, stated explicitly so the difference
isn't lost: **Prosper's T12 failure shipped non-blocking** because its
2026-08-07 seat-band restructure decoupled the quoted figure from the
exact `users_now` value — banding absorbed the uncertainty. **Kallat has
no equivalent band.** `users_now` (40) sits one user-band above `smb`'s
30-user ceiling; crossing it sets the segment (`mid_market` vs `smb`),
which sets the blended rate (525 vs 395 AED/hr), which moves
`build_value_aed` by 27.8% (`CHANGELOG.md` 2026-08-06 entry). No band
width absorbs a rate-card change — this is a structural dependency on
the number itself, not a range the number falls somewhere inside of.

**T12 stays hard-blocking for Kallat by design. No non-blocking
rationale applies, and no labelled-illustration figure (the kind Q11
used for Prosper) is authorized until `users_now` is confirmed.**

Confirmation question drafted for **Sadique Abbas** (Sales Manager,
decision-maker per `client-brief.yaml`/`manifest.yaml` — not either call
transcript's participants, both SGC-internal) —
`00-intake/sdr-followup-headcount-2026-08-07.md`. Routed as an ordinary
SDR follow-up through **Johnny Gurrera** (logged the 2026-07-24 client
call) rather than the stamp→SDR→John→stamp sequence: it commits nothing
and quotes no figure, so that gate doesn't apply. Held, not sent.

**Same-day correction, worth recording**: an intermediate pass added a
Bran→John approval gate and "take-it-or-leave-it" framing to this
question before it was corrected back to the above. Neither belonged
here — the gate sequence is for figures/commitments, this question
carries neither, and "take-it-or-leave-it" reads as pressure on a free
scoping question, not the priced offer that framing actually belongs to.
Corrected same day per direct instruction; `manifest.yaml`'s two
2026-08-07 escalation entries record both the mistake and the fix
rather than rewriting history.

**A third transcript surfaced same day — briefly changed T12, then
reverted by direct ruling.** A previously-missing discovery/demo call
transcript (Sadique Abbas present, date now confirmed **2026-07-16,
9:51am, 25 min**, via Otter.ai notification metadata) was added:
`00-intake/call-transcript-2026-07-16-discovery-demo.md`. Direct
exchange: asked "How many agents do you have right now?", Sadique
answers "We have approximately 40 or 15, approximate." An earlier pass
this session read that as a garbled "40 or 50" and upgraded
`USERS_NOW_PROVENANCE` accordingly — **reverted the same day, per direct
ruling.** Two reasons, stated precisely: (1) reading "15" as "50" is
reconstruction, not reading — Sadique qualifies the number twice in one
sentence, answering informally; (2) more fundamentally, Kallat is a group
spanning multiple businesses across different industries (Sadique
himself, same call, ~11:04-11:12) — even a precise figure from this
exchange wouldn't establish which entity it counts, or whether the
system is meant to size one brokerage or several. **`USERS_NOW_PROVENANCE`
is back to unverified. T12 stays a hard block, unchanged from the entry
above.** The drafted SDR follow-up now carries two questions: precise
headcount, and which Kallat Group entities would be on the system — see
`00-intake/sdr-followup-headcount-2026-08-07.md`.

**The transcript's date also resolves the SGC-KP-2026-07 sequencing
question — and corrects this entry's own earlier "same morning"
framing.** Checked against the actual per-meeting timestamps inside each
Otter notification (not send times, which was the earlier error): this
call is **9:51am**; the internal prep call is two short segments at
**4:51pm (13 min) and 5:16pm (10 min)** — same day, but ~7 hours later,
not back-to-back. A third, unidentified 32-minute recording at 4:13pm
also exists (Otter snippet only: "Speaker 1 expressed frustration about
the difficulty of generating leads... a company expected a demo without
a diagnostic phase") — matches no transcript currently in this repo,
flagged and not chased further.

**Consequence for the headcount provenance record, not the gate**: the
internal prep call's "40 people... 50 then" line came ~7 hours *after*
this call, from SGC's own team — **it is not independent corroboration
of Sadique's headcount, it is SGC recalling what Sadique said earlier
that day.** One source, counted twice, is a worse state than one weak
source honestly labelled as such. Corrected in
`call-transcript-2026-07-16-internal-prep.md` and this call's own
transcript file; T12 was already, and remains, a hard block — this
changes the record, not the gate.

Sequencing itself still holds: discovery call (9:51am) → [unidentified
call, 4:13pm] → internal debrief (4:51-5:26pm) → SGC-KP-2026-07 sent 7
days later (2026-07-23) → client price pushback the next day
(2026-07-24). **Whether SGC-KP-2026-07 addresses what Sadique asked
for — checked, not assumed.** Document itself not retrievable this
session (same limitation as attachment 5306 — two Gmail searches, no
trace). From this repo's own secondhand descriptions: `verbal-promises.md`
rows 1-2, 4-5 source portal sync, AI scoring, the group-level roadmap,
and website/SEO to "the original discovery call (via SGC-KP-2026-07
doc)" — all four trace directly to things Sadique raised on this call.
Against that: the internal prep call describes it as a generic tiered
structure (Tier 1 basic → Tier 3 "all services included," explicitly
built to be "something better with similar scope" than a competitor's
template) carrying at least one item (WhatsApp, Tier 2/3) that traces to
nothing said on this call. **Best available read: partially responsive,
delivered through a generic tier structure — a mixed case, not a clean
match to Prosper's "answered none of the 14 questions" failure. Not
confirmed either way without the actual document.** See §11's table,
updated accordingly.

---

## 13. Confirmed: this session's Gmail tooling authenticates as `scholarixglobal@gmail.com`, not `renbranmadelo@gmail.com` (2026-08-07)

§8.1 already found `scholarixglobal@gmail.com` empty when searching for
Prosper's attachment 5306, but treated the account identity itself as
inferred from the session setup, not independently confirmed. **Now
directly verified**: `search_threads` with query `to:me` — Gmail's own
resolution of "me" to the authenticated account — returned live inbox
results (a Zapier task-replay alert, two Resend quota-alert emails, all
2026-08-07) every one of which lists `toRecipients: ["scholarixglobal@gmail.com"]`.
Not a config file read, not a memory citation — the mailbox's own
messages confirm which account this is.

Separately, this session created a Gmail draft to `bran@sgctech.ai`
(Kallat internal-review request, later superseded/neutralized — see
`manifest.yaml` 2026-08-07 entries) from this same account, before the
account identity had been checked. No indication that draft failed to
create, so `scholarixglobal@gmail.com` does have working send/draft
capability — the issue is which mailbox it is, not whether it works.

**The real conclusion, stated plainly: client correspondence for these
deals lives on `mail.sgctech.ai` behind SOGo webmail, not in Gmail at
all — so the Gmail connection was never going to hold it, independent of
which Gmail account.** §8.1 already found the actual Prosper rejection
thread's SMTP headers point there. That is not a coincidence sitting
next to this account-mismatch finding — it is the explanation for it.
Every negative result this session got from `scholarixglobal@gmail.com`
(attachment 5306, and — downgraded above per this section — MRD's
retraction search) was always going to come back empty, regardless of
whether the connected account had been `scholarixglobal@gmail.com`,
`renbranmadelo@gmail.com` (this session's own account table lists this
as the intended connection, and this session has never actually had
access to it), or any other Gmail address. **Absence of evidence from
Gmail, in general, is not evidence of absence for these deals — the
evidence lives elsewhere.**

**What this confirms vs. what it doesn't**: confirmed — this session's
tooling authenticates as `scholarixglobal@gmail.com`; confirmed — at
least one relevant thread (the 5306 rejection reply) ran on
`mail.sgctech.ai`/SOGo. **Not yet confirmed**: that *all* relevant
correspondence (MRD's, Kallat's) also lives there rather than being
scattered across multiple systems, and this session still has no read
access to `mail.sgctech.ai`/SOGo to check directly. Getting that access
is now logged as the highest-value open item — §2 decision #8.

**Decision #1 in §2 above is the resolving action for this entry too** —
this doesn't add a new decision, it records that the question is now
drafted and routed, not that headcount is resolved.

---

## 14. Kallat — 2026-07-16 discovery/demo call: verbal exposure, gap register, scope signal (2026-08-07)

Full transcript: `00-intake/call-transcript-2026-07-16-discovery-demo.md`.
Headcount handled in §12 above (T12 stays blocked). Everything below is
what else that call surfaces — most of it more consequential than
headcount, per direct instruction.

### 14.1 Verbal exposure — full detail in `verbal-promises.md` rows 9-13

| # | What was said | Who / when | Why it matters |
|---|---|---|---|
| 9 | "You have everything at your disposal... right from the get go," said directly against per-user monthly pricing and per-feature upcharges | Johnny, ~9:11 | **Serious finding, not a footnote.** Conflicts with the governed SUB-model's seat-band monthly structure and with phase2 add-on pricing — both are exactly the "pay by user, pay extra for features" pattern this promise disclaims. See §14.4 — new Stage 5 blocker. |
| 10 | Cybercrime/hacking "completely implausible" | Johnny, ~1:48 | Unqualified absolute guarantee on the client's first-raised concern. Unbackable — needs written correction before signing. |
| 11 | Portal connection "one click," fees are the portal's not SGC's; software "already accredited by" Bayut/Property Finder/dubizzle | Consultant, ~7:16-21:19 | Conflicts with planned Portal Sync add-on pricing (`phase2-catalogue.yaml`). Accreditation claim checked against the full `00-knowledge/` tree — UNSOURCED, no partnership record exists anywhere in this repo. |
| 12 | Named another client and disclosed their monthly Property Finder spend (~AED 30,000/mo) | Consultant, ~7:16-7:48 | Third-party confidentiality breach, independent of this deal — see §14.2. |
| 13 | Spontaneous pre-Kickoff sandbox/demo access offer | Consultant, ~24:12 | Timeline correction to `verbal-promises.md` row 6: this offer predates and contradicts the "2026-08-05 deliberate concession, reversing 2026-07-16 policy" framing — the practice was already happening the same day the policy is dated to. |

### 14.2 Known-defects.md candidate — flagged, not written (00-knowledge/ is read-only to this agent)

Row 12 above is a distinct defect class from anything already in
`known-defects.md`'s 20-item MRD-derived list: an SGC representative
disclosing one client's identity and specific commercial terms to a
different prospect, unprompted, as a sales point. Not a pricing defect,
not specific to Kallat — a disclosure-hygiene defect that could recur on
any call. Recommended for the Commercial Desk to add as its own numbered
entry; this agent cannot write to `00-knowledge/` (per `AGENTS.md`'s
access table — Commercial Desk write, agent read-only).

### 14.3 Gap register — demoed on the call, checked against the catalogue

Built the same way as Prosper's (`§8.3`): from what was actually shown
and discussed, not from the brief.

| Feature | Demonstrated on this call? | Catalogue reference? |
|---|---|---|
| AI lead-probability scoring | Yes — walked through in detail (~14:56-16:20), "give you a percentage of the probability of closing" | Yes — already priced as an add-on, `ai_lead_scorer_lite` (AED 495/mo), per `verbal-promises.md` #2. Already correctly excluded from base scope. |
| Agent commission calculation | Yes — "our commission calculation for the agents... very streamlined... it will just automatically calculate" (~23:12) | **No** — `phase2-catalogue.yaml` has only a `commission_impact` note stating no commission/comp-plan document exists anywhere in this repo; no priceable line item. Same gap already established on Prosper (`HANDOVER.md` §8.3). |
| Auto-reconciliation of client/landlord payments | Yes — "without your accountant having a headache... it will be auto reconciled" (~23:12) | **No catalogue entry at all** — checked `hour-lookup.yaml` and `phase2-catalogue.yaml` in full, zero matches for reconciliation. |
| Client/landlord payment portals | Yes — "we can also give portal access for the clients... if you have landlords... they can see their dashboards... pay directly" (~23:03-23:12) | **No catalogue entry** — zero matches for "landlord" or a client-payment-portal concept anywhere in the pricing knowledge layer. |
| Live-synced website module with auto-brochure generation | Yes — demoed live (~21:31-22:57), "once you upload in the CRM, it fetch into website... directly, live" | **Different feature from what exists in catalogue.** `phase2-catalogue.yaml`'s `website_lead_capture` (AED 2,400 one-time) is a lead-capture widget, not a full property-listing-synced site with auto-brochure generation. Neither the demoed module nor "website cleanup, SEO, social media consultancy" (which Sadique separately and explicitly asks for, ~12:00) has a real catalogue match — consistent with `verbal-promises.md` row 5's existing EXCLUDED classification for website/SEO work, now confirmed against the actual demo rather than just the old PRJ doc. |

**Assessment, same shape as Prosper's §8.3 finding**: this is a catalogue
gap, not a Kallat-specific one — commission logic, payment reconciliation,
and landlord/client portals sit in domains (financial operations,
multi-party portal access) the real-estate-brokerage-uae catalogue has
never covered. The AI-scoring line is the one exception, already handled
correctly.

### 14.4 Stage 5 presentation — RESOLVED IN PRINCIPLE by Bran, blocked in practice on the correction draft

Ruling (2026-08-07, §2 decision #9): the per-user promise ("everything at
your disposal... right from the get go") is the **smaller half** of the
exposure this call created — §14.3's gap register (commission calc,
payment auto-reconciliation, landlord/client portals, all demoed live,
none in the catalogue) contradicts that promise far more sharply than
any seat-band pricing structure would, since those features were shown
working and aren't in the offer at all. **A written correction to Kallat
is required regardless of which pricing shape is chosen, and it must
land before or with the price, never after.**

Once that's accepted, the pricing shape follows directly: **flat
monthly, no per-user rate anywhere in the document, no per-user
derivation even as a labelled illustration, with a capacity ceiling
stated as an operational limit rather than a pricing tier.** This
honours what Johnny actually said, keeps seat exposure bounded across an
unknown number of Kallat Group entities without needing headcount
precision first, and doesn't require walking back the one thing Sadique
was told most emphatically.

**Status: resolved shape, pending correction — not open.** The only
remaining action is drafting the written correction (gap-register
features + per-user framing, addressed together); not requested this
pass, not drafted. No repricing or re-presentation performed.

### 14.5 Scope signal and one correction to this session's own earlier framing

Sadique's own redirect (~18:55, "let me have the proposal on the... open
property management... that is something which is aligning with what we
are looking for") names **property management** and **portal integration**
as his stated priority on this call. `client-brief.yaml`'s
`work_packages_requested` (`crm_leads`, `users_roles_agent_perf`,
`reports_dashboard`, `data_migration_500`) contains neither as a named
item — worth checking against `property_unit_register` (already in the
worksheet, but as one of the four *unrequested* packages per §11/
CHANGELOG's contamination finding) before assuming it's simply missing.

**Correction, checked directly rather than assumed**: an instruction this
pass characterized the incumbent system (Zapier automation) as something
"the brief records as not described." **Not accurate** —
`client-brief.yaml:31` already reads `incumbent_system: "Zapier
automation (lead distribution) + Google Sheets (reporting/pipeline)"`,
matching the transcript's own Zapier mention (~13:40) exactly. Stated
plainly rather than silently agreed with: this specific point was already
correctly captured before this session touched the file.
