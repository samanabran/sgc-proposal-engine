# Escalation Triggers (v2)

Exactly when an SDR must stop and escalate rather than proceed. If any of
these apply, **stop, log the escalation in the client's `manifest.yaml:
escalations`, and route per `approval-matrix.md`.** Never resolve any of
the following by improvising, discounting, or paraphrasing around it.

## Any G1–G41 gate failure

Every gate failure is an escalation. Full definitions in
`commercial-rules/{subscription,payment-plan,protection}-guardrails.md`.
The highest-frequency triggers in practice:

| Gate | Fails when | Matching known defect |
|---|---|---|
| G1 Platform floor | Recurring price doesn't clear CTS × 1.25 | `known-defects.md` #1 |
| G3 Mobilisation ≥ 33% | Mobilisation short of 33% without a logged concession | — |
| G4/G16 Clawback present | Any deferred structure with no clawback clause | `known-defects.md` #8 |
| G8/G23 Margin floor | Margin below 30% target, or below 25% absolute (no approver may go here) | `known-defects.md` #1 |
| G9 Rate provenance | Any figure not traceable to `pricing/*.yaml`, including `forbidden_rates` | `known-defects.md` #2 |
| G11 Discount on recovery | A discount applied to the recovery portion, not just platform | `known-defects.md` #16 |
| G21/G22 Exposure/walk-away card | Pricing discussed with a client before the walk-away card exists | — |
| G35 False VAT claim | Any statement that SGC charges VAT or is registered | `known-defects.md` #10, #11 |
| G36–G38 Edition misdescription | Community described as Enterprise, or exclusions not disclosed in writing | `known-defects.md` #18 |

## Portfolio-level triggers (not deal-specific)

- Any early-warning indicator at `high` or `critical` tier fires
  (`07-protection/monitoring/early-warning-indicators.yaml`) — new
  deferred-payment structures pause per
  `07-protection/monitoring/graduated-response.md`.
- Peak cash exposure on a new deal would push the aggregate above
  `07-protection/exposure/portfolio-limits.yaml: max_aggregate_peak_cash_exposure_aed`.
- A client's risk score lands in the `refuse` band
  (`risk-security-matrix.yaml`) — this is an abort trigger
  (`07-protection/abort/abort-criteria.md`), not an escalation to
  negotiate around.

## Entity and brand triggers

- Any field in `06-brand/entity/legal-identity.yaml` is still `RESOLVE`
  and the document requires it (signature block, dispute-and-jurisdiction
  clause) — the document cannot be issued, full stop, until Founder +
  Commercial Desk resolve it.
- Any clause used from the library carrying `requires_counsel_review: true`
  has not actually been reviewed by counsel — escalate for review, don't
  issue the draft text as final.

## Rate, module, or work package not on the card

Escalate to Commercial Desk (`AGENTS.md` absolute rule;
`known-defects.md` #2).

## Quoting near a previously rejected budget

Escalate with a logged value justification before requoting near a
number the client has already declined (`known-defects.md` #14).

## Correction to an already-issued proposal

Never edit `05-issued/` in place. Escalate to Commercial Desk to
authorize a new revision or a `correction-notice.md`
(`known-defects.md` #9 v1 numbering / general immutability rule).
