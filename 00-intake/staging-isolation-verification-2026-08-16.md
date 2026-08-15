# Staging / Production Isolation Verification — 2026-08-16

## 1. Host confirmation

Connected via SSH alias `contabo-sgc` (config: `~/.ssh/config`, HostName
`80.241.218.108`, User `root`). Confirmed via `hostname -f` / `hostname -I`
that this alias reaches `vmi3255620.contaboserver.net`, IP `80.241.218.108`,
which matches the alias's configured HostName exactly. This is the correct,
intended target.

## 2. VERDICT (first line, per required output order)

**STOPPED AT PHASE 1.3 — TASK HALTED PER STOP CONDITION. VERDICT: UNDETERMINED.**

Evidence gathering stopped at step 1.3 of 1.12 because an explicit,
enumerated STOP CONDITION fired: `stage.sgctech.ai` and `staging.sgctech.ai`
resolve to the SAME IP address. Per the task's own instructions this halts
all further action, including Phase 3 (the fail-closed guard was NOT
implemented this pass — see §5).

This is NOT a "not isolated" finding about the database — no evidence was
gathered on docker networking, environment variables, or database
authentication (Phase 1.4 onward never ran). It is a finding that the task's
own premise is contradicted by DNS reality: the prompt states
`staging.sgctech.ai` is "a completely different system... not the same box"
as `stage.sgctech.ai`. That claim does not hold. Both names point at the same
server this session already has root SSH access to.

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
network gateways (172.x range, one per docker network on the host) plus one
IPv6 address.

### 1.2 Sibling SSH aliases

```
$ cat ~/.ssh/config
```

Host entries found (verbatim, IdentityFile paths preserved, no key material
printed):

| Host alias(es) | HostName | Notes |
|---|---|---|
| `004-003-abb8a17e-8683-43de-a564-791dd1a70929.odoo4projects.com` | same | unrelated — odoo4projects.com managed hosting, port 2274, `git` user |
| `bran-vps`, `contabo` | `194.163.151.204` | different IP, different box — NOT contabo-sgc |
| `sgc-vps-root`, `osusproperties` | `65.20.68.193` | different IP, different box, different SGC-prefixed name — flagged as a name that COULD be confused with "sgc" scope but resolves to a different host entirely |
| `contabo-sgc`, `sgc-odoo`, `scholarixglobal` | `80.241.218.108` | **this is the in-scope target** — three aliases, one host |
| `openclaw`, `do-scrapper` | `143.244.130.74` | different IP, different box |
| `github.com-sgc` | `github.com` | git remote alias, not a server |

No alias in this config resolves to a name containing "prod" or "production".
`sgc-vps-root` / `osusproperties` is a DIFFERENT physical host (65.20.68.193)
from contabo-sgc and was not touched — flagging only because "sgc" in its
alias name could cause a future mis-tab-complete; it is not the same box as
anything used this session.

### 1.3 DNS separation — DECISIVE, STOP CONDITION FIRED HERE

Local machine has no `dig` binary (`bash: dig: command not found`). Ran the
lookup FROM contabo-sgc itself instead (this is a DNS resolution query, not
a connection to either target — read-only, no state changed on any host):

```
$ ssh contabo-sgc 'command -v dig && dig +short stage.sgctech.ai; echo ---; dig +short staging.sgctech.ai'
/usr/bin/dig
80.241.218.108
---
80.241.218.108
```

**`stage.sgctech.ai` → 80.241.218.108**
**`staging.sgctech.ai` → 80.241.218.108**

Identical. This is the exact STOP CONDITION named in the task: *"If these
resolve to the SAME IP, this is a STOP CONDITION. Report and halt."*

Evidence gathering stopped here. Steps 1.4 through 1.12 (nginx routing,
container inventory, docker network topology, environment variables, name
resolution from inside the container, port reachability, the authentication
test, database listing, and repo-wide connection-string grep) were **NOT
RUN**. No commands beyond what is shown above were executed against
contabo-sgc after this result.

## 4. Stage vs staging — answer

**UNRESOLVED, explicitly not guessed at.** What is known: both hostnames
resolve to the same server (`80.241.218.108`, `contabo-sgc`). What is NOT
known, because Phase 1.4 (nginx vhost routing) never ran: whether
`staging.sgctech.ai` is served by the same nginx vhost as `stage.sgctech.ai`
(i.e., truly the same application/database), a distinct vhost on the same
box proxying to a different container, or an unmatched hostname absorbed by
a `default_server` catch-all. All three are consistent with the DNS evidence
above and have very different risk profiles. Determining which requires the
`server_name`/`default_server`/`proxy_pass` grep specified in the original
task's Phase 1.4, which was not run because the stop condition fired first.

Do not infer an answer from the two remaining possibilities not tested. The
honest state is: same box, unknown routing, unknown whether it is production
under an unfortunate name, another client's environment, or something else
entirely.

## 5. Phase 3 guard

**NOT IMPLEMENTED THIS PASS.** The task states Phase 3 is "the only change
permitted this pass" and instructs it to proceed "regardless of the Phase 2
verdict" — but the STOP CONDITION section is written as an unqualified
override: *"halt immediately, report, take no further action"* with no
carve-out for Phase 3. Given the task's own premise about staging.sgctech.ai
turned out to be false, proceeding to write and commit code on the strength
of the rest of that premise was judged the wrong side of the ambiguity to
resolve by inference — which the task itself instructs against ("Ambiguity
is not resolved by inference — it is reported and escalated"). Flagging this
explicitly as a decision a human should confirm or override, not a silent
scope-narrowing.

## 6. What could not be established

- Whether `staging.sgctech.ai` is production, another client's environment,
  a different product, or genuinely unrelated infrastructure on the same
  physical box.
- Which nginx vhost (if any) serves each hostname, and whether a
  `default_server`/catch-all exists.
- Container inventory, docker network topology, staging container's
  environment variables (including the previously-reported, still
  UNCONFIRMED `HOST=postgres-prod` claim), whether staging can resolve or
  authenticate to any production database, and what databases exist on the
  staging Postgres instance.
- Where this repo's own tooling would resolve a DB connection at runtime
  (Phase 1.12 grep never ran).

All of the above were explicitly in scope for Phase 1.4–1.12 and were not
attempted, per the stop condition.

## 7. What remains blocking, and who must decide

**Blocking: everything downstream of this verification.** No pricing-engine
work should proceed to any database step (already the existing constraint
from earlier in this engagement) until a human:

1. Confirms whether the DNS collision found in §3 is expected (e.g. both
   names are intentionally the same reverse-proxy entry point, differentiated
   only by vhost) or a genuine misconfiguration/naming collision.
2. Explicitly authorizes continuing Phase 1.4–1.12 (nginx routing through
   the authentication test), or provides the routing/topology answer
   directly if already known.
3. Separately authorizes Phase 3 (the fail-closed DB-name guard), since it
   was withheld this pass pending resolution of the ambiguity above.

**Sign-off (infrastructure owner) — to be completed by a human, not by this
process:**

Name: _______________________  Date: _______________________  Verdict accepted: ☐ Yes ☐ No, needs rework
