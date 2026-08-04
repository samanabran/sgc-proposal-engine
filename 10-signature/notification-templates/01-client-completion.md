# Notification Template 1 — To Client on Completion

Sent when both parties have signed (envelope `completed` event).
Plain text and HTML versions.

Brand tokens used: `IBM Plex Sans`, `#0F213D` (navy), `#B79554` (gold),
`#F7F4EE` (ivory), `SGC TECH AI`, `Scholarix Global Consultants FZCO`.

---

## Plain text

```
Subject: Your SGC TECH AI Proposal — Signed and Ready

Dear {client_signatory_name},

Thank you for signing {proposal_ref}. The agreement has been fully executed
by both parties and is now legally binding.

Please find attached:
  - Your signed copy of {proposal_ref}
  - Audit certificate issued by Zoho Sign

WHAT HAPPENS NEXT

1. Mobilisation
   Your mobilisation invoice (AED {mobilisation_amount}) will be issued
   separately by SGC TECH AI. Please expect it within 3 business days
   of today's date.

2. Kickoff
   Our team will be in touch to schedule your kickoff session. The target
   start date is {kickoff_date}. Your dedicated implementation consultant
   will be in contact within 5 business days to confirm the agenda.

3. Access and Onboarding
   Once the mobilisation payment is confirmed, you will receive your
   Odoo access credentials and onboarding materials.

QUESTIONS

For any questions about your proposal or the agreement, contact us at
hello@sgctech.ai or call +971 52 198 5231.

We look forward to working with you.

Regards,

Ali Asghar Teli Muhammad Iqbal Teli
Company Manager
Scholarix Global Consultants FZCO
Trading as SGC TECH AI
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
  .header p { margin: 4px 0 0; color: #B79554; font-size: 13px;
              letter-spacing: 0.05em; }
  .content { padding: 32px 40px; }
  h2 { font-family: 'IBM Plex Serif', Georgia, serif; font-size: 18px;
        color: #0F213D; margin: 0 0 16px; }
  h3 { font-size: 14px; font-weight: 600; color: #B79554; margin: 24px 0 8px;
        text-transform: uppercase; letter-spacing: 0.05em; }
  p { line-height: 1.75; margin: 0 0 12px; }
  ul { margin: 0 0 16px; padding-left: 20px; }
  li { margin-bottom: 8px; }
  .next-steps { background: #F7F4EE; border-left: 4px solid #B79554;
                padding: 16px 20px; margin: 24px 0; }
  .next-steps p { margin: 0; font-size: 14px; }
  .footer { background: #0F213D; color: #D9C08A; padding: 24px 40px;
             font-size: 12px; }
  .footer p { margin: 0; }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>SGC TECH AI</h1>
    <p>FINANCE &middot; SYSTEM &middot; TECHNOLOGY</p>
  </div>
  <div class="content">
    <h2>Your Proposal — Signed and Executed</h2>
    <p>Dear {client_signatory_name},</p>
    <p>Thank you for signing <strong>{proposal_ref}</strong>. The agreement
    has been fully executed by both parties and is now legally binding.</p>

    <div class="next-steps">
      <p><strong>Attached:</strong> Signed proposal and Zoho Sign audit
      certificate</p>
    </div>

    <h3>What Happens Next</h3>
    <ol>
      <li><strong>Mobilisation</strong><br>
          Your mobilisation invoice (AED {mobilisation_amount}) will be issued
          by SGC TECH AI within 3 business days.</li>
      <li><strong>Kickoff</strong><br>
          Target start: {kickoff_date}. Your implementation consultant will
          contact you within 5 business days to confirm the agenda.</li>
      <li><strong>Access and Onboarding</strong><br>
          Upon mobilisation payment confirmation, you will receive your Odoo
          access credentials and onboarding materials.</li>
    </ol>

    <h3>Questions?</h3>
    <p>Contact us at <a href="mailto:hello@sgctech.ai"
    style="color:#0F213D">hello@sgctech.ai</a> or call +971 52 198 5231.</p>
    <p>We look forward to working with you.</p>

    <p>Regards,<br>
    <strong>Ali Asghar Teli Muhammad Iqbal Teli</strong><br>
    Company Manager<br>
    Scholarix Global Consultants FZCO<br>
    Trading as SGC TECH AI</p>
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

- **No marketing content** — no product pitches, no promotional links.
- `proposal_ref`, `client_signatory_name`, `mobilisation_amount`, `kickoff_date`
  are template variables replaced by the webhook handler at send time.
- `{mobilisation_amount}` is formatted as a number with commas (e.g. 4,900).
- `{kickoff_date}` is the target date from the Order Form, formatted DD MMM YYYY.
