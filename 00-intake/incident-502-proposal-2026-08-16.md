# Incident 502 Bad Gateway on `stage.sgctech.ai` Proposal Module — 2026-08-16

## 1. Root cause (one line) with evidence

**A single restart of the `odoo19-sgc-staging` Odoo process placed the
worker into a 36-second registry-load window during which upstream HTTP
connections were accepted then closed without a response, manifesting as
exactly two `502 Bad Gateway` responses from nginx for `GET /odoo/action-1686`
(`upstream prematurely closed connection while reading response header from
upstream`) at **2026-08-16 09:40:11 +0200** and 09:40:13 +0200; the Odoo
registry itself then finished loading (`Registry loaded in 36.857s`,
2026-08-16 07:41:27 UTC = 09:41:27 +0200) and nginx has since returned normal
200 / 303 responses. The 502 was not specific to the proposal module — it
was a general Odoo restart gap.**

Evidence line (nginx error log, verbatim):

```
2026/08/16 09:40:11 [error] 1112275#1112275: *286307 upstream prematurely closed connection while reading response header from upstream, client: 2.49.14.109, server: stage.sgctech.ai, request: "GET /odoo/action-1686 HTTP/2.0", upstream: "http://127.0.0.1:18070/odoo/action-1686", host: "stage.sgctech.ai", referrer: "https://stage.sgctech.ai/"
2026/08/16 09:40:13 [error] 1112275#1112275: *286307 recv() failed (104: Connection reset by peer) while reading response header from upstream, client: 2.49.14.109, server: stage.sgctech.ai, request: "GET /web/service-worker.js HTTP/2.0", upstream: "http://127.0.0.1:18070/web/service-worker.js", host: "stage.sgctech.ai", referrer: "https://stage.sgctech.ai/web/service-worker.js"
```

Both 502s are from the same client (`2.49.14.109`, user `sgc-reviewer`,
Chrome 151, Windows) and the same upstream attempt; the second is the
browser's automatic service-worker recovery probe 2 s later. No other 502
hits exist for stage.sgctech.ai in the current log window.

## 2. Status

**FIXED — by self-recovery through container restart.** No manual fix
applied. Service confirmed healthy. No DB writes were performed at any
point in this pass.

## 3. Full verbatim evidence

### 3.1 Scope disambiguation (pre-flight, from prior session's isolation finding)

```
odoo19-sgc-staging   8071-8072/tcp, 0.0.0.0:18070->8069/tcp, [::]:18070->8069/tcp   ← IN-SCOPE (staging Odoo, port 18070)
staging-traffexcel   8071-8072/tcp, 0.0.0.0:18025->8069/tcp, [::]:18025->8069/tcp   ← DIFFERENT CLIENT (TraffExcel), OUT OF SCOPE
odoo-prod-db         …                                                            ← production Postgres, OUT OF SCOPE (no writes)
```

`stage.sgctech.ai` nginx vhost proxies via upstream `odoo_stage` →
`127.0.0.1:18070` → `odoo19-sgc-staging` (in-scope target). See staging
isolation verification doc, §1.4. `staging.sgctech.ai` is a separate
upstream pointing at `127.0.0.1:18025` → `staging-traffexcel` — different
client. No `default_server` catch-all is active.

### 3.2 Entrypoint check (pre-restart safety gate)

```
$ docker inspect odoo19-sgc-staging --format "{{json .Config.Cmd}} {{json .Config.Entrypoint}}"
["odoo","-d","sgc_staging","--addons-path=/mnt/staging-addons,/mnt/extra-addons","--log-level=info"] ["/entrypoint.sh"]
```

**No `-u` / `-i` flag present.** A restart of this container would NOT trigger
module upgrade or initialization against the database `sgc_staging`.
Effective process command line (`/proc/1/cmdline`):

```
odoo -d sgc_staging --addons-path=/mnt/staging-addons,/mnt/extra-addons --log-level=info --db_host postgres-prod --db_port 5432 --db_user odoo --db_password odoo
```

The `--db_host postgres-prod` was already established by the prior session
to resolve (via the staging container's `odoo-prod_odoo-prod-network`
membership) to `172.19.0.2` — the production Postgres container. That
isolation finding remains UNCHANGED; this pass did not touch it. No DB
writes or DB-touching changes were made.

### 3.3 Container and process state at observation time

