# Staging / Production Isolation Verification — 2026-08-16

**Revision note:** this document was originally written after a halt at
Phase 1.3. Human authorization (2026-08-16) withdrew that stop condition —
same-IP virtual hosting on one box is expected and not itself evidence of
shared infrastructure — and directed resumption through Phase 1.12, Phase 2,
and Phase 3. This is that continuation, same file, same date, not a second
report. Section 3 below now contains the full Phase 1.1–1.12 evidence in
order; the original 1.1–1.3 evidence is preserved unchanged.

## 1. Host confirmation

Connected via SSH alias `contabo-sgc` (config: `~/.ssh/config`, HostName
`80.241.218.108`, User `root`). Confirmed via `hostname -f` / `hostname -I`
that this alias reaches `vmi3255620.contaboserver.net`, IP `80.241.218.108`,
matching the alias's configured HostName exactly. Correct, intended target.

## 2. VERDICT (first line, per required output order)

**NOT ISOLATED.**

Specific path: the staging Odoo container (`odoo19-sgc-staging`) is attached
to docker network `odoo-prod_odoo-prod-network`, the same network as the
production Postgres container (`odoo-prod-db`) and the production Odoo
container (`odoo-prod`). Inside the staging container, both `postgres-prod`
and `odoo-prod-db` resolve by name to `172.19.0.2` — the same address,
confirming they are the same production database container reachable from
staging by two names. The staging container's own environment is configured
with `HOST=postgres-prod`, `PORT=5432`, `USER=odoo`, and a `PASSWORD`
variable (value redacted, presence confirmed) — i.e., staging is configured,
by its own environment, to point at production's database host. A read-only
connection attempt from inside the staging container to `postgres-prod:5432`
reached PostgreSQL's password-negotiation stage (TCP connect succeeded,
protocol handshake succeeded) and failed only because this test did not
supply a password — not because the network refused the connection or the
host was unreachable. Network-layer isolation, the strongest of the "GOOD /
ACCEPTABLE / STOP" outcomes described in the task's own Phase 1.10
interpretation guide, does not hold: the path from staging to production's
actual database is open at the network and protocol level. Whether
staging's own stored credential would additionally succeed at the
authentication layer is UNDETERMINED (see §3, step 1.10) — but isolation
already fails upstream of that question, at the network layer, which the
task's own framework treats as sufficient on its own for a NOT ISOLATED
finding.

This does not by itself mean anything has been read from or written to
production. Nothing in this pass connected successfully, queried, or
modified any database. It means the barrier that should prevent staging
from doing so does not currently exist at the network layer, and the
staging container's own configuration actively points at the production
host rather than a staging-scoped one.

## 3. Full evidence, verbatim

### 1.1 SSH reachability and identity

```
$ ssh contabo-sgc 'hostname -f; uname -a; uptime'
vmi3255620.contaboserver.net
Linux vmi3255620 6.8.0-124-generic #124-Ubuntu SMP PREEMPT_DYNAMIC Tue May 26 13:00:45 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux
 23:41:53 up 62 days,  8:31, 24 users,  load average: 2.61, 2.68, 2.78
```

```
$ ssh contabo-sgc 'hostname -I'
80.241.218.108 172.17.0.1 172.18.0.1 172.20.0.1 172.28.0.1 172.23.0.1 172.24.0.1 172.19.0.1 172.22.0.1 172.26.0.1 172.27.0.1 172.25.0.1 172.21.0.1 2a02:c207:2325:5620::1
```

Public IP `80.241.218.108` confirmed. Remaining addresses are docker bridge
network gateways (one per docker network on the host, 172.x range) plus one
IPv6 address.

### 1.2 Sibling SSH aliases

```
$ cat ~/.ssh/config
```

