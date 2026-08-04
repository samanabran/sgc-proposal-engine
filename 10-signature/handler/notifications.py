#!/usr/bin/env python3
"""Notification dispatcher — SMTP sends using the brand templates in
10-signature/notification-templates/.

Templates: 01-client-completion.md, 02-sgc-signatory-completion.md,
03-sdr-completion.md. Variables like {proposal_ref} are substituted by the
handler before dispatch. In stub mode (no SMTP config) sends are recorded
in-memory so the offline self-test can assert notification_sent=True.
"""
import os
import re
import smtplib
from email.message import EmailMessage

TEMPLATES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "notification-templates",
)

# Canonical template filenames per recipient (webhook-spec.md §notifications)
TEMPLATE_CLIENT = "01-client-completion.md"
TEMPLATE_SGC_SIGNATORY = "02-sgc-signatory-completion.md"
TEMPLATE_SDR = "03-sdr-completion.md"


class Notifier:
    def __init__(self, templates_dir=TEMPLATES_DIR, smtp_host="",
                 smtp_port=587, smtp_user="", smtp_password="", smtp_from=""):
        self.templates_dir = templates_dir
        self.smtp_host = smtp_host
        self.smtp_port = int(smtp_port or 587)
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.smtp_from = smtp_from or "SGC TECH AI <hello@sgctech.ai>"
        self.stub = not smtp_host
        self.sent = []  # stub record: {"to", "template", "subject", "body"}

    # -- template rendering -------------------------------------------------

    def _load(self, template_name):
        import os
        path = os.path.join(self.templates_dir, template_name)
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()

    def render(self, template_name, variables):
        """Return (subject, body) with {var} placeholders substituted.

        Templates carry a YAML-ish front block with `Subject:` on its own
        line; the remainder is the email body. Unknown placeholders are
        left as-is so a missing variable is visible rather than silently
        dropped.
        """
        raw = self._load(template_name)
        subject = ""
        body = raw
        m = re.search(r"^Subject:\s*(.+)$", raw, re.MULTILINE)
        if m:
            subject = m.group(1).strip()
            body = raw[m.end():].lstrip("\n")
        for key, value in (variables or {}).items():
            subject = subject.replace("{" + key + "}", str(value))
            body = body.replace("{" + key + "}", str(value))
        return subject, body

    # -- send ---------------------------------------------------------------

    def send(self, template_name, to, variables=None):
        subject, body = self.render(template_name, variables)
        self.sent.append({"to": to, "template": template_name,
                          "subject": subject, "body": body})
        if self.stub:
            return True
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.smtp_from
        msg["To"] = to
        msg.set_content(body)
        with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=30) as smtp:
            if self.smtp_user:
                smtp.starttls()
                smtp.login(self.smtp_user, self.smtp_password)
            smtp.send_message(msg)
        return True
