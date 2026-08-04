#!/usr/bin/env python3
"""Odoo External API JSON-RPC 2.0 client with stub mode.

Odoo External API: POST https://<odoo-instance>/json/2/ with
Authorization: Bearer <api_key>. Operations mirror odoo-mapping.yaml:
search_read / write / create on crm.lead, ir.attachment, mail.activity,
account.move.

Stub mode (ODOO_URL / ODOO_DATABASE / ODOO_API_KEY unset): every operation
is recorded in-memory and returns a deterministic fake id, so the handler
runs end-to-end offline against the fixture pack.
"""
import base64
import json
import urllib.request


class OdooError(Exception):
    pass


class OdooClient:
    def __init__(self, url, database, api_key, stub_mode=False):
        self.url = url.rstrip("/")
        self.database = database
        self.api_key = api_key
        self.stub_mode = stub_mode or not (url and database and api_key)
        # Stub record of every call, keyed by operation name
        self.stub_calls = []
        self._stub_id = 1000

    # -- transport ---------------------------------------------------------

    def _call(self, method, params):
        if self.stub_mode:
            return self._stub(method, params)
        payload = json.dumps({
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": self._next_request_id(),
        }).encode("utf-8")
        req = urllib.request.Request(
            self.url + "/json/2/" if not self.url.endswith("/json/2/") else self.url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.api_key,
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise OdooError("Odoo HTTP {}: {}".format(exc.code, exc.reason))
        except urllib.error.URLError as exc:
            raise OdooError("Odoo unreachable: {}".format(exc.reason))
        if "error" in result:
            raise OdooError("Odoo error: {}".format(result["error"].get("message", result["error"])))
        return result.get("result")

    def _next_request_id(self):
        self._stub_id += 1
        return self._stub_id

    def _stub(self, method, params):
        """Deterministic offline stand-in; records the call for tests."""
        self.stub_calls.append({"method": method, "params": params})
        self._stub_id += 1
        if method == "call_kw" and params.get("method") == "search":
            model = params.get("model")
            domain = params.get("args", [[]])[0]
            # Fake: return the first id for any domain; 0 if empty domain
            if not domain:
                return []
            return [self._stub_id]
        if method == "call_kw" and params.get("method") == "write":
            return True
        if method == "call_kw" and params.get("method") == "create":
            return self._stub_id
        if method == "call_kw" and params.get("method") == "search_read":
            return []
        if method == "call_kw" and params.get("method") == "read":
            ids = params.get("args", [[], []])[0]
            ids = ids if isinstance(ids, list) else [ids]
            return {i: {} for i in ids}
        if method == "version":
            return {"server_version": "stub"}
        return True

    # -- crm.lead lookups ---------------------------------------------------

    def find_opportunity(self, envelope_id=None, proposal_ref=None):
        """Lookup order per odoo-mapping.yaml §CRM search lookup."""
        if envelope_id:
            ids = self._call("call_kw", {
                "model": "crm.lead",
                "method": "search",
                "args": [[["x_envelope_id", "=", envelope_id]]],
                "kwargs": {"limit": 5},
            })
            if ids:
                if len(ids) > 1:
                    raise OdooError(
                        "Multiple opportunities found for envelope {}".format(envelope_id)
                    )
                return ids[0]
        if proposal_ref:
            ids = self._call("call_kw", {
                "model": "crm.lead",
                "method": "search",
                "args": [[["name", "=", proposal_ref]]],
                "kwargs": {"limit": 5},
            })
            if ids:
                if len(ids) > 1:
                    raise OdooError(
                        "Multiple opportunities found for ref {}".format(proposal_ref)
                    )
                return ids[0]
        return None

    def read(self, model, ids, fields):
        """Read specific fields from records (e.g. x_frozen_pdf_hash)."""
        return self._call("call_kw", {
            "model": model,
            "method": "read",
            "args": [ids, fields],
        })

    def write(self, model, ids, values):
        return self._call("call_kw", {
            "model": model,
            "method": "write",
            "args": [ids, values],
        })

    def create(self, model, values):
        return self._call("call_kw", {
            "model": model,
            "method": "create",
            "args": [values],
        })

    def attach_pdf(self, res_model, res_id, name, pdf_bytes):
        """Create an ir.attachment holding a PDF (base64 datas)."""
        return self.create("ir.attachment", {
            "name": name,
            "type": "binary",
            "datas": base64.b64encode(pdf_bytes).decode("ascii"),
            "res_model": res_model,
            "res_id": res_id,
            "mimetype": "application/pdf",
        })
