# Validate — Running the G1–G10 Gate Check

The exact procedure for running the gate check against a completed
`02-calc/pricing-worksheet.yaml` and writing `02-calc/gate-report.md`.
Use this as a literal checklist. Gate definitions are in
`commercial-rules/subscription-guardrails.md` — this file is the
*procedure*, that file is the *definitions*; don't duplicate the gate
logic here, reference it.

## Preconditions

- [ ] `02-calc/pricing-worksheet.yaml` is complete: `number_1_cost_to_serve`,
      `number_2_build`, `number_3_financing`, and `assembly` are all filled,
      in that order (`runbook/subscription-proposal-runbook.md` §2). Do not
      run gates against a partially-filled worksheet.
- [ ] `manifest.yaml: knowledge_version_used` is pinned to the current
      `CHANGELOG.md` version before you start — the gate check is only
      meaningful against a specific, recorded pricing version.

## Procedure

Work through the gates in order (G1 → G10), writing each result directly
into `02-calc/gate-report.md` as you go — don't batch them at the end,
since an early failure changes what's worth checking later.

1. **G1 — Platform floor.** Pull `cts_total_aed` from
   `number_1_cost_to_serve`. Compute `platform_floor_aed = cts_total_aed ×
   policy.yaml: gates.platform_floor_multiplier (1.25)`. Check
   `cts_total_aed × 1.25 ≤ build_value_aed + cts_total_aed`. Record pass/
   fail with the actual numbers, not just "pass" — the arithmetic is the
   audit trail.
2. **G2 — Term ≥ recovery.** From `number_3_financing`, confirm
   `mobilisation_aed + recovery_total_aed` is fully recovered within
   `term_months`. If mobilisation is spread with uplift over the term,
   confirm the recovery schedule completes at or before the final month,
   not after it.
3. **G3 — Rate provenance.** Walk every rate, hour figure, and percentage
   in the worksheet and confirm each one cites a specific key in
   `pricing/*.yaml`. Any figure that doesn't have a citable source key
   fails this gate — see `AGENTS.md`: "if you cannot cite the source file
   and key, delete the number."
4. **G4 — Documentation coverage.** Check `documentation_hours ≥
   max(overlays.documentation_hours_min, 5% of dev hours)` using the
   values from `policy.yaml: overlays` and the worksheet's dev-hour total.
5. **G5 — QA coverage.** Check `qa_hours ≥ max(overlays.qa_hours_min, 8%
   of delivery hours)`, same source.
6. **G6 — PM coverage.** Confirm the PM line in the worksheet equals the
   segment's `pm_pct` × subtotal (10% startup, 15% smb/mid_market per
   `policy.yaml: segments`).
7. **G7 — Segment rate integrity.** Confirm the segment used matches the
   client's user count against `policy.yaml: segments.*.max_users`, and
   that `blended_rate_aed` used matches that segment's pinned rate exactly
   (280 / 395 / 525).
8. **G8 — Gross margin floor.** Compute `(assembly value −
   internal_build_cost_aed) / assembly value` using
   `cost_to_serve.internal_consultant_cost_aed_hr` for the cost side.
   Check ≥ `gates.min_gross_margin` (0.30); flag if below
   `gates.target_gross_margin` (0.35) even if it still passes the floor —
   worth a note even on a pass.
9. **G9 — Market test.** Pull `incumbent_benchmark_aed_mo` from the
   client brief. Check `year1_client_cost_aed ≤ incumbent_benchmark_aed_mo
   × 12 × gates.max_multiple_of_incumbent (1.30)`.
10. **G10 — Budget test.** Check the client brief for
    `budget_rejected_aed`. If none is present, record G10 as
    **pass (not triggered)** — this is a valid pass state, not a skipped
    gate. If present, check `year1_client_cost_aed` doesn't meet or exceed
    it without a logged value justification.

## Writing `gate-report.md`

For each gate, record:

- Gate ID and name.
- The formula, with the actual numbers substituted (not just the
  worksheet's abstract keys — a reviewer should be able to verify the
  arithmetic without opening the worksheet).
- Pass / fail.
- If fail: which remediation path applies (`subscription-guardrails.md:
  On a failed gate`) and the escalation logged in `manifest.yaml`.

Close with a summary line: `gates_passed: true` only if all 10 gates
passed. If any gate failed and was subsequently resolved by a scope
change, keep the original failing run in the report (don't overwrite it)
and add the re-run below it — the failure and its resolution are both
part of the audit trail (`04-governance/review-log.md` conventions apply
the same way here).

## On any failure

**Stop. Do not proceed to draft.** Follow
`04-governance/escalation-triggers.md` §1 and log the escalation in
`manifest.yaml: escalations` before doing anything else. Reduce scope and
re-run the full gate check from G1 — a partial re-check after a scope
change isn't sufficient, since a change made to fix one gate can affect
others (e.g. cutting a module changes `build_value_aed`, which affects
G1, G8, and G9 simultaneously).

## After all 10 gates pass

Set `manifest.yaml: gates_passed: true`. Only at this point does the
runbook allow moving from calc to draft
(`runbook/subscription-proposal-runbook.md` §3–4).