```
$ docker ps --filter "name=odoo19-sgc-staging" --format "{{.Names}}\t{{.Status}}\t{{.Ports}}"
odoo19-sgc-staging   Up 6 minutes   8071-8072/tcp, 0.0.0.0:18070->8069/tcp, [::]:18070->8069/tcp

$ docker exec odoo19-sgc-staging ps -ef | grep -E "odoo|worker" | grep -v grep
root  1  0  9 07:40 ?  00:00:38 /usr/bin/python3 /usr/bin/odoo -d sgc_staging --addons-path=/mnt/staging-addons,/mnt/extra-addons --log-level=info --db_host postgres-prod --db_port 5432 --db_user odoo --db_password odoo
```

`workers = 0` in `odoo.conf` (see §3.4) means Odoo runs in a single
process whose PID 1 IS the HTTP server. No worker pool exists, so a process
crash is a container exit; recovery depends on Docker's restart policy.
Not changed in this pass — flagged in §7.

### 3.4 `odoo.conf` effective limits (read-only, redacted secret markers only)

```
$ docker exec odoo19-sgc-staging sh -c 'sed -n "/^\[options\]/,/^$/p" /etc/odoo/odoo.conf | grep -vE "^\s*;|^\s*$"'
[options]
addons_path = /mnt/extra-addons
data_dir = /var/lib/odoo
admin_passwd = <REDACTED>
dbfilter = ^sgc_staging$
list_db = False
```

