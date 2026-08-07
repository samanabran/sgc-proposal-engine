# SDR follow-up (drafted, held — not sent)

**Purpose:** resolve the unsourced `users_now` figure blocking Stage 5
pricing (see `manifest.yaml` 2026-08-07 escalation, `CHANGELOG.md` and
`HANDOVER.md` §12). Commits nothing, quotes no figure.

**Route, per instruction (2026-08-07, updated):** internal review first,
not directly to Johnny. Bran (`bran@sgctech.ai`) reviews/approves →
forwarded to John, with a note that he should talk to Sadique about it
directly, presented as take-it-or-leave-it, and that clear, confirmed
commitment from Sadique is required before anything further is sent →
only then does a version reach Sadique (via Johnny Gurrera, SDR who
logged the 2026-07-24 client call, or directly by John — Bran/John's
call).

## Routing status

| Step | Status | Detail |
|---|---|---|
| 1. Internal review draft → Bran | **Sent as a Gmail draft, held (not sent)** | `bran@sgctech.ai`, subject "[Kallat KP-2026-SUB-01] Internal review — headcount confirmation to Sadique (hold for your approval)", created 2026-08-07 10:49 UTC, thread `19fdbd7544ad31e8`. Summarizes the blocker and the drafted message below, asks for approval before anything moves further. |
| 2. Forward to John | **Not created — waiting on Bran's approval** | To include: the drafted question below, plus the note that John should talk to Sadique directly, take-it-or-leave-it framing, clear commitment required before sending further. |
| 3. To Sadique | **Not created** | Contingent on step 2. |

Nothing has been sent to Sadique or to anyone outside SGC. The one
Gmail account connected to this session is `scholarixglobal@gmail.com`
(per prior Prosper attachment-5306 investigation, `HANDOVER.md` §8.1) —
the draft above was created from that account, addressed to Bran; if
that's not the right sending account for this to look right in his
inbox, say so and I'll recreate it from the correct one.

**Original route (superseded by the above, kept for reference):**
Johnny Gurrera (SDR, logged the 2026-07-24 client call) → Sadique
Abbas, Sales Manager, `sales@kallatproperties.com` / `+971 54 791 6003`.

**Why this is blocking, not routine:** for this deal specifically, headcount
sets the pricing segment directly (40 users vs. the 30-user `smb` ceiling),
which sets the hourly rate, which moves the quoted build value by ~28%.
There is no safe range to price into until this is confirmed — do not send
any figure ahead of Sadique's answer.

---

## Draft message (Johnny → Sadique)

> Hi Sadique,
>
> Quick follow-up while we finalize the proposal on our end — want to make
> sure we're scoping this correctly before we come back to you with numbers.
>
> When you mentioned 40–50 people earlier, were you referring specifically
> to active sales agents taking client-facing leads, or does that number
> also include admin/ops/management staff who'd need system access? And is
> 40 the number you'd want us to plan around today, or should we be sizing
> for the higher end of that range?
>
> A rough split is completely fine here — e.g. "about X client-facing,
> Y access-only" — you don't need an exact headcount for us to move forward.
>
> Thanks — will follow up once we hear back.
>
> Johnny

---

## Logging note

Per runbook, log Sadique's reply (whatever it is, including "don't know")
to this file and to `manifest.yaml` on receipt, then update
`00-intake/client-brief.yaml:12` and `02-calc/pricing-worksheet.yaml:
inputs.users_now` accordingly before Stage 5 resumes. Until a reply lands,
Stage 5 stays held per explicit instruction.
