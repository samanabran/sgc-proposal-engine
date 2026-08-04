#!/usr/bin/env python3
"""Idempotency + audit + dead-letter store.

Reference implementation uses SQLite so the handler runs anywhere with the
standard library. Production swaps to PostgreSQL using the identical schema
in 10-signature/webhook-db-schema.sql (UNIQUE(envelope_id, event_id) is the
idempotency contract — the table layout mirrors it exactly).

Append-only semantics: no UPDATE/DELETE on audit/event rows.
"""
import json
import sqlite3
import time


SCHEMA = """
CREATE TABLE IF NOT EXISTS signature_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    envelope_id TEXT NOT NULL,
    event_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    processed_at TEXT NOT NULL,
    odoo_write_performed INTEGER DEFAULT 0,
    notification_sent INTEGER DEFAULT 0,
    UNIQUE(envelope_id, event_id)
);
CREATE TABLE IF NOT EXISTS signature_audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    logged_at TEXT NOT NULL,
    envelope_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_id TEXT NOT NULL,
    event_timestamp TEXT,
    actor TEXT,
    actor_email TEXT,
    actor_ip TEXT,
    provider TEXT DEFAULT 'zoho_sign',
    raw_payload_hash TEXT,
    odoo_opportunity_id INTEGER,
    odoo_write_performed INTEGER,
    odoo_write_details TEXT,
    notification_sent INTEGER,
    error_message TEXT,
    UNIQUE(envelope_id, event_id)
);
CREATE TABLE IF NOT EXISTS signature_dead_letter (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    envelope_id TEXT NOT NULL,
    event_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload TEXT NOT NULL,
    retries INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TEXT NOT NULL,
    reviewed INTEGER DEFAULT 0,
    reviewed_by TEXT
);
"""


def _iso(ts=None):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ts or time.time()))


class Store:
    def __init__(self, db_path=":memory:"):
        self._conn = sqlite3.connect(db_path)
        self._conn.executescript(SCHEMA)
        self._conn.commit()

    def close(self):
        self._conn.close()

    def is_duplicate(self, envelope_id, event_id):
        row = self._conn.execute(
            "SELECT 1 FROM signature_events WHERE envelope_id=? AND event_id=?",
            (envelope_id, event_id),
        ).fetchone()
        return row is not None

    def record_event(self, envelope_id, event_id, event_type,
                     odoo_write=False, notification_sent=False):
        """Insert idempotency row; returns True if inserted, False if dup."""
        try:
            self._conn.execute(
                "INSERT INTO signature_events "
                "(envelope_id, event_id, event_type, processed_at, "
                " odoo_write_performed, notification_sent) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (envelope_id, event_id, event_type, _iso(),
                 1 if odoo_write else 0, 1 if notification_sent else 0),
            )
            self._conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def audit(self, envelope_id, event_type, event_id, event_timestamp=None,
              actor=None, actor_email=None, actor_ip=None,
              raw_payload_hash=None, odoo_opportunity_id=None,
              odoo_write=False, odoo_write_details=None,
              notification_sent=False, error_message=None):
        self._conn.execute(
            "INSERT INTO signature_audit_log "
            "(logged_at, envelope_id, event_type, event_id, event_timestamp, "
            " actor, actor_email, actor_ip, raw_payload_hash, "
            " odoo_opportunity_id, odoo_write_performed, odoo_write_details, "
            " notification_sent, error_message) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (_iso(), envelope_id, event_type, event_id, event_timestamp,
             actor, actor_email, actor_ip, raw_payload_hash,
             odoo_opportunity_id, 1 if odoo_write else 0,
             json.dumps(odoo_write_details) if odoo_write_details else None,
             1 if notification_sent else 0, error_message),
        )
        self._conn.commit()

    def dead_letter(self, envelope_id, event_id, event_type, payload,
                    error_message, retries=0):
        self._conn.execute(
            "INSERT INTO signature_dead_letter "
            "(envelope_id, event_id, event_type, payload, retries, "
            " error_message, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (envelope_id, event_id, event_type,
             json.dumps(payload) if not isinstance(payload, str) else payload,
             retries, error_message, _iso()),
        )
        self._conn.commit()
