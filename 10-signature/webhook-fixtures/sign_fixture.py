#!/usr/bin/env python3
"""Sign a Zoho Sign webhook fixture with the correct HMAC headers.

Computes X-ZS-WEBHOOK-TIMESTAMP and X-ZS-WEBHOOK-SIGNATURE for a payload
file, per 10-signature/webhook-spec.md:

    signature = HMAC-SHA256(raw_body, key=ZOHO_SIGN_WEBHOOK_SECRET) base64

Usage:
    python sign_fixture.py completed_by_all.json --secret whsec_test_0000
"""

import argparse
import base64
import hashlib
import hmac
import json
import sys
import time
from pathlib import Path


def sign(payload_bytes: bytes, secret: str, timestamp: int | None = None) -> dict:
    ts = timestamp if timestamp is not None else int(time.time())
    digest = hmac.new(secret.encode("utf-8"), payload_bytes, hashlib.sha256).digest()
    signature = base64.b64encode(digest).decode("ascii")
    return {
        "X-ZS-WEBHOOK-TIMESTAMP": ts,
        "X-ZS-WEBHOOK-SIGNATURE": signature,
        "body_sha256": hashlib.sha256(payload_bytes).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path, help="Path to a webhook fixture JSON")
    parser.add_argument("--secret", default="whsec_test_0000", help="Webhook secret")
    parser.add_argument("--timestamp", type=int, default=None, help="Override timestamp")
    parser.add_argument(
        "--stale",
        action="store_true",
        help="Emit a timestamp older than 300s (tests skew rejection)",
    )
    args = parser.parse_args()

    payload = args.fixture.read_bytes()
    try:
        json.loads(payload)
    except json.JSONDecodeError as exc:
        print(f"Fixture is not valid JSON: {exc}", file=sys.stderr)
        return 1

    ts = args.timestamp
    if args.stale and ts is None:
        ts = int(time.time()) - 3600  # 1 hour stale

    result = sign(payload, args.secret, ts)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
