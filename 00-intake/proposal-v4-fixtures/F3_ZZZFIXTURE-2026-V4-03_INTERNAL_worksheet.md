# INTERNAL WORKSHEET — F3 — ZZZFIXTURE-2026-V4-03 — ZZZ OVER-CAPACITY SYNTHETIC FIXTURE (not a real client)

**NOT FOR CLIENT TRANSMISSION.**

## One-time build (pe.four_component_build())
- template: {'price_aed': 12000, 'hours': 6, 'maturity': 'mature', 'derivation': 'fixed_fee', 'scope': None}
- modules: {'rows': [{'name': 'lead_capture_meta_google_ads', 'price_aed': 3000, 'hours': 4.0}, {'name': 'whatsapp_lead_notification', 'price_aed': 2500, 'hours': 3.0}, {'name': 'auto_distribution_manual_reassign', 'price_aed': 2000, 'hours': 3.0}, {'name': 'call_logging_manual_entry', 'price_aed': 2000, 'hours': 3.0}, {'name': 'attendance_in_app_checkin', 'price_aed': 3000, 'hours': 5.0}, {'name': 'daily_reporting_pack', 'price_aed': 2000, 'hours': 3.0}, {'name': 'multi_agent_access_control', 'price_aed': 3500, 'hours': 7.0}, {'name': 'property_portal_feed', 'price_aed': 4000, 'hours': 6.0}], 'price_aed': 22000.0, 'hours': 34.0, 'derivation': 'fixed_fee_per_catalogue_row'}
- migration: {'band': 'over_20000', 'price_aed': None, 'hours': None, 'unpriced': True, 'note': '[UNPRICED — Commercial Desk] — never estimate, quote only after seeing the data.', 'derivation': 'banded_fixed_fee'}
- price_ex_vat_aed: None, hours_total: None

## Recurring (pe.platform_portion_aed_mo())
{'users_now': 25, 'hosting_allocation_aed': 450.0, 'support_labour_aed': 1400, 'account_mgmt_aed': 350, 'tooling_aed': 50, 'cts_total_aed': 2250.0, 'platform_floor_multiplier': 1.25, 'platform_portion_aed_mo': 2812}

## Quote-time floor test: not computed -- migration UNPRICED, no total to test.

## Risk-adjusted hours (contingency schedule, policy.yaml -- local-only addition, survives merge unmodified)
- lead_capture_meta_google_ads: raw=4h, risk_adjusted=4.6h (contingency 15%)
- whatsapp_lead_notification: raw=3h, risk_adjusted=3.45h (contingency 15%)
- auto_distribution_manual_reassign: raw=3h, risk_adjusted=3.45h (contingency 15%)
- call_logging_manual_entry: raw=3h, risk_adjusted=3.45h (contingency 15%)
- attendance_in_app_checkin: raw=5h, risk_adjusted=5.75h (contingency 15%)
- daily_reporting_pack: raw=3h, risk_adjusted=3.45h (contingency 15%)
- multi_agent_access_control: raw=7h, risk_adjusted=8.05h (contingency 15%)
- property_portal_feed: raw=6h, risk_adjusted=6.9h (contingency 15%)

- quotation_validity: NO policy.yaml value exists for a standard validity period as of this pass — printed as [OPEN] on the client document, not a plausible-but-invented date.