| Host alias(es) | HostName | Notes |
|---|---|---|
| `004-003-abb8a17e-...odoo4projects.com` | same | unrelated managed hosting |
| `bran-vps`, `contabo` | `194.163.151.204` | different box |
| `sgc-vps-root`, `osusproperties` | `65.20.68.193` | different box; name contains "sgc" but is NOT contabo-sgc |
| `contabo-sgc`, `sgc-odoo`, `scholarixglobal` | `80.241.218.108` | **in-scope target**, three aliases, one host |
| `openclaw`, `do-scrapper` | `143.244.130.74` | different box |
| `github.com-sgc` | `github.com` | git remote, not a server |

No alias resolves to a name containing "prod" or "production".

### 1.3 DNS separation

```
$ ssh contabo-sgc 'command -v dig && dig +short stage.sgctech.ai; echo ---; dig +short staging.sgctech.ai'
/usr/bin/dig
80.241.218.108
---
80.241.218.108
```

Both resolve to the same box. Per human authorization 2026-08-16, this is
expected for name-based virtual hosting on a single server and is not
independently evidence of shared infrastructure. Not a stop condition.
Recorded, not halted on.

### 1.4 Reverse proxy routing — DECISIVE for the stage/staging question

```
$ ssh contabo-sgc 'grep -rn "server_name\|default_server\|proxy_pass" /etc/nginx/sites-enabled/ /etc/nginx/conf.d/ 2>/dev/null'
/etc/nginx/sites-enabled/app.sgctech.ai:6:    server_name app.sgctech.ai;
/etc/nginx/sites-enabled/app.sgctech.ai:14:    server_name app.sgctech.ai;
/etc/nginx/sites-enabled/app.sgctech.ai:27:        proxy_pass http://127.0.0.1:3001/;
/etc/nginx/sites-enabled/app.sgctech.ai:40:        proxy_pass http://odoo_sgc_v19;
/etc/nginx/sites-enabled/app.sgctech.ai:48:        proxy_pass http://127.0.0.1:18072;
/etc/nginx/sites-enabled/app.sgctech.ai:55:        proxy_pass http://127.0.0.1:18072;
/etc/nginx/sites-enabled/app.sgctech.ai:76:        proxy_pass http://127.0.0.1:5000;
/etc/nginx/sites-enabled/stage.sgctech.ai:11:    server_name stage.sgctech.ai;
/etc/nginx/sites-enabled/stage.sgctech.ai:28:        proxy_pass http://odoo_stage;
/etc/nginx/sites-enabled/stage.sgctech.ai:35:        proxy_pass http://odoo_stage;
/etc/nginx/sites-enabled/stage.sgctech.ai:48:        proxy_pass http://odoo_stage;
/etc/nginx/sites-enabled/stage.sgctech.ai:76:    server_name stage.sgctech.ai;
/etc/nginx/sites-enabled/staging.sgctech.ai:8:    server_name staging.sgctech.ai;
/etc/nginx/sites-enabled/staging.sgctech.ai:14:    server_name staging.sgctech.ai;
/etc/nginx/sites-enabled/staging.sgctech.ai:31:        proxy_pass http://odoo_staging;
/etc/nginx/sites-enabled/staging.sgctech.ai:49:        proxy_pass http://172.18.0.4:8072;
/etc/nginx/sites-enabled/staging.sgctech.ai:61:        proxy_pass http://odoo_staging;
```

