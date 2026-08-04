#!/usr/bin/env python3
"""Configuration loading for the signature webhook handler.

All secrets come from environment variables or a secret manager only.
Nothing secret is ever committed (G52).
"""
import os


class Config:
    """Read-only view of environment configuration with sane defaults."""

    def __init__(self, environ=None):
        env = environ if environ is not None else os.environ
        self.zoho_webhook_secret = env.get("ZOHO_SIGN_WEBHOOK_SECRET", "")
        self.zoho_client_id = env.get("ZOHO_SIGN_CLIENT_ID", "")
        self.zoho_client_secret = env.get("ZOHO_SIGN_CLIENT_SECRET", "")
        self.zoho_refresh_token = env.get("ZOHO_SIGN_REFRESH_TOKEN", "")
        self.zoho_account_id = env.get("ZOHO_SIGN_ACCOUNT_ID", "")
        self.zoho_base_url = env.get("ZOHO_SIGN_BASE_URL", "https://sign.zoho.com")
        # Odoo External API (JSON-RPC 2.0). ODOO_URL unset => stub mode.
        self.odoo_url = env.get("ODOO_URL", "")
        self.odoo_database = env.get("ODOO_DATABASE", "")
        self.odoo_api_key = env.get("ODOO_API_KEY", "")
        self.alert_email = env.get("ALERT_EMAIL", "sgc-admin@sgctech.ai")
        # SGC contact/signatory identity (for audit fields and notifications)
        self.sgc_signatory_name = env.get(
            "SGC_SIGNATORY_NAME",
            "Ali Asghar Teli Muhammad Iqbal Teli",
        )
        self.sgc_signatory_email = env.get(
            "SGC_SIGNATORY_EMAIL", "hello@sgctech.ai"
        )

    @property
    def odoo_stub_mode(self):
        """True when no Odoo instance is configured — run fully offline."""
        return not (self.odoo_url and self.odoo_database and self.odoo_api_key)

    def validate(self):
        """Return a list of missing required config items (empty = ok)."""
        problems = []
        if not self.zoho_webhook_secret:
            problems.append("ZOHO_SIGN_WEBHOOK_SECRET is required")
        return problems
