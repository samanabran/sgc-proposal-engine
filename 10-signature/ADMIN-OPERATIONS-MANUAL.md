# Signature Webhook — Admin Operations Manual

**Audience:** SGC team members who send proposals for e-signature or operate the
webhook handler. **Status as of 2026-08-04: infrastructure proven reachable,
end-to-end signed delivery not yet confirmed, Odoo write-back not yet wired.**
Read the "Known Gaps" section before telling anyone this is production-ready.

---

## 1. What this system does

When a proposal is sent to a client via Zoho Sign, Zoho calls a **webhook**
(an HTTPS URL) every time something happens to the envelope — sent, viewed,
signed, completed, declined, expired, etc. A local handler service receives
those calls, verifies they really came from Zoho (HMAC signature check),
and is designed to update the matching Odoo CRM record automatically.

```
Zoho Sign  --POST-->  [tunnel]  --->  handler.py (127.0.0.1:8765)  --->  Odoo (currently stub mode)
```

Two pieces run locally and must both be up for anything to work:

1. **The handler** — `10-signature/handler/handler.py`, a Python process
   listening on `127.0.0.1:8765`.
2. **The tunnel** — currently `localhost.run` over SSH, which exposes that
   local port to the internet at a public `https://<random-id>.lhr.life` URL,
   because Zoho can't reach `127.0.0.1` directly.

---

## 2. Known gaps — read this before relying on it

