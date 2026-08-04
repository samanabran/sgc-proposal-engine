#!/usr/bin/env python3
"""Signature webhook handler — entry point.

Reference implementation of the separate webhook handler service specified in
10-signature/webhook-spec.md. Pure-stdlib Python 3.9+.

Usage:
    python handler.py serve [--host HOST] [--port PORT] [--insecure-no-hmac]
    python handler.py selftest <fixtures_dir> [--secret whsec_test_0000]

Env vars honoured by serve:
    HOST (default 0.0.0.0)  PORT (default 8080)
    ZOHO_SIGN_WEBHOOK_SECRET (required unless --insecure-no-hmac)
    ZOHO_SIGN_CLIENT_ID / CLIENT_SECRET / REFRESH_TOKEN / ACCOUNT_ID / BASE_URL
    ODOO_URL / ODOO_DATABASE / ODOO_API_KEY (all three unset = stub mode)
    STORE_PATH (default /data/store.db on Railway, store.db locally)
    ALERT_EMAIL (default sgc-admin@sgctech.ai)

Serve:
    GET  /healthz                 -> 200 ok
    POST /webhooks/signature/zoho_sign/
    400 bad JSON | 401 HMAC fail/stale | 200 accepted (+ duplicate->200) | 500

Selftest:
    Replays every fixture through HMAC verify -> idempotency -> dispatch with
    the Odoo client in stub mode; prints a PASS/FAIL table. Exit 0 = all pass.

Exit codes: 0 = clean, 1 = selftest failure, 2 = usage error (matches the
validate.py convention in 05-ops/).
"""
import base64
import hashlib
import hmac
import json
import logging
import os
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config                     # noqa: E402
from events import EventDispatcher            # noqa: E402
from hmac_verify import (VerificationFailure, verify_request)  # noqa: E402
from notifications import Notifier            # noqa: E402
from odoo_client import OdooClient            # noqa: E402
from store import Store                       # noqa: E402
from zoho_client import TokenManager          # noqa: E402

log = logging.getLogger("handler")


class SignatureWebhookHandler(BaseHTTPRequestHandler):
    """Serves POST /webhooks/signature/zoho_sign/ per webhook-spec.md."""

    dispatcher = None    # set by serve()
    insecure = False     # --insecure-no-hmac (offline dev only)

    def do_GET(self):
        if self.path.rstrip("/") == "/healthz":
            self._respond(200, "ok")
            return
        self.send_error(404, "Not found")

    def do_POST(self):
        if self.path.rstrip("/") != "/webhooks/signature/zoho_sign":
            self.send_error(404, "Not found")
            return

        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length)
        actor_ip = self.client_address[0]

        # 1. HMAC verification (unless explicitly disabled for offline dev)
        if not self.insecure:
            try:
                verify_request(self.headers, raw,
                               self.dispatcher.config.zoho_webhook_secret)
            except VerificationFailure as exc:
                log.warning("HMAC mismatch — potential spoofing from %s: %s",
                            actor_ip, exc)
                self._respond(401, "HMAC verification failed")
                return

        # 2. Parse JSON (400 on invalid)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            self._respond(400, "Invalid JSON body")
            return

        event = payload.get("event") or {}
        envelope_id = event.get("request_id") or event.get("envelope_id") or ""
        event_id = event.get("event_id") or ""
        event_type = event.get("event_type") or ""
        body_hash = hashlib.sha256(raw).hexdigest()

        if not envelope_id or not event_id:
            self._respond(400, "Missing envelope_id/event_id")
            return

        # 3. Idempotency — respond 200 immediately, before async work
        store = self.dispatcher.store
        if store.is_duplicate(envelope_id, event_id):
            log.info("Duplicate event ignored: %s/%s", envelope_id, event_id)
            self._respond(200, "Duplicate event ignored")
            return

        # 4. Acknowledge the provider, then process async (never block >500ms)
        self._respond(200, "accepted")
        thread = threading.Thread(
            target=self._process_async,
            args=(payload, raw, actor_ip, body_hash),
            daemon=True,
        )
        thread.start()

    def _process_async(self, payload, raw, actor_ip, body_hash):
        event = payload.get("event") or {}
        envelope_id = event.get("request_id") or event.get("envelope_id") or ""
        event_id = event.get("event_id") or ""
        event_type = event.get("event_type") or ""
        store = self.dispatcher.store
        try:
            status, details = self.dispatcher.dispatch(event)
            store.record_event(envelope_id, event_id, event_type,
                               odoo_write=True, notification_sent=True)
            store.audit(
                envelope_id, event_type, event_id,
                event_timestamp=event.get("event_time"),
                actor="system", actor_email="",
                actor_ip=actor_ip, raw_payload_hash=body_hash,
                odoo_write=True, odoo_write_details=details,
                notification_sent=True,
            )
            log.info("Processed %s/%s -> %s", envelope_id, event_id, status)
        except Exception as exc:  # noqa: BLE001 — async path must not die
            log.error("Failed %s/%s: %s", envelope_id, event_id, exc)
            store.dead_letter(envelope_id, event_id, event_type,
                              payload, str(exc))
            store.audit(envelope_id, event_type, event_id,
                        actor_ip=actor_ip, raw_payload_hash=body_hash,
                        error_message=str(exc))

    def _respond(self, code, message):
        body = json.dumps({"status": message}).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        log.info("%s - %s", self.address_string(), fmt % args)


