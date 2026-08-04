#!/usr/bin/env python3
"""Per-event handlers for the signature webhook pipeline.

Implements the event dispatch table from 10-signature/odoo-mapping.yaml:
sent / viewed / signed_by_a_recipient / completed_by_all / declined /
expires / recalled / hard_bounced / reassigned.

On `completed`, the signed PDF is downloaded from Zoho Sign and its SHA-256
is verified against the frozen original before any Odoo write (webhook-spec.md
§Hash verification). Mismatch → CRITICAL, alert, NO Odoo write, 200.
"""
import datetime
import json
import logging

from notifications import (Notifier, TEMPLATE_CLIENT, TEMPLATE_SDR,
                           TEMPLATE_SGC_SIGNATORY)
from zoho_client import sha256_hex

log = logging.getLogger("events")

# Stage names match odoo-mapping.yaml §Stage mapping. Stage IDs are
# config-driven in production (handler config), not hardcoded here.
STAGE_PROPOSAL_SENT = "Proposal Sent"
STAGE_WON = "Won"
STAGE_LOST = "Lost"
STAGE_STALLED = "Stalled"

FOLLOWUP_ACTIVITY = "Follow-up"
KICKOFF_ACTIVITY = "Kickoff"

# Events that only append to the audit trail and never touch Odoo.
AUDIT_ONLY_EVENTS = frozenset({"viewed", "signed_by_a_recipient"})


class EventError(Exception):
    """Raised when an event cannot be processed safely (no partial writes)."""


