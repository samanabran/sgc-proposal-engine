# Notification Template 2 — To SGC Signatory on Completion

Sent to the SGC authorised signatory (hello@sgctech.ai) when the envelope
reaches `completed` status (both parties signed).
Plain text and HTML versions.

Brand tokens used: `IBM Plex Sans`, `#0F213D` (navy), `#B79554` (gold),
`#F7F4EE` (ivory), `SGC TECH AI`, `Scholarix Global Consultants FZCO`.

---

## Plain text

```
Subject: [ACTION REQUIRED] {proposal_ref} — Fully Executed by Both Parties

Ali,

{client_signatory_name} has countersigned {proposal_ref}. The envelope is
now fully executed by both parties.

EXECUTED FIGURES

  Client:               {client_legal_name}
  Opportunity:          {proposal_ref}
  Term:                {contract_term_months} months
  Monthly Subscription: AED {subscription_fee}
    Platform portion:   AED {platform_fee}
    Recovery portion:   AED {recovery_fee}
  Mobilisation:        AED {mobilisation_amount}
  Payment Cadence:     {cadence}
  Edition:             {edition}
  Kickoff Target:      {kickoff_date}
  Signed at:           {completed_timestamp}

ATTACHED

  - {proposal_ref}_Signed.pdf
  - {proposal_ref}_AuditCertificate.pdf

ODOO RECORD

  Opportunity: {proposal_ref}
  Stage:       Won
  URL:         {odoo_opportunity_url}

INVOICE

  Mobilisation invoice drafted as DRAFT in Odoo.
  DO NOT POST until payment is confirmed.
  Review at: {odoo_invoice_url}

NEXT STEP: Review the Odoo record and post the mobilisation invoice
once payment is confirmed.

SGC TECH AI — Scholarix Global Consultants FZCO
hello@sgctech.ai | +971 52 198 5231
```

---

## HTML

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  body { font-family: 'IBM Plex Sans', Arial, sans-serif; font-size: 15px;
         color: #1C2430; background: #F7F4EE; margin: 0; padding: 0; }
  .container { max-width: 600px; margin: 40px auto; background: #ffffff;
               border: 1px solid #D9C08A; }
  .header { background: #0F213D; color: #ffffff; padding: 32px 40px; }
  .header h1 { font-family: 'IBM Plex Serif', Georgia, serif; font-size: 22px;
                font-weight: 700; margin: 0; }
  .header p { margin: 4px 0 0; color: #B79554; font-size: 13px; }
  .content { padding: 32px 40px; }
  h2 { font-family: 'IBM Plex Serif', Georgia, serif; font-size: 18px;
        color: #0F213D; margin: 0 0 16px; }
  h3 { font-size: 13px; font-weight: 600; color: #B79554; margin: 24px 0 8px;
        text-transform: uppercase; letter-spacing: 0.05em; }
  p { line-height: 1.75; margin: 0 0 12px; }
  table { width: 100%; border-collapse: collapse; margin: 16px 0;
           font-size: 14px; }
  th { text-align: left; padding: 8px 12px; background: #F7F4EE;
        border-bottom: 1px solid #D9C08A; color: #0F213D; font-weight: 600; }
  td { padding: 8px 12px; border-bottom: 1px solid #ECE7DF; }
  td:last-child { text-align: right; font-variant-numeric: tabular-nums; }
  .alert { background: #0F213D; color: #ffffff; padding: 16px 20px;
            margin: 24px 0; }
  .alert p { margin: 0; font-weight: 600; color: #B79554; }
  .alert .body { color: #ffffff; font-weight: 400; margin-top: 8px; }
  .footer { background: #0F213D; color: #D9C08A; padding: 24px 40px;
             font-size: 12px; }
  .footer p { margin: 0; }
  a { color: #B79554; }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>SGC TECH AI</h1>
    <p>FINANCE &middot; SYSTEM &middot; TECHNOLOGY</p>
  </div>
  <div class="content">
    <h2>[ACTION REQUIRED] {proposal_ref} — Fully Executed</h2>
    <p>Ali,</p>
    <p><strong>{client_signatory_name}</strong> has countersigned
    <strong>{proposal_ref}</strong>. The envelope is now fully executed
    by both parties.</p>

    <h3>Executed Figures</h3>
    <table>
      <tr><th>Client</th><td>{client_legal_name}</td></tr>
      <tr><th>Opportunity</th><td>{proposal_ref}</td></tr>
      <tr><th>Term</th><td>{contract_term_months} months</td></tr>
      <tr><th>Monthly Subscription</th><td>AED {subscription_fee}</td></tr>
      <tr><th>  Platform portion</th><td>AED {platform_fee}</td></tr>
      <tr><th>  Recovery portion</th><td>AED {recovery_fee}</td></tr>
      <tr><th>Mobilisation</th><td>AED {mobilisation_amount}</td></tr>
      <tr><th>Payment Cadence</th><td>{cadence}</td></tr>
      <tr><th>Edition</th><td>{edition}</td></tr>
      <tr><th>Kickoff Target</th><td>{kickoff_date}</td></tr>
      <tr><th>Signed at</th><td>{completed_timestamp}</td></tr>
    </table>

    <h3>Attached</h3>
    <ul>
      <li>{proposal_ref}_Signed.pdf — signed proposal</li>
      <li>{proposal_ref}_AuditCertificate.pdf — Zoho Sign audit certificate</li>
    </ul>

    <div class="alert">
      <p>INVOICE — ACTION REQUIRED</p>
      <p class="body">Mobilisation invoice drafted as DRAFT in Odoo.
      DO NOT POST until payment is confirmed.</p>
    </div>

    <h3>Odoo Record</h3>
    <p>Review at: <a href="{odoo_opportunity_url}">{odoo_opportunity_url}</a></p>
    <p>Invoice at: <a href="{odoo_invoice_url}">{odoo_invoice_url}</a></p>

    <p>Review the Odoo record and post the mobilisation invoice once payment
    is confirmed.</p>
  </div>
  <div class="footer">
    <p>Scholarix Global Consultants FZCO &middot; Maseed Building, Office 304,
    119/12 St, Al Rigga, Dubai, UAE &middot; Licence 45160</p>
    <p>&copy; 2026 Scholarix Global Consultants FZCO. All rights reserved.</p>
  </div>
</div>
</body>
</html>
```

---

## Notes

- **No marketing content** — internal operations notification only.
- Variables replaced by the webhook handler at send time.
- `{odoo_opportunity_url}` and `{odoo_invoice_url}` are the deep links to the
  Odoo record and invoice, respectively.
- The `[ACTION REQUIRED]` prefix in the subject line ensures the email surfaces
  clearly in the inbox.
