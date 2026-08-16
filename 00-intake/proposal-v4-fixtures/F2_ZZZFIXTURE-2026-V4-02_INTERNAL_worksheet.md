# INTERNAL WORKSHEET — F2 — ZZZFIXTURE-2026-V4-02 — ZZZ MINIMAL SYNTHETIC FIXTURE (not a real client)

**NOT FOR CLIENT TRANSMISSION.**

## One-time build (pe.four_component_build())
- template: {'price_aed': 12000, 'hours': 20, 'maturity': 'first_build', 'derivation': 'fixed_fee', 'scope': None}
- modules: {'rows': [{'name': 'lead_capture_meta_google_ads', 'price_aed': 3000, 'hours': 7.2}], 'price_aed': 3000.0, 'hours': 7.2, 'derivation': 'fixed_fee_per_catalogue_row'}
- migration: {'band': 'up_to_1000', 'price_aed': 2500, 'hours': 4, 'unpriced': False, 'note': None, 'derivation': 'banded_fixed_fee'}
- price_ex_vat_aed: 17500.0, hours_total: 31.2

## Recurring (pe.platform_portion_aed_mo())
{'users_now': 5, 'hosting_allocation_aed': 90.0, 'support_labour_aed': 280, 'account_mgmt_aed': 100, 'tooling_aed': 50, 'cts_total_aed': 520.0, 'platform_floor_multiplier': 1.25, 'platform_portion_aed_mo': 650}

## Quote-time floor test (pe.hour_rate_floor_test())
- price_ex_vat_aed: 17500.0
- hours_total: 31.2
- commission_aed: 2450.0
- net_aed: 15050.0
- effective_rate_aed_hr: 482.37
- floor_per_hour_aed: 394.38
- gross_break_even_aed_hr: 458.58
- cushion_pct: 22.31
- verdict: PASS
- NOTE: gross_break_even_aed_hr (458.58) is a REPORTED METRIC, not a threshold -- a quote billed at exactly that gross rate earns zero cushion. The verdict above (BLOCK/WARN/PASS) is the actual gate.

## Risk-adjusted hours (contingency schedule, policy.yaml -- local-only addition, survives merge unmodified)
- lead_capture_meta_google_ads: raw=4h, risk_adjusted=4.6h (contingency 15%)

- quotation_validity: NO policy.yaml value exists for a standard validity period as of this pass — printed as [OPEN] on the client document, not a plausible-but-invented date.