| Gap | Impact | Who resolves it |
|---|---|---|
| Tunnel is free-tier `localhost.run` | URL changes every time the tunnel drops (observed 6+ times in one session, unattended, no alert) — if this happens after a real envelope is sent, `completed_by_all` is lost silently | Needs real hosting: paid Railway, Render, Fly, or an authenticated Cloudflare named tunnel, before relying on this for a live deal |
| Odoo write-back in stub mode | `sgc_crm_fields` is now installed on `app.sgctech.ai` / db `odoo19-sgc` (confirmed via server log: "Module sgc_crm_fields loaded", module count 253→254) — the crm.lead fields exist. But `ODOO_URL`/`ODOO_DATABASE`/`ODOO_API_KEY` still aren't set on the handler process, so it's still writing nowhere until that happens | Whoever restarts the handler sets the three env vars in their own shell (§4) using a freshly rotated API key — the one first shared for this needs rotating, see §8 |
| No real signed event has been observed passing cleanly end-to-end | The HMAC + timestamp code is verified by an *offline* fixture replay (10/10 pass) and a live bug fix, but not yet by an actual Zoho-originated `200` | Send a real envelope (or trigger a real Zoho Sign test send) once hosting is sorted, and confirm a clean `200` in the log |
| Secrets pasted into chat this session | Webhook HMAC secret, an OAuth refresh token, and a temp OAuth token were all typed into an AI chat session at some point | Rotate all three in Zoho's console before any live send, if not already done |
| Zoho account is on the 5-envelope free tier | Test sends cost real quota | Confirm plan/volume before doing throwaway tests |
| Branded sender (`hello@scholarixglobal.com`) not working | Signing emails come from `notifications@zohosign.com` | Not a blocker (Zoho's audit cert + hash chain carry legal weight regardless) — see `send-protocol.md` |

---

## 3. Sending a proposal for signature (day-to-day)

Follow the client's runbook exactly, e.g.
`02-clients/VGE-vongeyern-realestate/04-review/runbook-issue-rev3.md`. Short
version of the flow:

1. Confirm `validate.py` is clean and the gate report is signed.
2. Confirm the handler and tunnel are both up (§4 below).
3. Freeze the PDF with the issue footer, hash it, record the hash in
   `manifest.yaml`.
4. Compose the envelope (proposal + Order Form + MSA/SLA) and send via the
   verified two-step Zoho Sign API contract in the runbook's §5 — **this step
   requires live Zoho credentials and must be run by a human in their own
   shell**, never pasted into an AI chat.
5. Copy the frozen PDF into `05-issued/` immediately (never edit it after).
6. Watch the handler log for the `sent` event, then leave the rest to the
   webhook (or manually track status in Zoho Sign + update Odoo by hand until
   §2's Odoo write-back gap is closed).

**Do not send anything if a `RESOLVE:` field is open anywhere, or if
`validate.py` doesn't exit 0.**

---

## 4. Starting / restarting the handler

From `10-signature/handler/`, in your own shell (bash example):

```bash
cd "/c/sgc_proposal_engine/10-signature/handler"
export ZOHO_SIGN_WEBHOOK_SECRET="whsec_..."   # from Zoho's webhook config UI
python handler.py serve --host 127.0.0.1 --port 8765
```

Confirm it started: `Signature webhook listening on http://127.0.0.1:8765/...`

If port 8765 is already in use by a stale process, find and kill it first:

```powershell
Get-NetTCPConnection -LocalPort 8765 -State Listen | Select OwningProcess
taskkill //PID <pid> //F
```

**Never paste the secret value anywhere outside your own terminal** — not
into chat, not into a committed file (G52).

Sanity check after any restart:

```bash
curl http://127.0.0.1:8765/healthz          # expect {"status": "ok"}
python handler.py selftest ../webhook-fixtures   # expect "10 passed, 0 failed"
```

---

## 5. Starting / restarting the tunnel

```bash
ssh -o ServerAliveInterval=30 -o StrictHostKeyChecking=accept-new -R 80:127.0.0.1:8765 nokey@localhost.run
```

It prints a line like:

```
<random-id>.lhr.life tunneled with tls termination, https://<random-id>.lhr.life
```

**Verify it actually round-trips before trusting it** — registration
succeeding is not the same as working:

```bash
curl https://<random-id>.lhr.life/healthz   # expect {"status": "ok"}
```

This tunnel **will drop unattended** — it has done so repeatedly, sometimes
within 15 minutes, sometimes after longer. There is no alert when it does.
If you're relying on it for anything time-sensitive, check it periodically,
or better, don't rely on it — see §2.

---

## 6. Updating the webhook URL in Zoho Sign

Every time the tunnel restarts, the URL changes, and the webhook config in
Zoho Sign must be updated to match:

**Settings → Webhooks → (edit the webhook) → Callback URL:**

```
https://<current-tunnel-id>.lhr.life/webhooks/signature/zoho_sign/
```

(Note the trailing path — the bare domain is not enough.)

**Known false negative:** the **"Test Url"** button in that dialog fires a
bare reachability ping with no HMAC headers at all — it will *always* show
"Failure" against this handler, because the handler correctly refuses
unsigned requests by design (`webhook-spec.md` — "every inbound callback must
be verified"). **Do not treat a failed Test Url as a real problem** — save
the webhook anyway. The only real test is a genuine signed event.

Required settings in that same dialog:

| Setting | Value |
|---|---|
| Enable HMAC signature | On |
| Algorithm | HMAC-SHA256 |
| Enable timestamp | On |
| Events | Sent, Completed by all, Expires, Recalled, Viewed, Signed by a recipient, Declined, Reassigned, Hard bounced (skip "Approved by a recipient" — that's an approval-workflow event, unrelated to signature requests) |
| Basic Auth / mTLS / Custom headers | Off — not supported by this handler |

---

## 7. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `503 no tunnel here` | Tunnel dropped | Restart per §5, update Zoho per §6 |
| `401` + log says `Timestamp missing or unparseable: None` | This is the Zoho "Test Url" ping, not a real event | Ignore — see §6 |
| `401` + log says `Timestamp skew rejected... diff=178...s` (absurdly large) | Old bug: handler misread Zoho's millisecond timestamp as seconds | Fixed as of 2026-08-04 in `hmac_verify.py`; confirm you're running a handler process started *after* that fix |
| `config error: ZOHO_SIGN_WEBHOOK_SECRET is required` | Forgot to `export`/set the env var in the same shell before starting | Re-run §4's block as one sequence — env vars don't persist across separate shell invocations |
| Handler running but tunnel curl hangs then `HTTP 000` | Transient `localhost.run` edge hiccup | Retry once after a couple seconds before assuming it's dead |

---

## 8. Security rules (non-negotiable)

- **G52** — Zoho client secret, refresh token, webhook HMAC secret, Odoo API
  key: environment variables in your own shell only. Never in a file in this
  repo, never in a chat message (to a human or an AI assistant), never
  logged.
- If a secret is ever pasted somewhere it shouldn't be, treat it as
  compromised and rotate it — don't just delete the message.
- The actual Zoho Sign send (runbook §5) and any command that requires a live
  secret must be run by a person, in their own terminal — this is a hard
  rule, not a preference.
