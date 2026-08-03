# UAE Tax / VAT — Vertical Note

Read before pricing any UAE deal, and before drafting §10 Commercial Terms.
This note explains the numbers pinned in `pricing/policy.yaml: vat` — it does
not replace them. If a client's situation doesn't fit the summary below,
escalate to the Commercial Desk rather than resolving it in the proposal.

## The pinned values

```yaml
vat:
  standard_rate: 0.05
  mandatory_threshold_aed: 375000
  voluntary_threshold_aed: 187500
  free_zone_exempt: false
```

- **Standard rate 5%** applies to taxable supplies UAE-wide, mainland and
  free zone alike, unless the supply is specifically zero-rated or exempt
  under UAE VAT law.
- **Mandatory registration threshold AED 375,000** — a business whose
  taxable supplies and imports exceed this over the preceding 12 months (or
  are expected to in the next 30 days) must register for VAT.
- **Voluntary registration threshold AED 187,500** — a business above this
  but below the mandatory threshold may register voluntarily. Relevant for
  a `startup_boutique` segment client not yet at mandatory scale.
- **`free_zone_exempt: false`** — being registered in a UAE free zone does
  **not**, by itself, exempt a business from VAT. Only supplies made by a
  business registered as a "Designated Zone" and meeting specific conditions
  (goods held within the zone, certain B2B fencing conditions) get VAT-free
  treatment on qualifying transactions. Most SGC clients — including free
  zone companies providing services or selling to the UAE mainland — are
  **not** exempt. **DO NOT CHANGE `free_zone_exempt` to `true`** for a client
  merely because they mention "free zone" in intake. Confirm Designated Zone
  status and transaction type before treating any supply as VAT-free, and
  flag the clause for human/legal review regardless.

## What this means for a proposal

- Odoo Accounting configuration for a UAE client always includes VAT setup
  scoped from `pricing/hour-lookup.yaml: uae_vat_localization` (8–20 hours),
  not folded silently into generic `finance_setup`.
- Quote all commercial figures **exclusive of VAT** with VAT called out as a
  separate line in §10 Commercial Terms, using
  `clause-library/vat-uae.md` verbatim.
- If the client is a Designated Zone entity claiming VAT-free treatment on
  the engagement itself (rare — SGC's services are typically standard-rated
  regardless of the client's zone status), do not resolve this in the
  proposal. Flag for human review before the draft goes out.
- TRN (Tax Registration Number) is a required field in
  `02-clients/{client}/manifest.yaml: client_trn`. If the client cannot
  supply one and claims to be under the voluntary threshold, note this
  explicitly in `00-intake/client-brief.yaml` — it may affect invoicing
  format, not the VAT rate applied.

This note is operating guidance, not legal advice. UAE VAT law and FTA
guidance change; if in doubt, escalate rather than guess.