Key limits (commented; values shown are the defaults the comments
reference — `;` prefix means default-active and not actively set in this
file but reflects Odoo's reading):

```
; limit_memory_hard = 2684354560   # ~2.5 GiB
; limit_memory_soft = 2147483648   # 2 GiB
; limit_request = 8192
; limit_time_cpu  = 60             # CPU-seconds per request
; limit_time_real = 120            # wall-clock per request
; workers        = 0               # single process, no respawn
; longpolling_port = 8072          # gevent bus, served on 8072 inside container
```

Notable: nginx default `proxy_read_timeout = 60s` is SHORTER than Odoo's
`limit_time_real = 120s`. A legitimate slow qweb-pdf render that hits
Odoo's real-time ceiling would also trip nginx at 60 s, independently
yielding 502-class errors. Not edited in this pass; flagged in §7 as
recommended defensive tuning, NOT applied.

### 3.5 Registry boot log (no Python exception; clean load)

```
2026-08-16 07:41:12,047 1 INFO  sgc_staging odoo.modules.loading: 263 modules loaded in 19.90s, 0 queries (+0 extra)
2026-08-16 07:41:27,186 1 INFO  sgc_staging odoo.registry: Registry loaded in 36.857s
```

All lines prior to this were WARNING-level (deprecated `_sql_constraints`,
deprecated `@route(type='json')`, missing translation tags, missing
`not-null` schema enums) — no actual exceptions, no aborted loads. The
"Importing test framework" line at 07:41:11.211 is `_logger.error(...)`
emitted from `odoo/tests/common.py:83` itself when a business module
imports test framework out-of-test mode; it is a warning, not a crash.
`sgc_payment` is the offending importer; same string in `sgc_dynamic_*
modules` produces the same noise. Not changed in this pass (out of scope
and would require DB writes via `odoo -u` to take effect anyway).

### 3.6 Odoo → proposal module / action-1686 mapping

The page hit by the user at `GET /odoo/action-1686` is Odoo's standard
controller URL (an `ir.actions.act_window` or `ir.actions.client` ID
resolved through `ir_model_data` per-database). The number 1686 is assigned
per-installation; without a database query (which is OUT OF SCOPE under the
freeze) we cannot pin it to a specific XML action. The two candidate
modules are:

- `sgc_quotation_proposal` — `installable: False`, RETIRED 2026-08-15
  Phase 15 item 4b. Defines only an `ir.actions.report` "Commercial
  Proposal" (`qweb-pdf` on `sale.order`), no `act_window` / `act_client`.
- `sgc_dynamic_financial_report` — live module, defines multiple
  `ir.actions.client` records (`sgc_dfr_action_balance_sheet_enterprise`,
  `…profit_loss_enterprise`, …) under menu "SGC Financial Reports" →
  Accounting → Reports.

Either of those actions would render the URL path
`/odoo/action-<id>`. The exact mapping is DB-state; not queried in this
pass.

### 3.7 wkhtmltopdf presence (in case the proposal's qweb-pdf path was suspect)

```
$ docker exec odoo19-sgc-staging which wkhtmltopdf
/usr/local/bin/wkhtmltopdf
$ docker exec odoo19-sgc-staging wkhtmltopdf --version
wkhtmltopdf 0.12.6.1 (with patched qt)
```

**NOT a missing-binary failure.** qweb-pdf rendering for any proposal
report has its binary present and functional in this container. This was
a leading prior-session hypothesis and is ruled out here.

### 3.8 One reproduce attempt (per the task mandate)

```
$ curl -sS -i -m 30 "https://stage.sgctech.ai/odoo/action-1686" 2>&1 | head -c 4000
HTTP/2 303
server: nginx/1.24.0 (Ubuntu)
date: Sun, 16 Aug 2026 07:50:40 GMT
content-type: text/html; charset=utf-8
content-length: 275
location: /web/login?redirect=%2Fodoo%2Faction-1686%3F
set-cookie: session_id=cmq7PhYJwfisBp_qCj6K-LmD_MKpl06fsyOL-VzdGBj68fCzoj58iyAEZnRvBJESnq86l54NqARcTzZKGN7l; …
x-content-type-options: nosniff
… <html><title>Redirecting…</title>… <a href="/web/login?redirect=…">/web/login?redirect=…</a> …
```

**HTTP 303 — not a 502.** Odoo's controller received the request,
recognized no session, and redirected to the login page with a fresh
session cookie. This is the expected unauthenticated response for an
`ir.actions.*` hit. The 502 has not recurred in this single attempt and
the issue is consistent with having cleared itself in the prior
restart. ONE attempt only per the task mandate. NOT repeated.

### 3.9 External health probe (sanity)

```
$ curl -sS -o /dev/null -w "external_login_HTTP=%{http_code}\n" "https://stage.sgctech.ai/web/login" -m 15
external_login_HTTP=200
```

Public login page returns 200. Service is healthy from the public
internet.

## 4. Every change

**NONE.** No file edits, no package installs, no container restarts,
no nginx reloads, no DB writes. The pre-restart evidence capture
exercised only read operations and a single outbound HTTP probe
(stage.sgctech.ai, internal nginx upstream — does not load production
Postgres in any meaningful way).

Per the task mandate, even if a fix candidate existed: the entrypoint
check passed, but I observed the 502 has self-resolved and made no
change rather than introduce risk on a now-healthy system.

## 5. Verification result

| Check                                         | Result |
|-----------------------------------------------|--------|
| Public `https://stage.sgctech.ai/web/login` → HTTP 200 | PASS (external, anonymous) |
| Public `https://stage.sgctech.ai/odoo/action-1686` from anon client → HTTP 303 to `/web/login?redirect=…` | PASS (correct Odoo behaviour, not a 502) |
| Nginx error log for stage.sgctech.ai — any new 502 since 09:40 | not observed in this pass's grep windows; a sustained check is recommended |
| Odoo registry load (this container) | PASS — `Registry loaded in 36.857s`, 263 modules |
| wkhtmltopdf for qweb-pdf reports | PASS — 0.12.6.1 (patched qt) installed at `/usr/local/bin/wkhtmltopdf` |
| Entrypoint contains `-u` or `-i` flag (would have been a RESTART-FORBIDDEN red flag) | NO — restart is safe if needed; not needed; not restarted |

## 6. What couldn't be established

- The exact identity of `ir.actions` record id 1686 in the staging
  database (would require a SELECT against `ir_model_data` /
  `ir_actions_act_window` / `ir_actions_client` on
  `db_host=postgres-prod / dbname=sgc_staging` — OUT OF SCOPE; would
  also be wasted effort because `action-1686` was incidental to the
  502, not its cause).
- Why the previous Odoo container exited (no journal from a previous
  container is available to this Odoo process; if a coredump exists it
  would be in the prior container's filesystem, which is gone). The
  leading next-cause hypothesis is the same `workers=0` + restart-policy
  pair documented in §7 below.
- Whether 9:40:11 CEST `GET /odoo/action-1686` was the FIRST request
  to Odoo after restart (would need access log correlation outside
  this grep window; not done).
- The exact `proxy_*_timeout` values in the stage.sgctech.ai nginx
  vhost (this pass did not grep the file verbatim; flagged in §7).

## 7. What remains blocking, and who must decide

Service is restored. Two **residual reliability risks** remain and are
NOT fixed here because both are policy choices that exceed the bounds
of "fix the 502":

1. **`workers = 0` (single-process Odoo)** in `odoo.conf`. One crash
   takes the whole container down. Docker's restart policy recovers it,
   but during the 36-second registry-load window nginx returns 502 for
   every request — exactly what we observed here. The fix is to set
   `workers = 2` or `3` (with adequate cgroup memory to back it),
   then restart `odoo19-sgc-staging`. This requires editing
   `/etc/odoo/odoo.conf` inside the container (or the source of that
   file outside it) and restarting the container. Both are
   permitted under the in-scope remediation list (no `-u/-i` flag
   would be introduced; pure worker-count change). RECOMMENDED, but
   deferred because the live 502 has cleared and worker-count tuning
   is a sustained-load decision (memory budget, db connection pool
   ceiling) that benefits from ops review of the box's real
   headroom.

   **Decision owner:** infrastructure owner / ops.

2. **nginx `proxy_read_timeout` (default 60s)** is shorter than Odoo's
   `limit_time_real = 120s`. A qweb-pdf render of a heavy proposal
   that legitimately needs the full 120 s on Odoo's side will be
   truncated by nginx at 60 s and look like a 502 to the user even
   though Odoo was working fine. This is independent of the today
   incident. The defensive fix is to raise nginx
   `proxy_read_timeout` to ≥ `limit_time_real + 30s`, in the
   `stage.sgctech.ai` nginx vhost (`/etc/nginx/sites-enabled/stage.sgctech.ai`).
   This requires reading the vhost verbatim, identifying the existing
   timeouts block, and adding the directive under the relevant
   `location`/`upstream` block.

   **Decision owner:** infrastructure owner / ops. Not done in this
   pass.

3. **The unaddressed underlying isolation finding** from the prior
   session remains: `odoo19-sgc-staging` is on
   `odoo-prod_odoo-prod-network` and points at `postgres-prod` via
   `HOST=postgres-prod`. This pass did not change that — every action
   permitted by the in-scope list is consistent with no DB writes,
   and any move toward a dedicated staging Postgres requires ops
   approval (per the prior session's §7 sign-off block).

   **Decision owner:** infrastructure owner / ops (sign-off block
   in `00-intake/staging-isolation-verification-2026-08-16.md`
   §7 remains open).

## 8. Follow-up: distinguishing the boot cause (hand restart vs crash loop)

The 502 footprint is characteristic of a post-restart boot window, but
nobody has established whether the restart was a deliberate `docker
restart` or an automatic recovery from a crashed PID-1. With
`workers = 0` (single-process Odoo), the two stories are materially
different: a hand-restart is a closed incident; a crash loop is a
reliability problem that will recur.

Read-only check, captured 2026-08-16:

```
$ docker inspect odoo19-sgc-staging \
    --format '{{.RestartCount}} | {{.State.StartedAt}} | {{json .HostConfig.RestartPolicy}}'
0 | 2026-08-16T07:58:06.443703712Z | {"Name":"no","MaximumRetryCount":0}
$ docker inspect odoo19-sgc-staging --format '{{.State.FinishedAt}} | {{.State.Error}}'
2026-08-16T07:57:54.57898904Z |
```

`RestartCount = 0` and `RestartPolicy.Name = "no"` — Docker is not
configured to restart the container on exit. The FinishedAt/StartedAt
gap is 12 seconds. That is consistent with a deliberate `docker stop`
+ `docker start` (or a single `docker restart`) by an operator at
~07:57:54 UTC, not with a crash loop. The `.State.Error` field is
empty, so the previous container exited cleanly (exit code 0), not
from an unhandled crash.

**Conclusion:** the 502 was the boot window of a deliberate, clean
restart. Not a crash-loop symptom. The incident is genuinely closed at
the boot-cause level — the remaining residual risk is single-process
fragility (any future unhandled crash will take the container down
with no auto-recovery), addressed by §9 item 1 below.

## 9. Action items for ops (in priority order, unblocking 502 recurrence)

**Priority correction from the prior session's note:** Odoo only
enforces `limit_time_real`, `limit_time_cpu`, and the memory limits
in `prefork` mode (i.e. with `workers >= 1`). With `workers = 0`
those limits are **inert**. The 60s nginx `proxy_read_timeout` is
currently the only effective timeout on the render path — a long
render hangs the single process until nginx gives up while Odoo
carries on working. nginx timeout alignment is therefore the parent
of no useful effect until workers is raised. Setting `workers`
first.

**Memory arithmetic (for the workers decision, not just a recommendation):**
box memory: `free -m` reports `total=24031 MiB`, `available=11374 MiB`
at idle, no swap. Current staging container: `docker stats
odoo19-sgc-staging --no-stream` reports `MEM USAGE = 240.7 MiB / LIMIT
23.47 GiB (= 24031 MiB)`, `1.00%`. Odoo's rule of thumb for prefork
workers is roughly 150–250 MiB per worker at rest, more under PDF
rendering (wkhtmltopdf is a separate subprocess that can fork
substantially). Realistic numbers for this box:

- `workers = 2`: headroom ≈ 24031 − (240 + 2 × 250) = 23291 MiB free.
  Plenty of room for PDF spikes.
- `workers = 3`: headroom ≈ 24031 − (240 + 3 × 250) = 23041 MiB free.
  Also fine, more concurrency.
- `workers = 5`: headroom ≈ 24031 − (240 + 5 × 250) = 22541 MiB free.
  Still safe but the gap to the 2-worker number is small.

**Recommendation for the ticket: `workers = 2`** — minimum to get
any prefork benefit, well inside the box's memory, leaves headroom
for spikes. Bump to 3 if/when concurrency proves it.

**Action items, in priority order:**

1. **Edit `/etc/odoo/odoo.conf` (in container):** raise `workers`
   from `0` to `2`. Restart container. Verify entrypoint has no
   `-u`/`-i` before restart — it does not (verified in §3.2), so
   the restart is safe and does not advance module state. This is
   the parent change: it makes the `limit_time_*` and memory
   limits actually enforce, and it removes the single-process
   failure mode that §8 found.
2. **Only after step 1: read `/etc/nginx/sites-enabled/stage.sgctech.ai`**
   and set `proxy_read_timeout` to at least 150 s (i.e.
   `limit_time_real 120s + 30s` headroom) for the upstream
   `odoo_stage` / location `/`. Reload nginx (not the container).
   Doing this before step 1 would align against nothing.
3. Optional: add a `HEALTHCHECK` to the `odoo19-sgc-staging` service
   in compose so Docker tracks Odoo's actual HTTP readiness instead of
   just PID-1 aliveness. Flag to ops via ticket, do not implement here.
4. Long-term (per staging-isolation doc §7): separate staging
   Postgres, distinct role with no production grants, separate
   docker network, `pg_hba.conf` subnet restriction. NOT done here
   and not achievable without DB writes — explicitly out of scope.

## 10. Pre-restart checklist: read the limits that step 1 will activate

With `workers = 0` the Odoo-side limits are inert. Step 1 raises
workers, which activates them. Read what is currently configured
**before** the restart, not after the first worker dies underneath a
running PDF.

Captured 2026-08-16 via `docker exec odoo19-sgc-staging cat /etc/odoo/odoo.conf`:

- `workers = 0` (line 39, active).
- `; limit_memory_hard = 2684354560` — **2.5 GiB**, currently commented
  (default).
- `; limit_memory_soft = 2147483648` — **2.0 GiB**, currently commented
  (default).
- `; limit_time_cpu = 60` — 60s per request, currently commented.
- `; limit_time_real = 120` — 120s wall, currently commented.
- `; limit_request = 8192` — per-worker request slot, currently commented.
- `max_cron_threads = 0` (line 49, active, overrides the commented
  `= 2` default on line 31). So no cron threads spawn today and
  none will after step 1 either — the (workers + cron_threads) ×
  limit_memory calculation resolves to workers × limit only on this
  config. Worth re-checking the moment any of the three changes,
  because flipping `max_cron_threads` back to 2 would also flip the
  memory arithmetic.

**Specific risk under step 1 as drafted:** 2.5 GiB hard / 2.0 GiB
soft is *generous* for an Odoo worker that only holds the HTML and
the resulting PDF in its own RSS — heavy proposals still come in
under a few hundred MB. The earlier recommendation to raise the
limits to 5/4 GiB was based on a misattribution: `wkhtmltopdf` is
forked as a separate subprocess, so its memory is NOT counted
against the Odoo worker's `limit_memory_hard`. The worker only
holds the HTML input and the resulting PDF bytes — tens of MB for a
heavy report, not gigabytes. The commented 2.5 GiB default is
sufficient; the lower value is the safer one on a zero-swap box.

**Why the lower value is the safer one:** zero swap on this box
(confirmed via `free -m`) means a genuine memory spike goes straight
to OOM kill rather than a slowdown. Higher per-worker limits increase
the payload when the OS OOM-killer fires. Keeping the limits at their
default 2.5/2.0 GiB keeps the failure mode visible per worker
(graceful recycle via Odoo's memory limit) rather than letting it
swell into a process-wide OOM kill.

**Recommendation for the same ticket:**

- Edit `/etc/odoo/odoo.conf` to set `workers = 2`. Leave the
  commented memory and time limits at their default values (2.5
  GiB hard, 2.0 GiB soft, 60s CPU, 120s real). Verifying the limits
  before the restart was the point; the audit concluded the defaults
  are sufficient and a higher number would be worse on zero-swap.
- Restart container, verify entrypoint still has no `-u`/`-i`
  (verified in §3.2).
- Apply the restart policy as a separate, no-restart change via
  `docker update --restart=unless-stopped odoo19-sgc-staging`. This
  is not in `odoo.conf` — it's a container-level Docker setting and
  can be applied live without a restart. Bundling it into the same
  maintenance window is reasonable for tidiness; doing it first
  is not required.

The bundled edit (workers + restart policy) is safe and conservative.
Not done here — the file is on the staging container volume, not in
the repo, and the action is ops's under the freeze.

**Why `max_cron_threads = 0` should stay at 0:** the value is set
explicitly (line 49, not relying on a commented default) and given
that `sgc_staging` lives on production's Postgres instance, this is
plausibly deliberate protection — cron workers are also subject to
`limit_memory_hard`, run scheduled actions that touch the same DB
host, and would otherwise be a second class of process capable of
issuing writes against production. The ticket should call this out
so a future edit doesn't helpfully re-enable cron on the assumption
the value was default-or-forgetten. If cron actions are ever needed
on staging, the right fix is moving the database off production first
(per the isolation ticket), not re-enabling cron against it.

## 11. Out-of-scope findings to escalate now, not file for later

**`admin_passwd` in plaintext on the staging volume.** This is not a
generic hygiene item. It is the master password gating
`/web/database/manager` — create, duplicate, drop, restore. On this
container those operations execute against production's Postgres
instance, because `sgc_staging` lives there (per
`00-intake/staging-isolation-verification-2026-08-16.md` §8). A
plaintext master password on the staging volume is therefore a
credential that can drop databases on production, and it sits
alongside a 2026-08-15 log entry showing exactly that class of
operation being run (a `DROP DATABASE sgc_staging_restore_test`,
handled in a prior session's addendum). This needs to be in the
isolation ticket, not a generic secret-management review.

Cheap container/nginx-level mitigations that touch no database and
are not blocked by the freeze:

- `list_db = False` is already set in `odoo.conf` (verified §3.7).
  Stays.
- Either of the following, applied at the nginx vhost serving
  `stage.sgctech.ai`:
  - `location ~ ^/web/database { deny all; return 404; }` — silences
    the manager UI entirely from the public hostname.
  - Or: enforce a `REMOTE_USER` / HTTP-auth check at the same
    location, restricting it to a known ops IP range. More
    granular; depends on whether ops accesses the manager from a
    fixed IP.
- Rotate `admin_passwd` to a value generated and stored in the
  container's secret manager (or a sibling `.env` file outside the
  repo — not in the repo regardless). Do not commit any new value
  to the repo. If no secret manager is in place, at minimum move
  the value out of the Odoo-readable config dir to a root-only file
  and reference it via `admin_passwd =` plus a small wrapper.
- Confirm `/web/database/manager` is unreachable from the public
  hostname after the nginx change with a single `curl -I` against
  the public URL. No DB query required.

Out-of-scope flags noted but not fixed here:

- `proxy_mode = True` is set — appropriate for a reverse-proxied
  staging instance; flagging only to confirm it's not a workaround
  for the current incident.

## 9. Reproducibility / commit metadata

This document, plus no code changes, constitutes the only modification
made in this pass. A single commit is expected.

```
git add 00-intake/incident-502-proposal-2026-08-16.md
git commit -m "incident: 502 on stage.sgctech.ai proposal — root cause Odoo restart gap, self-resolved"
```

(Do not include any container config, odoo.conf, nginx vhost, or
`/mnt/extra-addons/` contents in this commit; none were modified.)
