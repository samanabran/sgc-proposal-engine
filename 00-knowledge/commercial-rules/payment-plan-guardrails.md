# Payment Plan Guardrails — G11–G20

Govern cadence, concessions, and security. See `PRECEDENCE.md` — these
extend, not replace, G1–G10.

| Gate | Rule | Test | Owner |
|---|---|---|---|
| **G11** | Discounts apply to the platform portion only | `payment-plans.yaml: discount_applies_to: platform_portion_only` — the recovery portion of the subscription is never discounted; the only lever on recovery is reducing/removing the financing uplift, because recovery principal is work already performed | Commercial Desk |
| **G12** | Cadence values are ceilings, margin floor binds | `applied_give = min(cadence_table_ceiling, max_give_aed)` — always apply the lower of the two, never the cadence table value on its own | Finance |
| **G13** | Total give capped | `total_give ≤ min(0.10 × contract_value, margin-floor-implied max)` | Finance |
| **G14** | Every concession carries logged, equal-or-greater compensators | Run `concession-ladder.yaml` procedure in full; an unlogged concession is void — the worksheet reverts | SDR + Commercial Desk |
| **G15** | Security sized to risk band | `risk-security-matrix.yaml` bands `elevated` and above cannot proceed with zero security instrument | Commercial Desk |
| **G16** | Every deferred structure carries a clawback | No approver, at any authority level, may waive `clause-library/clawback.md` | Commercial Desk (absolute floor — see PRECEDENCE.md) |
| **G17** | Guarantees are service credits only | Individually capped, and capped in aggregate at 10% of annual contract value; never a cash refund (`clause-library/service-credit-guarantee.md`) | Finance |
| **G18** | Client data export is unconditional | Survives any dispute; suspension (`clause-library/suspension-and-reinstatement.md`) applies to service access only, never to data export | Commercial Desk (absolute floor — see PRECEDENCE.md) |
| **G19** | No structure reduces hours, PM, QA, or documentation | Applies to every cadence, concession, and one-time structure — see `concession-ladder.yaml: forbidden_compensators` | SDR + validate script |
| **G20** | Non-standard structures require authority matrix sign-off | `04-governance/approval-matrix.md`; absolute margin floor is 25% regardless of who approves | Sales leadership |

## On a failed gate

G11/G12 failures usually mean a discount was applied to the wrong base —
recompute against the platform portion only. G15 failing on an elevated-
or-higher risk score is a hard stop, not a judgment call: get the security
instrument in place first. G16/G18 are absolute floors — there is no
approval path that waives them, at any deal size.
