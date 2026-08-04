# Notification Template 3 — To SDR on Completion

Sent to the SDR owner when the envelope reaches `completed` status.
Includes delivery handover checklist prompt.
Plain text and HTML versions.

Brand tokens used: `IBM Plex Sans`, `#0F213D` (navy), `#B79554` (gold),
`#F7F4EE` (ivory), `SGC TECH AI`, `Scholarix Global Consultants FZCO`.

---

## Plain text

```
Subject: {proposal_ref} — Deal Won. Delivery Handover Checklist.

{sdr_name},

{client_legal_name} has signed {proposal_ref}. The deal is Won.
Delivery handover is now due.

DEAL SUMMARY

  Client:           {client_legal_name}
  Opportunity:      {proposal_ref}
  Monthly Sub:     AED {subscription_fee}/month
  Platform:        AED {platform_fee}/month
  Recovery:        AED {recovery_fee}/month
  Mobilisation:    AED {mobilisation_amount} (drafted — confirm before posting)
  Term:            {contract_term_months} months
  Cadence:         {cadence}
  Edition:         {edition}
  Signed at:       {completed_timestamp}
  Kickoff Target:  {kickoff_date}

DELIVERY HANDOVER CHECKLIST

Complete the following in the delivery handover system:

  □ Notify delivery manager with this deal summary
  □ Confirm mobilisation invoice is drafted and payment is being tracked
  □ Schedule kickoff call with client (target: {kickoff_date})
  □ Confirm Odoo access credentials sent to client
  □ Confirm onboarding materials sent to client
  □ Set up project folder in delivery system
  □ Assign delivery team and confirm capacity
  □ Add client contacts to delivery Slack channel / communication plan
  □ Confirm MSA and Order Form are filed in the contract archive
  □ Add deal to monthly revenue forecast

ODOO RECORD

  {odoo_opportunity_url}

Signed documents are in the opportunity attachments.
Audit certificate is attached to the opportunity.

Questions? Contact hello@sgctech.ai.

SGC TECH AI
Scholarix Global Consultants FZCO
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
        color: #0F213D; margin: 0 0 4px; }
  .subtitle { color: #5F6775; font-size: 14px; margin: 0 0 24px; }
  h3 { font-size: 13px; font-weight: 600; color: #B79554; margin: 24px 0 8px;
        text-transform: uppercase; letter-spacing: 0.05em; }
  p { line-height: 1.75; margin: 0 0 12px; }
  table { width: 100%; border-collapse: collapse; margin: 16px 0;
           font-size: 14px; }
  th { text-align: left; padding: 8px 12px; background: #F7F4EE;
        border-bottom: 1px solid #D9C08A; color: #0F213D; font-weight: 600; }
  td { padding: 8px 12px; border-bottom: 1px solid #ECE7DF; }
  td:last-child { text-align: right; font-variant-numeric: tabular-nums; }
  .checklist { background: #F7F4EE; padding: 20px 24px; margin: 16px 0; }
  .checklist li { margin-bottom: 8px; line-height: 1.5; }
  .won-banner { background: #2C6654; color: #ffffff; padding: 16px 24px;
                 margin: 24px 0; }
  .won-banner p { margin: 0; font-weight: 700; font-size: 16px; }
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
    <h2>{proposal_ref} — Deal Won</h2>
    <p class="subtitle">Delivery Handover Checklist. Action required by {sdr_name}.</p>

    <div class="won-banner">
      <p>&#10003; DEAL WON — {client_legal_name}</p>
    </div>

    <h3>Deal Summary</h3>
    <table>
      <tr><th>Client</th><td>{client_legal_name}</td></tr>
      <tr><th>Opportunity</th><td>{proposal_ref}</td></tr>
      <tr><th>Monthly Subscription</th><td>AED {subscription_fee}/month</td></tr>
      <tr><th>  Platform portion</th><td>AED {platform_fee}/month</td></tr>
      <tr><th>  Recovery portion</th><td>AED {recovery_fee}/month</td></tr>
      <tr><th>Mobilisation</th><td>AED {mobilisation_amount} (drafted — do not post yet)</td></tr>
      <tr><th>Term</th><td>{contract_term_months} months</td></tr>
      <tr><th>Cadence</th><td>{cadence}</td></tr>
      <tr><th>Edition</th><td>{edition}</td></tr>
      <tr><th>Kickoff Target</th><td>{kickoff_date}</td></tr>
      <tr><th>Signed at</th><td>{completed_timestamp}</td></tr>
    </table>

    <h3>Delivery Handover Checklist</h3>
    <div class="checklist">
      <ul style="padding-left:20px;margin:0">
        <li>&#9634; Notify delivery manager with this deal summary</li>
        <li>&#9634; Confirm mobilisation invoice is drafted; track payment confirmation before posting</li>
        <li>&#9634; Schedule kickoff call with client (target: {kickoff_date})</li>
        <li>&#9634; Confirm Odoo access credentials sent to client</li>
        <li>&#9634; Confirm onboarding materials sent to client</li>
        <li>&#9634; Set up project folder in delivery system</li>
        <li>&#9634; Assign delivery team and confirm capacity</li>
        <li>&#9634; Add client contacts to delivery communication plan</li>
        <li>&#9634; Confirm MSA and Order Form filed in contract archive</li>
        <li>&#9634; Add deal to monthly revenue forecast</li>
      </ul>
    </div>

    <h3>Odoo Record</h3>
    <p><a href="{odoo_opportunity_url}">{odoo_opportunity_url}</a></p>
    <p>Signed documents and audit certificate are attached to the opportunity.</p>

    <p>Questions? Contact <a href="mailto:hello@sgctech.ai">hello@sgctech.ai</a>.</p>
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
- The `[ACTION REQUIRED]` or delivery checklist format ensures the SDR knows
  exactly what to do next.
- `{sdr_name}` and `{sdr_email}` are resolved from the opportunity owner field in Odoo.
- The mobilisation amount warning "(drafted — do not post yet)" reinforces G51:
  the invoice is created as draft and a human must confirm payment before it is posted.