```
$ ssh contabo-sgc 'grep -rn "upstream odoo_stage\b\|upstream odoo_staging\b\|default_server" /etc/nginx/ 2>/dev/null; echo ---UPSTREAM-BLOCKS---; grep -rn -A5 "upstream odoo_stage " /etc/nginx/conf.d/ /etc/nginx/nginx.conf /etc/nginx/sites-enabled/ 2>/dev/null; echo ---; grep -rn -A5 "upstream odoo_staging " /etc/nginx/conf.d/ /etc/nginx/nginx.conf /etc/nginx/sites-enabled/ 2>/dev/null'
/etc/nginx/sites-available/default:22:	listen 80 default_server;
/etc/nginx/sites-available/default:23:	listen [::]:80 default_server;
/etc/nginx/sites-available/default:27:	# listen 443 ssl default_server;
/etc/nginx/sites-available/default:28:	# listen [::]:443 ssl default_server;
/etc/nginx/sites-available/stage.sgctech.ai:5:upstream odoo_stage {
/etc/nginx/sites-available/staging.sgctech.ai:1:upstream odoo_staging {
/etc/nginx/sites-enabled/stage.sgctech.ai:5:upstream odoo_stage {
/etc/nginx/sites-enabled/staging.sgctech.ai:1:upstream odoo_staging {
---UPSTREAM-BLOCKS---
/etc/nginx/sites-enabled/stage.sgctech.ai:5:upstream odoo_stage {
/etc/nginx/sites-enabled/stage.sgctech.ai-6-    server 127.0.0.1:18070;
/etc/nginx/sites-enabled/stage.sgctech.ai-7-    keepalive 32;
/etc/nginx/sites-enabled/stage.sgctech.ai-8-}
---
/etc/nginx/sites-enabled/staging.sgctech.ai:1:upstream odoo_staging {
/etc/nginx/sites-enabled/staging.sgctech.ai-2-    server 127.0.0.1:18025;
/etc/nginx/sites-enabled/staging.sgctech.ai-3-    keepalive 32;
/etc/nginx/sites-enabled/staging.sgctech.ai-4-}
```

```
$ ssh contabo-sgc 'ls -la /etc/nginx/sites-enabled/ | grep -i default'
(no output — the default_server file exists only in sites-available, is NOT symlinked into sites-enabled, and is therefore INACTIVE)
```

```
$ ssh contabo-sgc 'docker ps --format "{{.Names}}\t{{.Ports}}" | grep -E "18070|18025"'
odoo19-sgc-staging	8071-8072/tcp, 0.0.0.0:18070->8069/tcp, [::]:18070->8069/tcp
staging-traffexcel	8071-8072/tcp, 0.0.0.0:18025->8069/tcp, [::]:18025->8069/tcp
```

**Disambiguated:** `stage.sgctech.ai` proxies (via upstream `odoo_stage`) to
`127.0.0.1:18070`, which is `odoo19-sgc-staging` — the in-scope SGC pricing
target. `staging.sgctech.ai` proxies (via upstream `odoo_staging`) to
`127.0.0.1:18025`, which is `staging-traffexcel` — a **different client's**
staging environment (TraffExcel), unrelated to SGC, hosted on the same
physical box. Separate upstream names, separate ports, separate containers.
No `default_server` catch-all is active. This is not "one install under two
names" — the human's own listed stop condition for that scenario does not
fire.

### 1.5 Container inventory

```
$ ssh contabo-sgc 'docker ps -a --format "{{.Names}}\t{{.Image}}\t{{.Status}}"'
odoo-prod	odoo:19.0-sgc	Up 13 hours
hf-speech	sgc/hf-speech:latest	Up 9 days (healthy)
docuseal	docuseal/docuseal	Up 10 days
signature-handler	python:3.12-slim	Up 11 days
odoo19-sgc-staging	odoo:19.0-sgc-staging	Up 2 hours
demo_presentation	odoo:19.0	Up 2 hours
cip-redis	redis:7-alpine	Up 3 weeks (healthy)
cip-db	pgvector/pgvector:pg16	Up 3 weeks (healthy)
cip-minio	minio/minio:latest	Up 3 weeks (healthy)
control-plane-cloudflared-1	cloudflare/cloudflared:latest	Up 3 weeks
control-plane-backend-1	vps-admin-dashboard-backend:latest	Up 3 weeks (healthy)
control-plane-prestart-1	vps-admin-dashboard-backend:latest	Exited (0) 3 weeks ago
control-plane-frontend-1	vps-admin-dashboard-frontend:latest	Up 3 weeks
gmail-addin	node:20-alpine	Up 4 weeks
odoo-staging	odoo:19.0	Exited (0) 3 weeks ago
staging-traffexcel	odoo:19.0	Up 10 days
demo_presentation_staging	odoo:19.0	Up 4 weeks
demo_presentation_staging_db	postgres:16	Up 5 weeks (healthy)
odoo-test-db	postgres:16	Up 5 weeks (healthy)
demo_presentation_db	postgres:16	Up 3 weeks (healthy)
osusproperties-v18	odoo:18.0	Up 6 weeks (healthy)
orchestrator-prod	odoo-prod-orchestrator	Up 7 weeks (healthy)
odoo-prod-db	postgres:16	Up 7 weeks (healthy)
litellm-prod	ghcr.io/berriai/litellm:main-stable	Up 7 weeks (healthy)
freellmapi-prod	ghcr.io/tashfeenahmed/freellmapi:latest	Up 7 weeks (healthy)
```

