# Walk-Away Deal Card — RVN-2026-SUB-01_Rev1

**Produced before any pricing conversation with the client (G22).**
One page. Nothing beyond what's below.

## Three numbers

| | AED/mo |
|---|---|
| List (target margin 35%, platform-portion basis) | 1,680 |
| Target floor (30% margin) | ~1,584 |
| **Absolute floor (25% margin — no approver may go below this)** | ~1,470 |

(List = quoted Subscription Fee, `02-calc/pricing-worksheet.yaml: assembly.subscription_fee_aed_mo`.
Target/absolute floors derived pro-rata against the worksheet's computed
gross margin (34.3% at list) — recovery-portion component is never
discounted per G11; any give comes from the platform portion only.)

## Total give available

AED 4,538 over the full term (10% of contract value AED 45,378, the
`hard_caps.max_total_give_pct_of_contract_value` ceiling), or the
margin-floor-implied max, whichever is smaller — see G13. **Currently
zero given.**

## Risk band and required security

Band: **moderate** (`pricing/risk-security-matrix.yaml`, score 27/100 —
4 of 8 inputs are call-transcript ASSUMPTIONS, scored toward the
higher-risk side; see `02-calc/risk-assessment.yaml`).
Required instrument(s): **Mobilisation at 33% (AED 5,058 at Kickoff) +
Security Deposit, 1 month (AED 1,680, refundable)** — both required per
the moderate band, not mobilisation alone.

## Top 3 compensators for this deal

1. Annual-prepay billing cadence (removes the Recovery Component
   entirely and improves cash position further).
2. Extended Initial Term beyond 24 months (extends the recovery window —
   relevant if Nazim pushes back on the 24-month commitment).
3. Reference-and-case-study credit (AED 2,500, max 1 per deal) — RVN is
   a first-CRM adopter in a visible vertical; a strong candidate for this
   compensator if a concession is later requested.

(from `pricing/concession-ladder.yaml: compensators` — pre-selected
before the Monday conversation, not improvised mid-negotiation.)

## Abort criteria

Reference `07-protection/abort/abort-criteria.md`. None currently
triggered. Specifically: margin clears 25% absolute floor at 34.3%
(worst-case 28.7%, G23/G31); cash-positive within 30 days — day 1
(G32); clawback present on the deferred value (G4, G16); no VAT
misstatement (G35); edition Community not described as Enterprise
(G36); no named consultant (G27); no exclusivity (G10); moderate-risk
security instruments both present (G15).

**Watch item, not an abort trigger**: two of the client's stated "must
have" features (automated call-analyzer/telephony integration, sensor-
based attendance tracking) have no catalogue price and are explicitly
excluded from Phase 1. If Nazim treats either as a hard condition of
approval rather than a Phase 2 discussion, re-evaluate before
committing to a number on either — do not invent a price under
pressure in the room (G9).

## Incumbent benchmark

Not applicable — client explicitly stated no fixed CRM budget and no
incumbent CRM cost ("whatever you are proposing, that will be the first
decision," transcript 16:07-16:12). RVN evaluated 5-6 other vendors
(India + Dubai) and was unconvinced by their packages, but no pricing
figures were shared. AED 15,000-60,000/month figures on the call are
ad-spend, not a CRM budget anchor — do not present Year 1 (AED 25,218)
against those figures as a comparison.
