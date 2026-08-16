# Pricing v4 — Initial Production Test (render path, no Odoo, no DB)

**Date**: 2026-08-16. **Method**: `05-ops/render_proposal_v4.py` (standalone HTML generator, offline) → transferred to `vps-root` → rendered via `wkhtmltopdf 0.12.6.1` inside the already-running `demo_presentation` container (binary invocation only — no Odoo process, no database read/write, no `-u`/`-i`, no container restart) → PDF pulled back and page-counted locally with `pypdf`. `sgc_staging` / `postgres-prod` were never touched.

---

## 1. What "production test" means here, stated plainly

This tests the **render path** — can the pricing v4 commercial model produce a correctly-computed, correctly-limited, correctly-worded client document end to end. It does **not** test the Odoo module, because installing it was explicitly out of scope this session (database freeze on `sgc_staging`/`postgres-prod`). See §7 for the full list of what this does not prove.

---

## 2. Prosper design-spec extract (Part 5.1)

Read before building anything: `02-clients/PRO-prosper-realestate/04-draft/render_brand.py` (the actual script that rendered Prosper's real Rev3 client documents), `06-brand/tokens/color.yaml`, `06-brand/registry.yaml`, `06-brand/entity/legal-identity.yaml`, `PRO-2026-SUB-01_Rev3_Offer.md` (real sent-shape document), `PRO-2026-SUB-01_Rev1/10-commercial-terms.md` (full 13-section formal proposal, commercial-terms convention).

| Element | Real convention found | Source |
|---|---|---|
| Type | Playfair Display 700 (headings) + Inter (body/UI) | `render_brand.py` header comment — explicitly supersedes `tokens/type.yaml`'s IBM Plex default for proposal work, "the precedent actually in force" |
| Colour | 7 client-safe tones only: ivory, navy, gold, charcoal, slate, champagne, parchment | `06-brand/tokens/color.yaml` — `midnight`/`emerald`/`amber`/`wine` reserved for internal status signalling per that file's own `usage_notes`, never client-facing |
| Grid | A4 portrait, 20mm margin, 170mm content width | `render_brand.py` |
| Table style | Navy header row, ivory uppercase text; champagne 1px cell borders | `render_brand.py` CSS; `10-commercial-terms.md`'s pricing-summary table shape |
| Exclusions shape | 3-column table (Requirement / Priority / Status) | `PRO-2026-SUB-01_Rev3_Offer.md` "What this does not include" — this generator extends it with a 4th "Alternative Offered" column, per this pass's own requirement, not inventing the base shape |
| Financing/legal disclosure | Blockquote | `PRO-2026-SUB-01_Rev3_Offer.md` "Term commitment" section |
| Signatory source | Single source of truth, never re-typed | `06-brand/entity/legal-identity.yaml` — this file's own header states it is "the single source for every footer, cover page, and signature block in every issued document," written after a real defect (Rev1/Rev2 stated two different registered addresses) |
| Logo | None — text wordmark only | `06-brand/registry.yaml` status_note: `assets/logos/` still empty, `.gitkeep` only, no logo file supplied as of this version; matches what Prosper's own real rendered documents already do |
| Watermarks | 18 pre-composited UAE-landmark assets, rotation mapped per section | `06-brand/assets/watermarks/rotation.yaml`, `registry.yaml` — but `render_brand.py` itself skips them for shorter/single-topic documents, reserving them for "the full 13-section formal proposal" |

**Two deviations from Prosper's convention, disclosed per Part 5.1's own instruction, not silent:**
1. **Watermarks not wired.** This document's 10-section structure sits between Prosper's two real shapes (a full 13-section formal proposal, which gets watermarks, and a short single-topic letter, which doesn't) — arguably closer to the former, but implementing 18-asset rotation logic was judged disproportionate to this pass's actual goal (get the v4 commercial model rendering correctly end-to-end). Flagged, not silently skipped, same reasoning `render_brand.py` itself already used for a similar document shape.
2. **VAT/registration status always printed** on the commercial-summary page, per Part 5.4's explicit instruction — this supersedes `AGENTS.md`'s older conditional-disclosure rule (silent unless the client/SDR raises it) for v4 documents specifically. A direct, current instruction, not a reinterpretation of the old one.

---

## 3. Fixture outputs

| Fixture | Modules | Migration | Computed total | Discount gate | Pages | Page-limit verdict |
|---|---|---|---|---|---|---|
| **F1** | all 5 | 3,000 records (band_2, 5,000) | **AED 35,000** | OK | 10 | PASS |
| **F2** | lead_capture_pipeline only | 500 records (band_1, 2,500) | **AED 19,500** | OK (see §4 bug) | 10 | PASS |
| **F3** | all 5 | 25,000 records (above band_3) | **UNPRICED — Commercial Desk** (never a number) | N/A (unpriced) | 10 | PASS |

Every total is exactly what F1/F2/F3's own spec expected (35,000 / 19,500 / UNPRICED). All computed via `pe.reference_quote_total_aed()`/`pe.modules_subtotal_aed()`/`pe.migration_band_for_records()` — nothing hand-typed.

**F3's commercial-summary page prints, verbatim**: *"Total: [OPEN — migration UNPRICED]"* with the migration line reading *"UNPRICED — routed to Commercial Desk"* — never a number, confirmed by direct inspection of the rendered HTML/PDF.

Artifacts (all in `00-intake/proposal-v4-fixtures/`): `{F1,F2,F3}_*_client.html`, `{F1,F2,F3}_*_client.pdf`, `{F1,F2,F3}_*_INTERNAL_worksheet.md`.

---

## 4. A real bug found while wiring this, fixed before this report was written

`discount_gate_verdict()` (built in Part 2) originally compared **every** quote against the fixed reference-quote floor (31,500, 90% of the 5-module 35,000 reference deal) — so F2 (genuinely smaller scope, 1 module, 19,500) incorrectly triggered `COMMERCIAL_DESK_APPROVAL_REQUIRED` for being a smaller *number*, not for being *discounted*. Caught by actually running the generator against F2, not assumed correct. Fixed: the gate now compares a quote against 90% of **its own scope's** undiscounted total (`undiscounted_total_aed` parameter, defaulting to the reference quote only to preserve Part 4's T23 exact call signature). T23 re-verified unchanged after the fix (`05-ops/test_pricing_engine.py`, still passing). Logged in HANDOVER.md decision #18.

---

## 5. Mechanical page-limit enforcement — proven, not assumed

All three real fixtures rendered to exactly 10 pages. **That result alone would not prove the enforcement mechanism works** — `render_proposal_v4.py`'s CSS forces `page-break-after: always` on all 10 fixed sections, so "10 pages" is partly a product of that construction (one section, one page, always), not solely evidence that overflow would be caught.

To actually test it: built `05-ops/verify_pdf_page_limit.py` (reads a rendered PDF's real page count via `pypdf`, exits non-zero above the limit) and ran it against a deliberately bloated adversarial fixture (150 injected filler list items in one section, forcing that section past one physical page). Result:

```
FAIL: .../ADVERSARIAL_overflow_test.pdf has 22 pages, exceeds the 10-page limit
exit code: 1
```

**The enforcement is real** — confirmed by making it fail on purpose, then removing the adversarial artifact (not part of the deliverable; the real F1/F2/F3 outputs are unaffected).

---

## 6. Content-rule compliance (Part 5.4) — checked, not assumed

- Grepped all three client HTML files for `394.38`, `458.58`, contingency/risk-adjusted language, capacity figures: **zero matches** beyond the module name "Commission and Deals" and descriptive scope text about what commission tracking does functionally — the actual 14% rate, either floor, and every internal hour figure are absent from every client document, present only in the paired `_INTERNAL_worksheet.md` files.
- Platform fee prints as a flat line (`AED 14,000`), never as hours × rate — confirmed by inspection; `pe.platform_fee_aed()` structurally cannot receive an hours argument (Part 4 T24).
- Migration prints its band and record ceiling (e.g. "Migration (5,000 records ceiling)"), never a raw record count with no context.
- Enhancement prints the rate and "quoted per request," explicitly not offered as a whole-deal basis.
- Exclusions table: all 5 named capabilities (WhatsApp, call logging, call-target enforcement, biometric attendance, portal feeds) print with a stated alternative beside each — confirmed by inspection of the rendered table.
- Version lock: "Odoo 19 Community" prints on the capability-summary page in every fixture.
- VAT: prints "not currently registered — no VAT charged" (source: `06-brand/entity/legal-identity.yaml: vat_registered: false`, consistent with `policy.yaml: vat.registered: false`).
- Quotation validity: prints literally `[OPEN — no policy.yaml value exists for a standard validity period; see internal worksheet.]` — **not** a plausible invented date. Confirmed: no such value exists anywhere in `00-knowledge/pricing/*.yaml` (checked before writing this line).
- Deciding-human line: populated in all three fixtures (`06-brand/entity/legal-identity.yaml: contact.actual_signer` = Renbran Anthony Madelo, acting on behalf of the named Company Manager). The `[BLOCKS ISSUE]`/non-zero-exit path exists in `render_proposal_v4.py` (`BlocksIssue` exception, raised by `_deciding_human()`) but was not exercised by real data in this pass — it is code that has never fired, not proven under load.
- Warrant-tier lint (Part 5.5): `_warrant_tier_lint()` scans every rendered document for T1-shaped phrasing ("proven in production," "production-proven," "already proven"). **Zero hits across all three fixtures** — every capability in `template-catalogue.yaml` is tagged `warrant_tier: T2`, and none of that language was ever written into the templates, so this lint has not yet been exercised against a genuine T1-vs-T2 violation either (see §7).

---

## 7. QWeb parity (Part 6.3)

`sgc_quotation_proposal/` (staged, not installed) mirrors the standalone generator's 10 sections and field names, authored side by side, same content. **One real divergence found and disclosed, not smoothed over**: the standalone generator derives each exclusion's display name from a dict key at render time (`key.replace('_',' ').title()`); the QWeb template assumes a pre-formatted `name` field would already exist in the rendering context. The two are not byte-identical without a controller-side transform that does not exist yet — logged in HANDOVER.md decision #18 as an open item before this module is ever installed.

**True QWeb-engine rendering was not performed** — that requires Odoo, explicitly out of scope this session (database freeze). "Parity" here means structural/content parity by construction, checked by reading both files side by side, not a rendered-output diff.

---

## 8. WHAT THIS TEST DOES NOT PROVE

Stated plainly, per the standing honesty rules:

- **It does not prove the Odoo module renders in Odoo.** `sgc_quotation_proposal` has never been installed or executed by Odoo's QWeb engine this session. Structural parity with the standalone generator is asserted by side-by-side authorship, not verified by an actual render-and-diff pass.
- **It does not prove the template deploys.** No `-i`/`-u`, no database write, no install attempt was made or permitted.
- **It does not prove any underlying capability claim** (lead capture, WhatsApp, etc.) works in a live system — that evidence (or its absence) is `00-intake/demo-presentation-inventory-2026-08-16.md`'s job, not this test's. This test only proves the *document* correctly describes what is and isn't included, at the tier warranted.
- **It does not prove the floor guard is meaningful for a whole deal.** F1's internal worksheet computes an effective rate of 3,739 AED/hr — because `template-catalogue.yaml` currently records an internal hour estimate for only ONE of the five modules (`multi_agent_access_control`, 7h). The other four modules have fixed prices but no recorded internal hour estimate at all, so F1's "floor guard: PASS" reflects that one line item clearing the floor by a wide margin, not a genuine whole-deal effort-vs-price check. A real whole-deal floor check needs hour estimates for every module — not supplied in this pass's brief beyond the one flagged line. Flagged here rather than presented as a clean PASS without qualification.
- **It does not prove the warrant-tier lint catches a real violation** — it has only been run against documents that never contained T1-shaped language in the first place (this generator's own templates don't write it). The lint mechanism exists and runs on every fixture, but, like the page-limit checker before its adversarial test, it has not yet been proven against a genuine failing case.
- **It does not prove the `[BLOCKS ISSUE]` deciding-human path works under real failure** — `legal-identity.yaml` has a populated signer for every fixture in this pass, so that code path has never actually executed.
- **It does not prove font/watermark fidelity beyond what was checked.** Google Fonts resolution and embedding WAS verified directly (`curl` returned HTTP 200 from inside the render container; `pypdf` confirms `PlayfairDisplay-Bold`/`Inter-Bold`/`Inter-Medium` are embedded in the output PDF, not a generic fallback) — but this depended on the render environment having live internet access at render time, which is an environmental fact about this specific VPS, not a guaranteed property of every future render environment.
- **It does not prove the two disclosed deviations (watermarks, VAT-always-print) are the right calls** — they are stated, reasoned decisions carried into HANDOVER.md decision #18 for Commercial Desk to confirm or overrule, not settled facts.
- **It does not prove this document would survive a real client's scrutiny** — only that it renders, computes correctly, stays within the mechanical page limit, and does not leak internal figures. Tone, persuasiveness, and commercial framing were not independently reviewed against Prosper's real sent documents beyond the structural elements listed in §2.
