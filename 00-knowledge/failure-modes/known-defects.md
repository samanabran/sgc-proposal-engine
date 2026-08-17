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
27. **A merge silently reverted a test's already-fixed hardcoded rate back
    to stale, and the resulting drop in failure count was reported as "the
    same baseline."** `test_pricing_engine.py`'s `t9_worksheet_internal_consistency()`
    had, in an earlier session, been edited to check worksheet floors
    against `394.38`. It carried that value as a second, undeclared literal
    copy of `business_cost_floor()["floor_per_hour_aed"]` rather than
    reading the rate live — the same duplicate-implementation defect class
    as #2 and #21, just inside a test instead of a config. When the
    2026-08-16 origin-merge resolved this file via `git checkout --theirs`,
    origin's copy of the test still had the pre-fix literal (`150`), so the
    merge silently reverted the fix. Four T9 assertions that had correctly
    been failing against `394.38` started passing against `150` instead —
    not because the underlying worksheets got healthier, but because the
    check itself got weaker. The failure count dropped from 16 to 12 and
    was reported as an unchanged baseline. It was not: the same four
    assertions were still running, now checking the wrong number, and a
    drop in failures immediately after a `--theirs` merge is exactly the
    direction a genuine regression would produce — it should have been the
    first thing treated as suspicious, not the thing waved through as
    coincidental. Caught only by isolating the pre-merge commit in a `git
    worktree` and diffing its actual failure list line-by-line against the
    post-merge run, not by comparing summary counts. **Fixed at the root**:
    the test now reads `floor_per_hour = pe.business_cost_floor()["floor_per_hour_aed"]`
    live instead of carrying its own copy, so a future merge cannot revert
    it to a stale number without the test itself changing. **Lesson: a
    failure count that moves during an "origin wins wholesale" merge is not
    automatically explained by the merge — name which specific checks
    changed and why, especially when the count moves in the direction a
    regression would produce.**