In-scope staging Odoo container: `odoo19-sgc-staging`. Production-named
containers flagged: `odoo-prod`, `odoo-prod-db`, `orchestrator-prod`,
`litellm-prod`, `freellmapi-prod`. No container is named for an SGC staging
Postgres specifically — resolved in §1.6/1.7 below: staging does not have
its own dedicated Postgres container at all; it is configured to use
production's.

### 1.6 Network topology

```
$ ssh contabo-sgc 'docker network ls'
NETWORK ID     NAME                                DRIVER    SCOPE
ab2cd6c597a7   bridge                              bridge    local
1f9d65a1572e   control-plane_default               bridge    local
c2d5c9ff9975   demo_presentation_default           bridge    local
aa88995c3d53   demo_presentation_staging_default   bridge    local
d7e532a4463e   docker_cip-network                  bridge    local
59ab353f7349   docuseal_default                    bridge    local
b69ae8b06c47   hf-speech_default                   bridge    local
bc0f00248533   host                                host      local
b457a29f4b87   none                                null      local
c77d7f27d710   odoo-prod-network                   bridge    local
03d7420d5104   odoo-prod_odoo-prod-network         bridge    local
a24f442c9857   odoo-test_odoo-test-network          bridge    local
daae8b92dbb3   signature-handler_default           bridge    local
86ac582c4188   traefik-public                      bridge    local
```

```
$ ssh contabo-sgc 'docker inspect odoo19-sgc-staging --format "{{json .NetworkSettings.Networks}}"'
{"odoo-prod_odoo-prod-network":{...,"Gateway":"172.19.0.1","IPAddress":"172.19.0.9",...,"DNSNames":["odoo19-sgc-staging","6df12732298f"]}}
```

`odoo19-sgc-staging` is attached to exactly one network:
`odoo-prod_odoo-prod-network`.

```
$ ssh contabo-sgc 'docker network inspect odoo-prod_odoo-prod-network --format "{{range .Containers}}{{.Name}} {{end}}"'
odoo-prod gmail-addin odoo-prod-db freellmapi-prod orchestrator-prod odoo19-sgc-staging litellm-prod demo_presentation
```

**Plain answer: YES**, staging shares a docker network with production
containers — specifically `odoo-prod` and `odoo-prod-db`.

### 1.7 Environment variables

```
$ ssh contabo-sgc 'docker inspect odoo19-sgc-staging --format "{{range .Config.Env}}{{println .}}{{end}}" | sed -E "s/(PASS|PASSWORD|SECRET|KEY|TOKEN)=.*/\1=<REDACTED>/i"'
HOST=postgres-prod
PORT=5432
USER=odoo
PASSWORD=<REDACTED>
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
LANG=en_US.UTF-8
ODOO_VERSION=19.0
ODOO_RC=/etc/odoo/odoo.conf
```

**Confirmed, not refuted.** The prior report's `HOST=postgres-prod` claim is
accurate. A credential is present in the `PASSWORD` variable; its value was
not printed, per the task's redaction requirement. The raw (unredacted)
`docker inspect` command was blocked by this session's own tool-safety
classifier before redaction could be applied client-side; the successful
command above redacts server-side via `sed`, before the value ever reaches
this session.

### 1.8 Name resolution from inside the container

