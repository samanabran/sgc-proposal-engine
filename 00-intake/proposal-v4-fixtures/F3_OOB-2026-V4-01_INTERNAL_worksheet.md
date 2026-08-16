# INTERNAL WORKSHEET — F3 — OOB-2026-V4-01 — Over-Capacity Test Client

**NOT FOR CLIENT TRANSMISSION.**

- platform_fee_aed: 14000
- modules_total_aed: 16000 (lead_capture_pipeline, property_listing_management, commission_and_deals, multi_agent_access_control, reporting_and_dashboards)
- migration_band: above_band_3, amount_aed: None, unpriced: True
- quoted_total_aed: None
- discount_gate: None

## Internal hours (raw vs risk-adjusted, INTERNAL ONLY)
- multi_agent_access_control: raw=7h, risk_adjusted=8.05h (contingency 15%)
- TOTAL: raw=7.0h, risk_adjusted=8.05h

## Floor guard: not computed — no risk-adjusted internal hours available for this fixture's module selection (only multi_agent_access_control carries an internal_build_estimate_hours figure in template-catalogue.yaml; a fixture without it has nothing to floor-check against yet).

- quotation_validity: NO policy.yaml value exists for a standard validity period as of this pass — printed as [OPEN] on the client document, not a plausible-but-invented date.