28. **A rebuild silently destroyed a real, evidence-based governed
    register, converted a fail-loud read into a fail-silent one in the
    same edit, and the report written immediately after did not catch
    either.** Found investigating why two independently-generated fixture
    proposals landed on an identical page count. The pre-merge local
    branch's own `template-catalogue.yaml` carried a genuine, non-fabricated
    `excluded_capabilities` register — 5 entries, each with a real evidence
    citation against `00-intake/demo-presentation-inventory-2026-08-16.md`'s
    audit of SGC's own demo Odoo instance (WhatsApp notification, automated
    call logging, call-target enforcement, biometric attendance hardware,
    portal feeds) — and `render_proposal_v4.py` read it with direct dict
    access, `cat["excluded_capabilities"]`, which would raise `KeyError`
    the instant the key went missing. The 2026-08-16 "origin wins
    wholesale" merge (`known-defects.md` #27's same merge) overwrote
    `template-catalogue.yaml` with origin's real-estate-vertical version,
    which has never had this key at all — a legitimate content change,
    since the real-estate catalogue's exclusions are a different, real
    register. But the SAME-DAY renderer rebuild (`66d3d2f7`) that ported
    the generator onto origin's schema also silently changed the access
    pattern to `doc.get("excluded_capabilities", {})` — swallowing the
    now-inevitable missing key into an empty table instead of the loud
    crash the original code would have produced, and masking the fact
    that `clause-library/exclusions-standard.md`'s mandatory verbatim
    clause (the thing that should have replaced the old register for this
    vertical) was never wired in at all. The report written immediately
    after that rebuild then asserted the exclusions table was populated
    with alternatives per row — true of the pre-merge branch's own
    rendering, verified in `00-intake/proposal-engine-v4-test-2026-08-16.md`
    §6, but not re-checked against the rebuilt output before being
    reported clean. Separately, the same rebuild's Scope & Acceptance
    table was five hardcoded rows claiming acceptance criteria for
    capabilities (lead capture, property/listing, commission & deals,
    multi-agent access control, reporting) regardless of which modules
    the client had actually bought — the same overclaiming-fixed-list
    shape as the QWeb mirror in
    `sgc_quotation_proposal/reports/proposal_template.xml` (see that
    module's manifest guard, same date). None of this broke a gate check,
    threw an error, or failed `assert_required_sections()` — the document
    rendered, every heading was present, and the page count looked
    plausible both times, which is exactly why an identical page count
    across two different fixtures was the signal worth chasing rather
    than dismissing. Confirmed by walking the actual git history
    (`ba834cb0` vs `66d3d2f7`) rather than assuming either report was
    right. **Fixed**: exclusions now load the governed clause file's
    verbatim `"> "` blockquote text via `_load_exclusions_clause()`,
    raising `BlocksIssue` rather than rendering empty if the clause file's
    shape ever changes; the Scope & Acceptance table now derives its rows
    from the actual quoted module list. **Two lessons, not one: (1)
    "the document has a section with that heading" is not the same claim
    as "the section contains the governed content" — a check for the
    heading alone passes an empty or overclaiming section underneath it.
    (2) Changing a dict access from `d[key]` to `d.get(key, default)`
    during an otherwise-unrelated rebuild is itself a content-loss risk,
    not a defensive improvement — it converts a bug that would have
    crashed the very next run into one that renders silently forever;
    prefer the loud form unless the missing case is genuinely expected
    and handled, not merely tolerated.**
29. **A page-limit ceiling proven against Chrome headless is a different
    claim than a page-limit ceiling proven against the renderer this repo
    actually ships with.** Following #27/#28's reconciliation pass, the
    regenerated fixtures and a fresh adversarial overflow proof were
    verified with Chrome headless (`--headless --print-to-pdf`) because
    neither a local `wkhtmltopdf` install nor VPS/SSH access was available
    that session — disclosed at the time as a substitution, not silently
    presented as equivalent. On the next pass, VPS/SSH access and a real
    `wkhtmltopdf 0.12.6.1` binary (inside the `demo_presentation` Odoo
    container, unrelated to the frozen `sgc_staging` production database —
    no `-u`/`-i`, no DB touched, purely a stateless HTML-to-PDF convert)
    were both available, and the same fixtures were re-rendered through
    it. The page counts moved: F2 (`ZZZFIXTURE-2026-V4-02`) rendered at 5
    pages under Chrome and 4 pages under wkhtmltopdf — a real, measured
    discrepancy, not a hypothetical one. A fresh 150-row synthetic
    overflow injection was ALSO not decisive at this size — Chrome
    rendered it at exactly 10 pages and wkhtmltopdf at 9, both under the
    `>10` ceiling in `verify_pdf_page_limit.py`, proving nothing about
    whether the ceiling actually fires. The two adversarial files already
    staged from the prior overflow proof (`ADVERSARIAL_overflow_test.html`,
    `ADVERSARIAL_v2_test.html`) were re-rendered instead: 26 and 34 pages
    under real wkhtmltopdf (vs. 27 reported under Chrome for the same
    overflow file previously) — both correctly fail the 10-page check.
    **The enforcement mechanism itself is now confirmed live under the
    renderer this repo actually ships with, not only under a substitute.
    But any page count quoted for a document that is NOT decisively over
    or under the limit (a 4-vs-5-page fixture, unlike a 26-vs-34-page
    adversarial file) is renderer-specific and provisional until re-proven
    against wkhtmltopdf specifically** — wkhtmltopdf 0.12.6.1 is an old
    WebKit engine with materially different flow/pagination behaviour
    from a modern Chrome build. **Policy going forward, stated once here
    so it doesn't have to be re-derived: `wkhtmltopdf 0.12.6.1` inside the
    `demo_presentation` container is the canonical render path for any
    page count cited in a client-facing decision. Chrome headless is a
    local convenience for fast iteration only, never a substitute for the
    final check.** "A non-production container that happened to have
    0.12.6.1" is not by itself a reproducible render path — naming it
    (`demo_presentation`, an `odoo:19.0` image, no relation to
    `odoo-prod`/`sgc_staging`) and writing the exact command down
    (`05-ops/verify_pdf_page_limit.py`'s docstring) is what makes it one;
    this is not the first time in this
    repo's history that a page count looked stable across variants only
    because the wrong renderer was asked (see #26's `grep -a`-on-a-PDF
    lesson for the same shape of "the tool answered, but not the question
    that mattered").
30. **A recurring fee formalized to a formula still carries a fidelity
    gap the hand-computed version never surfaced this precisely: the
    engine function only implements half of its own documented formula,
    and every recurring line it has ever priced sits exactly on a floor
    with zero cushion.** `pricing_engine.platform_portion_aed_mo()`
    reproduces both real client figures it has been checked against
    exactly (Prosper 3,648/mo, RVN 1,170/mo, both #27's T20 checks) — but
    both of those figures are `cost_to_serve × gates.platform_floor_multiplier`
    (1.25) with nothing added, confirmed by reading the function directly
    (`round(cts_total_aed * platform_floor_multiplier)`). The governed
    formula everywhere else in this repo (`runbook/subscription-proposal-runbook.md`,
    `.opencode/skills/sgc-proposal-engine/SKILL.md`, RVN's own worksheet
    and `gate-report.md`) is `max(CTS × 1.25, market_defensible_floor)` —
    a second, higher floor candidate the function has no parameter or
    code path for at all. This has produced no wrong number yet only
    because `market_defensible_floor` has never been populated with a
    real value anywhere in this repo for any segment (grepped in full);
    the moment one is, `platform_portion_aed_mo()` will silently ignore
    it rather than take the max, because the max was never coded, not
    because it evaluated to a smaller number. Separately, and more
    consequential day-to-day: `cost_to_serve.support_hours_per_5_users: 1`
    in `policy.yaml` is a bare, uncited policy assumption, not a measured
    figure — `00-knowledge/pricing/support-hours-log.yaml` exists
    specifically to hold real measurements and is deliberately empty
    (`entries: []`) by design, "do not seed with estimated or invented
    figures" stated in its own header. Every recurring fee quoted to date
    is therefore cost-plus-zero-cushion against an *assumed* support-hours
    figure that the repo's own measurement mechanism has not yet
    validated. **Not fixed, not urgent per explicit direction — named for
    the record.** The build-side floor (`business_cost_floor()`,
    `known-defects.md` #27's subject) had the same shape one layer up:
    a governed number with no margin above it, discovered only once
    someone re-derived it independently instead of trusting that a
    formalized formula automatically means a safe one. Re-derive before
    trusting, one layer down: once `support-hours-log.yaml` has real
    entries, or once any segment gets a documented `market_defensible_floor`,
    recompute `platform_portion_aed_mo()`'s formula fidelity against both
    before treating the recurring line as settled.