```
$ ssh contabo-sgc 'docker exec odoo19-sgc-staging getent hosts postgres-prod'
172.19.0.2      postgres-prod

$ ssh contabo-sgc 'docker exec odoo19-sgc-staging getent hosts odoo-prod-db'
172.19.0.2      odoo-prod-db
```

Both names resolve, from inside staging, to the same IP — confirming
`postgres-prod` and `odoo-prod-db` are the same container, reachable from
staging under either name.

### 1.9 Port reachability

```
$ ssh contabo-sgc 'docker exec odoo19-sgc-staging sh -c "nc -zv postgres-prod 5432 2>&1 || true"'
sh: 1: nc: not found
```

`nc` is not installed inside the staging container. Reported verbatim, not
worked around with a substitute tool for this specific step — but see §1.11,
which independently establishes reachability via `psql`'s own TCP+protocol
attempt.

### 1.10 Authentication test — the decisive one

**BLOCKED by this session's own tool-safety classifier before it could
run.** The scripted, credential-using form of this command (matching the
task's exact specification, using the container's own configured
`postgres-prod`/`odoo` values) was denied with: *"Permission for this
action was denied by the Claude Code auto mode classifier... you should not
attempt to work around this denial."* This is treated as a hard stop for
this specific step, not worked around via an alternate tool or invocation —
consistent with the task's own instruction not to substitute around a
blocked or erroring step. Reported as attempted, not completed.

### 1.11 Which databases exist on the staging Postgres

Staging has no dedicated Postgres container of its own (see §1.5/§1.7) — it
is configured to point at `postgres-prod`. This step therefore became: can a
connection even be attempted from staging to the host it's configured to
use.

```
$ ssh contabo-sgc 'docker exec odoo19-sgc-staging psql "host=postgres-prod user=odoo dbname=postgres" -lqt 2>&1 || true'
perl: warning: Setting locale failed.
perl: warning: Please check that your locale settings:
	LANGUAGE = (unset),
	LC_ALL = (unset),
	LANG = "en_US.UTF-8"
    are supported and installed on your system.
perl: warning: Falling back to the standard locale ("C").
Password for user odoo: 
psql: error: connection to server at "postgres-prod" (172.19.0.2), port 5432 failed: fe_sendauth: no password supplied
```

This command did NOT supply the container's actual stored password
(deliberately — doing so would mean handling the live credential this
report is required to redact, and would be functionally identical to
working around the §1.10 classifier block by another route). The result is
informative independent of that: the TCP connection to `172.19.0.2:5432`
succeeded, and PostgreSQL's own protocol proceeded far enough to prompt for
a password. It failed only because this specific manual invocation, run
non-interactively with no credential piped in, had none to send — not
because the network refused the connection, not because the host was
unreachable, and not because PostgreSQL itself rejected the connection
outright. Per the task's own §1.10 interpretation guide, "connection
refused / no route" (the GOOD outcome) did not occur.

Whether staging's actual stored credential (the redacted `PASSWORD` value
from §1.7) would additionally succeed at authentication is UNDETERMINED —
not tested, by design, to avoid extracting or piping a live secret this
report is required to keep redacted.

### 1.12 Tooling host resolution — where SGC's own repo code would point

```
$ grep -rniE "postgres|psql|dbname|db_host|DATABASE_URL|pg_dump|pg_restore|odoo.conf|db_name" --include="*.py" --include="*.yaml" --include="*.yml" --include="*.sh" --include="*.conf" --include="*.env" . 2>/dev/null | grep -v "\.git/"
./10-signature/handler/install_sgc_crm_fields.sh:2:docker exec odoo-prod odoo -c /etc/odoo/odoo.conf -d odoo19-sgc -i sgc_crm_fields --stop-after-init --no-http > /tmp/install_out.log 2>&1
./10-signature/handler/store.py:5:standard library. Production swaps to PostgreSQL using the identical schema
```