# ---------------------------------------------------------------------------
# Offline self-test: replay fixtures through the full pipeline
# ---------------------------------------------------------------------------

def _sign(raw, secret, timestamp=None):
    ts = int(timestamp if timestamp is not None else time.time())
    sig = base64.b64encode(
        hmac.new(secret.encode("utf-8"), raw, hashlib.sha256).digest()
    ).decode("ascii")
    return ts, sig


def _selftest(fixtures_dir, secret):
    store = Store(":memory:")
    config = Config({**os.environ, "ZOHO_SIGN_WEBHOOK_SECRET": secret})
    odoo = OdooClient("", "", "")          # stub mode
    notifier = Notifier()
    dispatcher = EventDispatcher(config, store, odoo, notifier=notifier,
                                 zoho=None)

    fixtures = sorted(
        f for f in os.listdir(fixtures_dir) if f.endswith(".json"))
    if not fixtures:
        print("No fixtures found in {}".format(fixtures_dir))
        return 2

    results = []
    for name in fixtures:
        with open(os.path.join(fixtures_dir, name), "rb") as fh:
            raw = fh.read()
        ts, sig = _sign(raw, secret)
        try:
            verify_request(
                {"X-ZS-WEBHOOK-TIMESTAMP": str(ts),
                 "X-ZS-WEBHOOK-SIGNATURE": sig},
                raw, secret)
            payload = json.loads(raw.decode("utf-8"))
            status, _ = dispatcher.dispatch(payload.get("event") or {})
            event = payload.get("event") or {}
            store.record_event(
                event.get("request_id") or event.get("envelope_id") or "",
                event.get("event_id") or "",
                event.get("event_type") or "",
                odoo_write=True, notification_sent=True)
            results.append((name, "PASS", status))
        except Exception as exc:  # noqa: BLE001
            results.append((name, "FAIL", str(exc)))

    # Duplicate-idempotency check: replay the first fixture once more.
    if fixtures:
        name = fixtures[0]
        with open(os.path.join(fixtures_dir, name), "rb") as fh:
            raw = fh.read()
        payload = json.loads(raw.decode("utf-8"))
        event = payload.get("event") or {}
        envelope_id = event.get("request_id") or event.get("envelope_id")
        event_id = event.get("event_id")
        dup = store.is_duplicate(envelope_id, event_id)
        results.append(("idempotency({})".format(name),
                        "PASS" if dup else "FAIL", "duplicate detected"))

    print("{:<38} {:>6}  {}".format("fixture", "RESULT", "detail"))
    print("-" * 72)
    ok = True
    for name, result, detail in results:
        print("{:<38} {:>6}  {}".format(name, result, detail))
        if result != "PASS":
            ok = False
    print("-" * 72)
    print("{} passed, {} failed".format(
        sum(1 for r in results if r[1] == "PASS"),
        sum(1 for r in results if r[1] != "PASS")))
    return 0 if ok else 1


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")

    if not argv:
        print(__doc__)
        return 2

    cmd = argv[0]
    if cmd == "selftest":
        if len(argv) < 2:
            print("usage: handler.py selftest <fixtures_dir> [--secret S]")
            return 2
        fixtures_dir = argv[1]
        secret = "whsec_test_0000"
        if "--secret" in argv:
            secret = argv[argv.index("--secret") + 1]
        return _selftest(fixtures_dir, secret)

    if cmd == "serve":
        host = os.environ.get("HOST", "0.0.0.0")
        port = int(os.environ.get("PORT", "8080"))
        insecure = False
        i = 1
        while i < len(argv):
            if argv[i] == "--host" and i + 1 < len(argv):
                host = argv[i + 1]
                i += 2
            elif argv[i] == "--port" and i + 1 < len(argv):
                port = int(argv[i + 1])
                i += 2
            elif argv[i] == "--insecure-no-hmac":
                insecure = True
                i += 1
            else:
                print("Unknown argument: {}".format(argv[i]))
                return 2
        return _serve(host, port, insecure)

    print(__doc__)
    return 2


def _serve(host, port, insecure=False):
    config = Config()
    problems = config.validate()
    if problems and not insecure:
        for p in problems:
            print("config error: {}".format(p))
        return 2

    db_path = os.environ.get("STORE_PATH")
    if not db_path:
        if os.path.isdir("/data"):
            db_path = "/data/store.db"
        else:
            db_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "store.db")
    log.info("Store path: %s", db_path)
    store = Store(db_path)
    odoo = OdooClient(config.odoo_url, config.odoo_database,
                      config.odoo_api_key)
    notifier = Notifier()
    zoho = None
    if config.zoho_client_id and config.zoho_client_secret \
            and config.zoho_refresh_token:
        zoho = TokenManager(config.zoho_client_id, config.zoho_client_secret,
                            config.zoho_refresh_token, config.zoho_base_url)
    dispatcher = EventDispatcher(config, store, odoo, notifier=notifier,
                                 zoho=zoho)

    SignatureWebhookHandler.dispatcher = dispatcher
    SignatureWebhookHandler.insecure = insecure

    server = ThreadingHTTPServer((host, port), SignatureWebhookHandler)
    log.info("Signature webhook listening on http://%s:%s%s", host, port,
             "/webhooks/signature/zoho_sign/")
    if insecure:
        log.warning("HMAC verification DISABLED (--insecure-no-hmac) — "
                    "offline development only")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log.info("shutting down")
        server.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
