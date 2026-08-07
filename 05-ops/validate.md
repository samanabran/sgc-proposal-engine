# Running the Gate Check

`validate.py` (Python, stdlib + PyYAML only) implements the 19 checks
below against a client folder. Run it before every human review, and
before every issue.

```
python 05-ops/validate.py 02-clients/{client}/
```

Exit code 0 means clean. Non-zero means at least one check failed — the
script prints which one and why, then exits.

## The 19 checks

1. All pricing YAMLs parse; no `forbidden_rates` (690) anywhere in the
   client folder.
2. `pricing-worksheet.yaml` complete; every rate traces to `rate-card.yaml`.
3. PM, QA, documentation, and contingency lines all present in
   `number_2_build`.
4. Total hours meet or exceed a comparable benchmark (roughly 9.2 hours
   per user at `startup_boutique` scale — derived from the reference
   worksheet, not an external source; recalibrate as more deals close).
5. Every capability named in §06 has corresponding hours in
   `number_2_build.delivery_hours` — cross-reference check.
6. All 41 named gates evaluated in `pricing-worksheet.yaml: gates`, each
   with a recorded `pass` value; any `false` blocks issue.
7. Worst-case gate (G31): concessions plus maximum guarantee-credit
   exposure, applied together, still clears the 25% absolute margin floor.
8. Cash-positive within 30 days (G32) — `exposure.cash_positive_by_day`
   must be ≤ `policy.yaml: gates.cash_positive_within_days`.
9. Cadence at or above quarterly-in-advance (G33), unless a logged
   exception exists.
10. Mobilisation ≥ 33% and ≥ any triggered third-party upfront cost (G34).
11. No VAT charged; `vat-gross-up.md` referenced; no VAT-registration
    claim anywhere in the draft (G35).
12. Edition declared; if Community, upgrade policy stated and exclusions
    listed (G36–G38).
13. Clawback present on any deferred structure (G16).
14. All entity fields resolved in `06-brand/entity/legal-identity.yaml`
    — **this check is expected to fail until real entity facts are
    supplied.** It is not a bug in the client folder; it is the entity
    file doing its job. A client folder can have all 41 commercial gates
    pass and still correctly fail this check.
15. Brand tokens only from `06-brand/registry.yaml`; no off-palette
    colour.
16. `verbal-promises.md` exists; every entry classified PRICED / DEFERRED
    / EXCLUDED.
17. Evidence file checklist complete before a `go-live` flag is set
    (`07-protection/evidence/evidence-file-standard.md`).
18. No forbidden phrase anywhere in the draft or issued document (not
    counted against `04-review/qa-checklist.md`, which is expected to
    name them): `bargain`, `not on our public list`, `will not be
    extended to any other brokerage`, `no VAT applies`, `VAT-registered`,
    `Odoo Enterprise` (if edition = community), `iOS / Android app` (if
    edition = community).
19. No internal narration/strategy vocabulary anywhere in the draft or
    issued document — a distinct failure mode from check 18: these
    phrases don't misstate a commercial term, they leak SGC's own
    authoring process or an unconfirmed-input caveat into client-facing
    prose. Currently: `disarm-hesitation`, `placeholder-driven`
    (`INTERNAL_VOCABULARY_PHRASES` in `validate.py` — extend as found,
    evidence-based, not pre-populated with hypotheticals). Scoped to
    exclude the deliberate "INTERNAL DRAFT — NOT FOR CLIENT TRANSMISSION"
    banner and similar required disclaimers by keeping the phrase list
    narrow rather than by any line-level exemption logic.

## Reading the output

The script separates **gate failures** (checks 1–13, 16–19 — these block
a deal from being commercially or legally sound) from the **entity
resolution blocker** (check 14 — this blocks issue specifically because
a real fact is genuinely still unknown, not because anything about the
deal itself is wrong). A client folder that passes checks 1–13 and 15–19
but fails check 14 is commercially clean and administratively blocked —
report it that way, don't conflate the two.

## Testing validate itself

Run it against a deliberately broken copy to confirm each defect is
caught independently: a rate of 690 anywhere, a missing clawback, an
edition claiming Enterprise capability with zero licence cost recorded,
or the string "VAT-registered" appearing outside the QA checklist file.
See `05-ops/validate.py`'s own `if __name__ == "__main__"` block for how
to point it at a fixture directory.