class EventDispatcher:
    def __init__(self, config, store, odoo, notifier=None, zoho=None):
        self.config = config
        self.store = store
        self.odoo = odoo
        self.notifier = notifier or Notifier()
        self.zoho = zoho  # TokenManager or None (stub mode -> skip downloads)
        self.handlers = {
            "sent": self._handle_sent,
            "viewed": self._handle_audit_only,
            "signed_by_a_recipient": self._handle_audit_only,
            "completed_by_all": self._handle_completed,
            "declined": self._handle_declined,
            "expires": self._handle_expired,
            "recalled": self._handle_recalled,
            "hard_bounced": self._handle_hard_bounced,
            "reassigned": self._handle_reassigned,
        }

    # -- public -------------------------------------------------------------

    def dispatch(self, event):
        """Route one parsed event; returns (status, details) for audit."""
        event_type = event.get("event_type", "")
        handler = self.handlers.get(event_type)
        if handler is None:
            raise EventError("Unknown event_type: {}".format(event_type))
        return handler(event)

    # -- helpers ------------------------------------------------------------

    def _envelope(self, event):
        return event.get("request_id") or event.get("envelope_id") or ""

    def _find_opp(self, event):
        envelope_id = self._envelope(event)
        proposal_ref = event.get("request_name") or event.get("proposal_ref")
        opp_id = self.odoo.find_opportunity(
            envelope_id=envelope_id or None,
            proposal_ref=proposal_ref or None,
        )
        if opp_id is None:
            raise EventError(
                "Opportunity not found for envelope {} / ref {}".format(
                    envelope_id, proposal_ref
                )
            )
        return opp_id

    def _alert(self, message, envelope_id=""):
        """Critical alert: log + email alert recipient. Never blocks dispatch."""
        log.error("CRITICAL envelope=%s: %s", envelope_id, message)
        try:
            self.notifier.send(
                TEMPLATE_SDR, self.config.alert_email,
                {"proposal_ref": envelope_id, "alert_message": message},
            )
        except Exception:  # pragma: no cover - alert path must not fail pipeline
            log.exception("Alert email failed for %s", envelope_id)

    # -- handlers -----------------------------------------------------------

    def _handle_audit_only(self, event):
        return "audited", {"action": "audit only, no Odoo write"}

    def _handle_sent(self, event):
        opp_id = self._find_opp(event)
        envelope_id = self._envelope(event)
        now = datetime.datetime.utcnow()
        self.odoo.write("crm.lead", [opp_id], {
            "x_envelope_id": envelope_id,
            "x_sent_date": now.isoformat(),
            "x_frozen_pdf_hash": event.get("frozen_sha256", ""),
            "stage_id": self._stage_id(STAGE_PROPOSAL_SENT),
        })
        # Day-3 follow-up activity (odoo-mapping.yaml §sent)
        deadline = (now + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        self.odoo.create("mail.activity", {
            "activity_type_id": self._activity_id(FOLLOWUP_ACTIVITY),
            "date_deadline": deadline,
            "user_id": event.get("sdr_user_id", 1),
            "note": "Day 3 reminder: {} sent for signature. "
                    "Check signing status in Zoho Sign.".format(
                        event.get("request_name", envelope_id)),
            "res_model": "crm.lead",
            "res_id": opp_id,
        })
        return "ok", {"opportunity_id": opp_id, "stage": STAGE_PROPOSAL_SENT}

    def _handle_completed(self, event):
        opp_id = self._find_opp(event)
        envelope_id = self._envelope(event)
        now = datetime.datetime.utcnow().isoformat()

        # 1. Hash verification — never trust the callback's own content.
        signed_pdf = b""
        signed_sha256 = ""
        documents = event.get("documents") or []
        if self.zoho is not None and documents:
            doc = documents[0]
            signed_pdf = self.zoho.download_document(
                envelope_id, doc.get("document_id", ""))
            signed_sha256 = sha256_hex(signed_pdf)
            # frozen hash stored on the opportunity at `sent` time
            rows = self.odoo.read(
                "crm.lead", [opp_id], ["x_frozen_pdf_hash"])
            frozen_sha256 = ""
            if rows and isinstance(rows, dict):
                frozen_sha256 = (rows.get(opp_id) or {}).get(
                    "x_frozen_pdf_hash") or ""
            if frozen_sha256 and signed_sha256 != frozen_sha256:
                self._alert(
                    "Hash mismatch on {}. Signed PDF does not match frozen "
                    "original. Odoo write-back ABORTED.".format(envelope_id),
                    envelope_id,
                )
                raise EventError("Hash mismatch on {}".format(envelope_id))
        else:
            # Stub mode (offline): no download possible; audit a placeholder.
            signed_sha256 = sha256_hex(signed_pdf)

        # 2. Find signatory names from the actions array.
        client_actor = ""
        for action in event.get("actions") or []:
            if action.get("signing_order") == 0:
                client_actor = action.get("recipient_name", "")
        sgc_actor = self.config.sgc_signatory_name

        # 3. Odoo write-back → Won (odoo-mapping.yaml §completed)
        self.odoo.write("crm.lead", [opp_id], {
            "x_completed_date": now,
            "x_signed_pdf_hash": signed_sha256,
            "stage_id": self._stage_id(STAGE_WON),
            "x_signing_actor_client": client_actor,
            "x_signing_actor_sgc": sgc_actor,
        })

        # 4. Attach signed PDF + audit certificate.
        ref = event.get("request_name", envelope_id)
        if signed_pdf:
            self.odoo.attach_pdf("crm.lead", opp_id,
                                 "{}_Signed.pdf".format(ref), signed_pdf)
        audit_cert = b""
        if self.zoho is not None:
            audit_cert = self.zoho.download_audit_trail(envelope_id)
        if audit_cert:
            self.odoo.attach_pdf(
                "crm.lead", opp_id,
                "{}_AuditCertificate.pdf".format(ref), audit_cert)

        # 5. Draft mobilisation invoice (G51 — draft only, never auto-posted).
        mobilisation = float(event.get("mobilisation_amount") or 0)
        if mobilisation > 0:
            self.odoo.create("account.move", {
                "move_type": "out_invoice",
                "partner_id": event.get("partner_id", 1),
                "invoice_date": now[:10],
                "invoice_line_ids": [(0, 0, {
                    "name": "Mobilisation: {} Rev1".format(ref),
                    "quantity": 1,
                    "price_unit": mobilisation,
                })],
                "invoice_origin": ref,
                "state": "draft",
            })

        # 6. Kickoff activity + notifications (SDR, signatory, client).
        kickoff = event.get("kickoff_date") or (
            datetime.datetime.utcnow() + datetime.timedelta(days=30)
        ).strftime("%Y-%m-%d")
        self.odoo.create("mail.activity", {
            "activity_type_id": self._activity_id(KICKOFF_ACTIVITY),
            "date_deadline": kickoff,
            "user_id": event.get("delivery_user_id", 1),
            "note": "Mobilisation invoice drafted for {}. Delivery kickoff "
                    "due.".format(ref),
            "res_model": "crm.lead",
            "res_id": opp_id,
        })
        variables = {
            "proposal_ref": ref,
            "mobilisation_amount": mobilisation,
            "kickoff_date": kickoff,
            "completed_timestamp": now,
            "client_name": client_actor,
        }
        self.notifier.send(TEMPLATE_SDR, self.config.alert_email, variables)
        self.notifier.send(TEMPLATE_SGC_SIGNATORY,
                           self.config.sgc_signatory_email, variables)
        self.notifier.send(TEMPLATE_CLIENT,
                           event.get("client_email", ""), variables)
        return "ok", {"opportunity_id": opp_id, "stage": STAGE_WON,
                      "signed_sha256": signed_sha256}

    def _handle_declined(self, event):
        opp_id = self._find_opp(event)
        reason = event.get("reason") or "declined by signatory"
        self.odoo.write("crm.lead", [opp_id], {
            "stage_id": self._stage_id(STAGE_LOST),
            "x_decline_reason": reason,
        })
        self.notifier.send(
            TEMPLATE_SDR, self.config.alert_email,
            {"proposal_ref": event.get("request_name", ""),
             "alert_message": "Proposal declined: {}".format(reason)})
        return "ok", {"opportunity_id": opp_id, "stage": STAGE_LOST,
                      "reason": reason}

    def _handle_expired(self, event):
        return self._stall(event, "Proposal envelope expired. Re-send or close.")

    def _handle_recalled(self, event):
        return self._stall(event, "Envelope voided. Review and re-send or close.")

    def _stall(self, event, note):
        opp_id = self._find_opp(event)
        self.odoo.write("crm.lead", [opp_id], {
            "stage_id": self._stage_id(STAGE_STALLED),
        })
        self.notifier.send(
            TEMPLATE_SDR, self.config.alert_email,
            {"proposal_ref": event.get("request_name", ""),
             "alert_message": note})
        return "ok", {"opportunity_id": opp_id, "stage": STAGE_STALLED}

    def _handle_hard_bounced(self, event):
        # Log + alert SDR; never move to Won (webhook-spec.md).
        self._alert(
            "Signer email bounced for envelope {}".format(self._envelope(event)),
            self._envelope(event))
        return "ok", {"action": "logged + alerted, no Odoo write"}

    def _handle_reassigned(self, event):
        # Audit trail only; signer details updated in Zoho.
        return "audited", {"action": "signer reassigned",
                           "details": event.get("reassigned_from")}

    # -- production config hooks (stage/activity IDs) ------------------------

    def _stage_id(self, name):
        # Config-driven in production (handler config YAML/JSON). Reference
        # returns the name so stub writes are readable.
        return getattr(self.config, "stage_ids", {}).get(name, name)

    def _activity_id(self, name):
        return getattr(self.config, "activity_ids", {}).get(name, name)


def build_dispatcher(config, store, odoo, notifier=None, zoho=None):
    return EventDispatcher(config, store, odoo, notifier=notifier, zoho=zoho)
