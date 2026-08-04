-- ============================================================================
-- Signature pipeline database schema (PostgreSQL)
-- Source of truth: 10-signature/webhook-spec.md (idempotency + audit log)
-- and 10-signature/audit-retention.md (retention policy).
--
-- This schema is consumed by the SEPARATE webhook handler service (see
-- webhook-spec.md). It is tracked here so the contract between spec and
-- implementation cannot drift.
-- ============================================================================

BEGIN;

-- ----------------------------------------------------------------------------
-- Idempotency table — one row per processed event; UNIQUE(envelope_id, event_id)
-- is the idempotency key. Append-only: no UPDATE, no DELETE.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS signature_events (
    id                   BIGSERIAL PRIMARY KEY,
    envelope_id          TEXT        NOT NULL,
    event_id             TEXT        NOT NULL,          -- provider's event ID
    event_type           TEXT        NOT NULL,          -- sent|viewed|signed_by_a_recipient|completed_by_all|declined|expires|recalled|hard_bounced|reassigned
    processed_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    odoo_write_performed BOOLEAN     NOT NULL DEFAULT FALSE,
    notification_sent    BOOLEAN     NOT NULL DEFAULT FALSE,
    CONSTRAINT uq_signature_events_envelope_event UNIQUE (envelope_id, event_id)
);

-- ----------------------------------------------------------------------------
-- Audit log — every event, append-only. No UPDATE, no DELETE.
-- Raw payload hash retained for forensics; retention per audit-retention.md
-- (10 years for contract records).
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS signature_audit_log (
    id                   BIGSERIAL PRIMARY KEY,
    logged_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    envelope_id          TEXT        NOT NULL,
    event_type           TEXT        NOT NULL,
    event_id             TEXT        NOT NULL,           -- provider's event UUID
    event_timestamp      TIMESTAMPTZ,                    -- from provider payload
    actor                TEXT,                           -- e.g. "client" | "sgc" | "system"
    actor_email          TEXT,
    actor_ip             TEXT,
    provider             TEXT        NOT NULL DEFAULT 'zoho_sign',
    raw_payload_hash     TEXT,                           -- SHA256 of raw JSON body
    odoo_opportunity_id  INTEGER,
    odoo_write_performed BOOLEAN     NOT NULL DEFAULT FALSE,
    odoo_write_details   TEXT,                           -- JSON summary of fields written
    notification_sent    BOOLEAN     NOT NULL DEFAULT FALSE,
    error_message        TEXT,
    CONSTRAINT uq_signature_audit_log_envelope_event UNIQUE (envelope_id, event_id)
);

-- ----------------------------------------------------------------------------
-- Dead-letter queue — async processing failures after max retries.
-- An envelope is never auto-reprocessed; a human reviews and manually triggers.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS signature_dead_letter (
    id            BIGSERIAL PRIMARY KEY,
    envelope_id   TEXT        NOT NULL,
    event_id      TEXT        NOT NULL,
    event_type    TEXT        NOT NULL,
    payload       JSONB       NOT NULL,                  -- full event payload
    retries       INTEGER     NOT NULL DEFAULT 0,
    error_message TEXT,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    reviewed      BOOLEAN     NOT NULL DEFAULT FALSE,    -- set when human reviews
    reviewed_by   TEXT
);

-- ----------------------------------------------------------------------------
-- Indexes
-- ----------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_signature_events_processed_at
    ON signature_events (processed_at);

CREATE INDEX IF NOT EXISTS idx_signature_audit_log_envelope_id
    ON signature_audit_log (envelope_id);

CREATE INDEX IF NOT EXISTS idx_signature_audit_log_logged_at
    ON signature_audit_log (logged_at);

CREATE INDEX IF NOT EXISTS idx_signature_dead_letter_unreviewed
    ON signature_dead_letter (reviewed, created_at);

COMMIT;
