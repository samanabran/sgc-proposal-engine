#!/usr/bin/env python3
"""Zoho Sign API client (OAuth refresh + signed document download).

Used on `completed` to fetch the signed PDF and audit certificate so their
SHA-256 hashes can be verified against the frozen original before any Odoo
write-back (webhook-spec.md §Hash verification).
"""
import base64
import hashlib
import json
import time
import urllib.parse
import urllib.request


class ZohoAuthError(Exception):
    pass


class TokenManager:
    """Short-lived access token holder; refresh token stored in env only.

    Access tokens are memory-only — never written to disk or logged.
    """

    def __init__(self, client_id, client_secret, refresh_token, base_url,
                 token_url="https://accounts.zoho.com/oauth/v2/token"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.base_url = base_url.rstrip("/")
        self.token_url = token_url
        self._access_token = None
        self._expires_at = 0

    def access_token(self):
        if self._access_token and time.time() < self._expires_at - 60:
            return self._access_token
        data = urllib.parse.urlencode({
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
        }).encode("utf-8")
        req = urllib.request.Request(
            self.token_url, data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        token = body.get("access_token")
        if not token:
            raise ZohoAuthError(
                "Token refresh failed: {}".format(body.get("error", "no token"))
            )
        self._access_token = token
        self._expires_at = time.time() + int(body.get("expires_in", 3600))
        return self._access_token

    def _api(self, path):
        req = urllib.request.Request(
            self.base_url + path,
            headers={"Authorization": "Zoho-oauthtoken " + self.access_token()},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read()

    def download_document(self, envelope_id, document_id):
        """Download one document's bytes from a completed envelope."""
        return self._api(
            "/api/v1/envelope/{}/download?file_id={}".format(
                envelope_id, document_id
            )
        )

    def download_audit_trail(self, envelope_id):
        return self._api("/api/v1/envelope/{}/audit_trail".format(envelope_id))


def sha256_base64(data):
    return base64.b64encode(hashlib.sha256(data).digest()).decode("ascii")


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()
