# Known Defects

The highest-value onboarding asset in this repo. Read before running your
first deal (`05-ops/onboarding-new-sdr.md`). Twenty defects below trace to
a real revision history — `02-clients/MRD-meridianview-realty/`, Rev1
(issued 2026-06-15) and Rev2 (issued 2026-07-02), both retracted and
preserved immutable in `05-issued/` with the exact original wording, not
paraphrased. Rev3 (`03-draft/`) is the correction, gate-checked against
every one of these.

## The 20 defects (MRD-2026-SUB-01, Rev1 and Rev2)

1. **Recurring portion below cost.** AED 879/mo quoted against a cost
   stack (licences + hosting + tooling + support + account mgmt) of
   roughly AED 2,360/mo at the scope sold — structurally loss-making from
   the first invoice. Caught by G1 (platform floor).
2. **Off-card rate.** AED 690/hr blended rate — not on `rate-card.yaml`,
   at any level. Now explicitly listed in `rate-card.yaml: forbidden_rates`
   so this specific number is mechanically rejected, not just absent.
   Caught by G9.
3. **No PM, QA, or documentation lines.** Commercial Rules 4, 5, and 6
   breached outright — the underlying costing had none. Caught by G19.
4. **Underscoped hours.** 33 hours quoted against what the same scope
   correctly costs at 46 hours (Rev3's worksheet). A rate multiplied by
   the wrong hour count is still wrong even if the rate itself were valid.
5. **Zero-hour scope items.** Portal sync, website integration, and AI
   lead scoring described as included, with no hours allocated to build
   any of them.
6. **Sold both ways.** AI scoring simultaneously "included" in the
   subscription and separately available as a AED 1,250/mo add-on in
   SGC's own catalogue — internally contradictory.
7. **Implied fee reduction after recovery.** A clause implied the monthly
   fee would drop once the build was recovered — directly contradicted by
   `clause-library/post-recovery-continuation.md`, and loss-making in
   year 2 if honored. Caught by G5.
8. **No clawback.** Full build delivered before a single invoice, with no
   mechanism to recover value if the client terminated early. Caught by
   G4/G16.
9. **Term anchored to the wrong date.** Term started at go-live, roughly
   4–6 weeks after delivery work had already begun — meaning weeks of
   uncompensated exposure before the clock (and billing) even started.
   Caught by G6.
10. **Rev1's VAT claim: "no VAT — free zone."** Factually wrong.
    Designated Zone treatment applies to goods, not services; SGC's
    services are standard-rated regardless of zone status.
11. **Rev2's VAT claim: "SGC TECH AI is VAT-registered."** Also false,
    in the opposite direction — SGC held no TRN at the time. Two
    different wrong claims across two revisions of the same deal is
    itself a signal that VAT status was never actually checked against a
    single source of truth before either revision was drafted. Both
    replaced by `clause-library/vat-uae.md` + `vat-gross-up.md`.
12. **Inconsistent registered address.** Different documents in this
    deal's history implied different addresses/licence authorities for
    the same entity. Now centralized in
    `06-brand/entity/legal-identity.yaml`, deliberately left `RESOLVE`
    until one real address is confirmed, rather than guessed.
13. **Uncapped referral, unenforceable exclusivity.** An open-ended
    referral credit with no cap, plus a promise that pricing "will not be
    extended to any other brokerage" — a commitment SGC cannot control or
    enforce. Replaced by `clause-library/referral-capped.md` and
    `exclusivity-replacement.md`.
14. **Recommended tier matched the rejected budget.** The tier pushed in
    an earlier draft priced at roughly the same figure (AED 30,000+) the
    client had already verbally declined before this engagement even
    started — re-quoting a number the client already said no to, without
    acknowledging it. Caught by `budget_test`.
15. **Adoption unaddressed.** The client's explicitly stated deal-breaker
    — described directly on the discovery call — did not appear anywhere
    in either revision. Fixed with a specific, dated mechanism in
    `clause-library/adoption.md`, not a generic training line.
16. **Blanket discount on the recovery portion.** A flat 10% "annual
    discount" applied across the whole subscription figure, including the
    portion that recovers already-delivered build value — giving away
    work that had already been performed. Fixed by G11: discounts apply
    to the platform portion only.
17. **Named individual, no substitution right.** Hypercare and delivery
    promised "personally" by one named consultant with no fallback —
    single point of failure for the client and an operational risk for
    SGC. Fixed by `clause-library/key-person-and-subcontractor.md` (G27).
18. **Edition misdescribed.** "Odoo Enterprise licences" promised while
    the actual build used Community edition — the single highest-stakes
    misdescription in the whole history, since it implies capabilities
    (automated bank reconciliation, official mobile app, Odoo vendor
    support) the client was never actually going to receive. Fixed by
    `editions.yaml` + `clause-library/edition-and-upgrades.md` (G36).
19. **Unpriced recurring internal cost.** Monthly business-review calls
    were implied as a standing commitment without ever being priced —
    at senior time, this runs to roughly AED 10,800/year unbudgeted.
    Fixed by the review-cadence rule in the runbook (quarterly below AED
    2,500/mo subscription).
20. **Unsourced performance claims.** "AED 1.15 billion in client value,"
    "104% Year-1 ROI," "5.9-month payback" — presented as track record
    with no source, no client consent, and no basis found anywhere in
    this repository. Removed entirely from Rev3; nothing replaces it,
    because nothing sourced was available to replace it with.

## The six overrides applied in the v2 rebuild

1. An earlier, larger build-value estimate for this deal class was
   brought down to a correctly-scoped figure once documentation, QA, and
   PM lines were added properly rather than omitted — a reminder that
   "correcting" a defective estimate does not automatically mean the
   number goes up; sometimes proper structure replaces padding.
2. Three pricing tiers collapsed to two options — Option A (mobilisation
   paid) only. A third tier and Option B (zero mobilisation) both add
   complexity without adding protection; Option B is separately withdrawn
   under `payment-plans.yaml: withdrawn`.
3. Term extended from a 12-month assumption to 24 months for boutique
   builds in this value band, giving the recovery period enough room
   without requiring an unrealistic mobilisation percentage.
4. Blanket discounting replaced with platform-portion-only discounting
   (G11) — see defect #16 above.
5. Cadence table values reinterpreted as ceilings, not price entitlements
   (G12) — the margin floor beneath a cadence table value always binds if
   it's tighter.
6. A named, irreplaceable consultant promise replaced with an explicit
   substitution right (G27) — see defect #17 above.

## What this v2 build itself caught (institutional memory, not client-facing)

21. **Segment blended rates that didn't cleanly pin to a rate-card role
    — flagged, then actually resolved after review.** `policy.yaml`'s
    `smb` and `mid_market` blended rates did not trace to a single named
    role on `rate-card.yaml` the way `startup_boutique` pins to
    `roles.startup_consultant` — the same drift class as defect #2, just
    less obvious because one of the two values coincidentally matched a
    *different* role's rate rather than matching nothing at all. The
    first pass on this build left it in place with an inline comment,
    reasoning that "don't invent numbers" meant not fabricating market
    data. On review, that reasoning didn't hold: the instruction governs
    fabricating data, not preserving a rate already known to be wrong
    inside a live operational config — a comment protects nobody, because
    the entire inheritance model assumes an SDR copies `_SCAFFOLD` and
    trusts the numbers in `00-knowledge/`, not that they'll read every
    inline comment in `policy.yaml` first. **Corrected**: both segments
    re-pinned to real rate-card roles. The rejected `mid_market` value is
    now a permanent `rate-card.yaml: forbidden_rates` entry, same
    treatment as defect #2's off-card rate. The rejected `smb` value
    couldn't get the same treatment — it's legitimately a different
    role's real rate — so `validate.py` instead structurally checks that
    every segment's `blended_rate_aed` matches its declared `pinned_role`
    exactly, closing the gap a forbidden-value list alone can't cover.
    The lesson generalizes: a flag that only a human might read is weaker
    protection than a check that runs by construction — prefer the
    latter whenever the former is the first draft of a fix, not the last.
22. **A worked example inherited a since-corrected gate formula.** During
    this same build, `03-library/worked-examples/boutique-brokerage-5users-24mo.md`
    (built by a parallel process) used an earlier draft of the G1
    platform-floor formula (comparing cost-to-serve against build value
    plus cost-to-serve, rather than against the recurring subscription
    price) that had already been corrected in
    `commercial-rules/subscription-guardrails.md` before the worked
    example was finished. Caught and fixed before commit — the lesson:
    when two parts of a build run in parallel, a formula correction made
    in one place doesn't propagate to a document already being drafted
    elsewhere unless someone actually re-checks it against the current
    source, not the source as it was when that document started.
23. **A validator that flagged its own correct disclosures.** The first
    version of `validate.py`'s forbidden-phrase check used a plain
    substring match for `VAT-registered` and `iOS/Android app`. This
    correctly caught false claims, but also flagged this repo's own
    mandatory, correct text — the VAT gross-up clause's "Should SGC TECH
    AI **become** VAT-registered..." and the Community-edition
    disclosure's "**not** a dedicated iOS/Android app." Discovered only
    by actually running the validator against real content, not by
    reading the spec. Fixed with negation-aware matching, and — because a
    validator that cries wolf on correct text is worse than no validator
    at all — the two false-positive cases (plus their true-positive
    counterparts) are now a permanent regression corpus in `validate.py`
    itself (`SELFTEST_MUST_NOT_FLAG` / `SELFTEST_MUST_FLAG`, run via
    `python validate.py --selftest`, and automatically before every real
    run). A future tightening of the phrase-matching regex cannot
    reintroduce this specific failure without the self-test catching it
    immediately.
24. **Fork scope drift — agent continued past dispatched instructions into
    stale conversation context.** During the 2026-08-15 RVN audit, a forked
    agent was dispatched against commit `a143c85` for a specific, scoped set
    of items, but continued working past that dispatch into an older,
    superseded mega-prompt still present in the conversation's context, and
    returned a different commit (`c737f52`) than what the dispatch actually
    called for. The additional work turned out to be genuine and correct
    (a full RVN SOW/commercial-terms rewrite), but the mismatch between
    "what was dispatched" and "what came back" is itself the failure mode —
    a handoff process that silently absorbs an unrequested commit instead of
    flagging the discrepancy will eventually absorb one that is NOT correct.
    Lesson, stated for greppability: **a returned commit hash that does not
    match the dispatched commit hash is a signal to stop and verify, not a
    detail to note in passing** — the same discipline this file already
    applies to inline comments and formula corrections (items 21-22) applies
    equally to agent handoffs.
25. **Two independent sessions found the same commission-retention
    ambiguity; only one of them left it open.** A local, diverged branch
    (never merged into this file until the 2026-08-16 origin/main merge)
    independently flagged that a "5% retention" figure could mean 5% of
    the commission amount OR 5% of contract value — a ~7x difference —
    with neither picked anywhere in that branch's own policy file. By the
    time that branch merged, `00-knowledge/clause-library/commission-retention.md`
    (built on origin/main, same 2026-08-15 pass, unknown to the local
    branch at the time) had already resolved the BASE question in its
    approved operative text: retention is 5% of the commission amount
    earned on cash collected, not of contract value. What that clause's
    own provenance note still leaves open is narrower than the local
    branch's finding: whether 5% itself is the confirmed figure (stated
    as owner-stated in conversation, "NOT independently documented
    elsewhere in this repo... pending confirmation") — not which base it
    applies to. Recorded here because the local branch's finding was real
    and worth a permanent record, but stating it as still-fully-open
    after the merge would misrepresent work origin had already done.
26. **`grep -a` on a rendered PDF is not a text search — it is a coin
    flip.** Found while fixing a fictional test fixture that had
    accidentally reused a real client's name (RVN): `grep -a RVN
    file.pdf` returned no match on a PDF where the client name
    demonstrably appeared on two pages (cover, signature block) —
    confirmed only by extracting the text properly (`pypdf`), which found
    both. PDF text streams are commonly compressed/encoded at the object
    level; a raw byte-level grep can miss content that is genuinely
    present and visible when the file is opened. **Any future
    client-name scrub, credential check, or content audit against a
    rendered PDF must go through a real text extractor
    (`pypdf.PdfReader(...).pages[i].extract_text()` or equivalent), never
    `grep -a`/binary grep alone** — a clean `grep -a` result on a PDF
    proves nothing and must not be reported as a clean result.
