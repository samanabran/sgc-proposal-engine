# MRD-2026-SUB-01 — Handover Register

**As of 2026-08-06.** This file assembles findings already produced across
this session's audit passes — it contains no new analysis. Where a claim
needed a one-line verification to state accurately, that's noted inline;
nothing here required opening a new investigation thread.

**Headline: MRD is not clear for issue, independent of any gate/check
status.** See §1 below — there is no artifact in this repo documenting
that the client was ever told Rev1/Rev2's figures were wrong. The
client's last actual communicated understanding is AED 879/month.

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
correction exists anywhere in this repo. Per the instruction that
prompted this check: that means MRD is not clear for issue regardless of
check status — the client's live understanding, as far as this repo's
evidence goes, is still Rev2's AED 879/month.

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

### PRO-prosper-realestate

Zero issued revisions — same pattern as Kallat (`PRO-2026-SUB-01_Rev1`,
`issued_date: ""`, `05-issued/` empty). Current draft stale against its
own worksheet (mobilisation printed AED 38,544 vs. current AED 22,002).
T10: 3/3 pass. T12: 2 of 3 assertions fail (`users_now` unverified;
same-pen scope match, not independently corroborated — no billing
exposure, since 8/8 packages match the brief). Not rendered by R11/R12.

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
| 4 | MRD: what is Rev1/Rev2's actual retraction status vis-à-vis the client? | ______ | Evidence of the correction communication (if one happened) — or, if none exists, a decision on whether Rev3's issue must be framed as a price correction rather than a first quote. |

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
