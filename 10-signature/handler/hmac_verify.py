#!/usr/bin/env python3
"""HMAC verification for Zoho Sign webhooks (webhook-spec.md §Security).

Headers verified:
  X-ZS-WEBHOOK-TIMESTAMP  — Unix seconds; rejected if |now - ts| > 300
  X-ZS-WEBHOOK-SIGNATURE  — base64(HMAC-SHA256(raw_body, secret))
"""
import base64
import hashlib
import hmac
import time


MAX_SKEW_SECONDS = 300
MS_TIMESTAMP_THRESHOLD = 10 ** 12  # any real seconds-epoch value stays below this until year 33658


class VerificationFailure(Exception):
    """Raised when a webhook request fails HMAC verification."""


def verify_timestamp(header_timestamp, now=None):
    """Reject if the request timestamp is older than MAX_SKEW_SECONDS.

    The header timestamp is authoritative (not event_time in the payload).
    Returns the parsed timestamp. Raises VerificationFailure on skew.
    """
    if now is None:
        now = time.time()
    try:
        ts = int(header_timestamp)
    except (TypeError, ValueError):
        raise VerificationFailure(
            "Timestamp missing or unparseable: {!r}".format(header_timestamp)
        )
    if ts > MS_TIMESTAMP_THRESHOLD:
        ts //= 1000  # Zoho Sign sends X-ZS-WEBHOOK-TIMESTAMP in milliseconds
    diff = abs(now - ts)
    if diff > MAX_SKEW_SECONDS:
        raise VerificationFailure(
            "Timestamp skew rejected: zs_timestamp={ts}, server_time={now}, "
            "diff={diff}s".format(ts=ts, now=int(now), diff=int(diff))
        )
    return ts


def verify_signature(raw_body, header_signature, secret):
    """Constant-time compare of base64(HMAC-SHA256(raw_body, secret)).

    Raises VerificationFailure on mismatch.
    """
    if not secret:
        raise VerificationFailure("Webhook secret not configured")
    expected = hmac.new(
        secret.encode("utf-8"), raw_body, hashlib.sha256
    ).digest()
    try:
        provided = base64.b64decode(header_signature)
    except (TypeError, ValueError):
        raise VerificationFailure("Signature header not valid base64")
    if not hmac.compare_digest(expected, provided):
        raise VerificationFailure("HMAC mismatch — potential spoofing")


def verify_request(headers, raw_body, secret, now=None):
    """Full verification entry point.

    headers: dict-like with lowercase keys (e.g. a WSGI environ or
             http.server headers). Returns the raw timestamp when valid.
    """
    ts_header = _header(headers, "X-ZS-WEBHOOK-TIMESTAMP")
    sig_header = _header(headers, "X-ZS-WEBHOOK-SIGNATURE")
    ts = verify_timestamp(ts_header, now=now)
    verify_signature(raw_body, sig_header, secret)
    return ts


def _header(headers, name):
    """Fetch a header case-insensitively from dict/Message/WSGI environ."""
    low = name.lower()
    # WSGI: environ has HTTP_ prefixed uppercase keys
    if "HTTP_" + name.upper().replace("-", "_") in headers:
        return headers["HTTP_" + name.upper().replace("-", "_")]
    for key, value in headers.items():
        if str(key).lower() == low:
            return value
    return None


def body_sha256(raw_body):
    """SHA-256 hex digest of the raw payload (for audit forensics)."""
    return hashlib.sha256(raw_body).hexdigest()