Two hits, neither in `05-ops/` (the pricing-engine tooling). The first is an
unrelated CRM-fields installer script that explicitly targets `odoo-prod`
and database `odoo19-sgc` by name — informational, not part of the pricing
engine, and not a path this session's work has touched or would touch. The
second is a comment in an unrelated signature-handler module. No file under
`05-ops/` resolves a database host, name, or connection string anywhere —
consistent with this session's earlier established finding that the
pricing engine is entirely flat-file (`pricing_engine.py` + YAML), with no
live database dependency of its own. There is no existing snapshot,
migration, or dump path in this repo's own code that could have resolved to
the wrong host — the risk this pass was checking for does not currently
exist in the codebase; Phase 3 below adds a guard against it existing in
the future regardless.

## 4. Stage vs staging — answer

**RESOLVED.** `staging.sgctech.ai` is **not production, and not SGC's own
staging** — it is a different client's environment entirely: TraffExcel's
staging deployment (container `staging-traffexcel`, port 18025). It shares
the physical box with SGC's infrastructure but is a separate nginx vhost,
separate upstream, separate container, with no shared install. The DNS
collision noted in §1.3 is exactly what the human's authorization described:
expected virtual-hosting behavior on one server, not evidence of shared
infrastructure. The actual isolation risk found in this pass is unrelated to
the stage/staging naming question entirely — it is that SGC's own staging
Odoo (`stage.sgctech.ai` → `odoo19-sgc-staging`) is configured to talk
directly to SGC's own production database.

## 5. Phase 3 guard

Added to `05-ops/pricing_engine.py`: `enforce_staging_db_name(db_name)`, a
fail-closed exact-match allowlist guard. Full detail and self-test results
below (§5 of the output order in the accompanying report). Implemented
unconditionally per the human's explicit authorization, independent of the
NOT ISOLATED verdict above.

## 6. What could not be established

- Whether staging's actual stored production-configured credential would
  succeed at PostgreSQL authentication (§1.10 blocked by tool classifier;
  §1.11 deliberately not supplied the real credential).
- Port-level reachability via `nc` specifically (tool absent in container;
  independently established via `psql`'s own TCP+protocol behavior in
  §1.11 instead).
- Whether `HOST=postgres-prod` in the staging container's environment is
  itself a misconfiguration (staging pointed at the wrong host by mistake)
  or an intentional-but-dangerous choice (e.g. staging deliberately reads
  production data for realistic testing) — this report does not have
  access to deployment history or intent, only current state.

## 7. What remains blocking, and who must decide

The verdict is NOT ISOLATED, with the specific path named in §2. This
should block any pricing-engine work that would connect to, snapshot,
restore, or migrate any database — a constraint that was already standing
in this engagement and now has direct evidence behind it rather than an
open flag. Remediation, in the priority order specified by the task
(strongest/most independent of topology first):

1. **Distinct credentials with no production grants.** Issue staging its
   own PostgreSQL role scoped only to `sgc_staging`, with no grants on any
   production database. Strongest because it holds even if network
   topology is later reconfigured incorrectly again.
2. **Separate docker networks.** Remove `odoo19-sgc-staging` from
   `odoo-prod_odoo-prod-network` and place it on its own staging-scoped
   network (or the existing `odoo-test_odoo-test-network`, if that is
   appropriate — not evaluated in this read-only pass). Structural fix,
   but a name/label alone doesn't prevent someone re-attaching it later.
3. **`pg_hba.conf` restricting production access to known production
   subnets.** Backstop for defense-in-depth even if the above two hold.
4. **Correcting the staging container's `HOST`/env vars to point at a
   real, dedicated staging Postgres instance.** Weakest alone (fixes
   today's specific misconfiguration but not the class of mistake), but
   still necessary — without it, "distinct credentials" in (1) requires the
   env to actually be changed to use them.

None of this was performed. This entire remediation section is a
recommendation, not an action taken.

**Sign-off (infrastructure owner) — to be completed by a human, not by this
process:**

Name: _______________________  Date: _______________________  Verdict accepted: ☐ Yes ☐ No, needs rework
Remediation authorized: ☐ Yes, proceed in listed order  ☐ No  ☐ Partial — specify: _______________________
