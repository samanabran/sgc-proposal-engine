#!/usr/bin/env python3
"""
Fail-closed database-name guard for SGC pricing-engine tooling.

Context: the staging-isolation verification pass (2026-08-16, see
00-intake/staging-isolation-verification-2026-08-16.md) found staging
Odoo (odoo19-sgc-staging) configured with HOST=postgres-prod, on the same
docker network as production, and reachable to production's Postgres over
the network. No file under 05-ops/ currently resolves a database
connection at all -- the pricing engine is flat-file (pricing_engine.py +
YAML). This guard exists so that changes clearly, the moment ANY future
code in 05-ops/ tries to connect, snapshot, restore, migrate, dump, or
seed a database, it cannot silently resolve to anything but the one
allowlisted staging database name -- regardless of what environment
variables, config files, or docker network state say at the time.

This guard does not depend on network topology being correct. That is its
entire purpose: it holds even if someone re-attaches the staging container
to the production network again.

RULE: exact string equality only. No prefix, substring, glob, or regex
match. "sgc_staging_old" is rejected. "staging" is rejected. A name that
merely CONTAINS the allowlisted string is rejected, not accepted.

RULE: fail closed. Missing, empty, or unreadable input aborts. A check
that passes on missing data manufactures assurance -- this repo has
already produced that exact defect twice (see PART 9 fixes in
05-ops/validate.py, commits fcfeda4 and 5b66ad6).

SUPERSEDED (2026-08-16 follow-up): the original enforce_staging_db_name(db_name)
checked database name only. The isolation follow-up pass established, with
direct evidence (odoo.conf: dbfilter = ^sgc_staging$; no db_host override;
staging container env: HOST=postgres-prod; postgres-prod resolves inside
staging to 172.19.0.2, the SAME address as production's odoo-prod-db), that
the database named "sgc_staging" is NOT hosted on a separate staging
Postgres instance -- it lives on production's own Postgres server. A
name-only guard passes cleanly on this exact database while pointing
straight at the host it exists to protect against: validating the right
value on the wrong dimension, the same manufactured-assurance failure class
already fixed twice in validate.py (fail-open / fail-closed-out-of-scope).
enforce_staging_db_name is REMOVED, not kept as a compatibility wrapper --
a name-only check that still exists and still passes would be worse than no
guard, since it would look protective while remaining exploitable exactly
the way the original bug was. Use enforce_staging_db_pair(host, db_name).

ALLOWED_DB_HOST is deliberately left unset (None) below. No verified-safe,
dedicated staging Postgres host currently exists in this environment (see
00-intake/staging-isolation-verification-2026-08-16.md addendum) -- the
only host staging's Odoo config actually uses is postgres-prod, which is
production. Fabricating a placeholder "safe" hostname here would be
guessing, which RULE 1 of this engagement forbids. With ALLOWED_DB_HOST
unset, enforce_staging_db_pair() fails closed on EVERY call until a human
completes remediation (see verification doc §7) and sets this value
deliberately to the real, dedicated staging host that results from it.
"""

ALLOWED_DB_NAME = "sgc_staging"
ALLOWED_DB_HOST = None  # deliberately unset -- see module docstring

# HARD DENYLIST -- checked before anything else, unconditionally, and NOT
# overridable by setting ALLOWED_DB_HOST to one of these values. These are
# the exact identifiers the 2026-08-16 isolation pass confirmed point at
# production: the env var value staging's own Odoo config actually uses
# (postgres-prod), the production Postgres container's real name
# (odoo-prod-db), and the IP that name resolves to on the shared docker
# network (172.19.0.2). The most likely mistake once this tooling is
# unfrozen is someone pasting in the value they see in the staging env var
# as if it were the fix -- that is precisely the one input this guard must
# refuse outright, deliberately or not.
DENIED_HOSTS = frozenset({"postgres-prod", "odoo-prod-db", "172.19.0.2"})


class DatabaseNameRejected(Exception):
    """Raised by enforce_staging_db_pair on any non-exact-match or missing
    input, on either host or database name. Callers must let this
    propagate -- do not catch-and-continue."""


def _require_nonempty_str(value, label, expected):
    if value is None:
        raise DatabaseNameRejected(
            f"ABORT: {label} is None (missing). Expected exactly {expected!r}. "
            f"Refusing to proceed -- a check that passes on missing input manufactures "
            f"assurance, which this repo treats as worse than no check."
        )
    if not isinstance(value, str):
        raise DatabaseNameRejected(
            f"ABORT: {label} is not a string (got {type(value).__name__}: {value!r}). "
            f"Expected exactly {expected!r}."
        )
    if value.strip() == "":
        raise DatabaseNameRejected(
            f"ABORT: {label} is empty or whitespace-only ({value!r}). "
            f"Expected exactly {expected!r}."
        )
    return value


def enforce_staging_db_pair(host, db_name):
    """The single choke point every DB-touching path in this repo's
    tooling must call before connect/snapshot/restore/migrate/dump/seed.
    Requires BOTH host and db_name to exactly match the allowlisted pair --
    a correct db_name on the wrong host is REJECTED, not passed, because
    that is precisely the real-world scenario this guard exists to catch
    (see module docstring: sgc_staging on postgres-prod).

    Usage:
        from db_guard import enforce_staging_db_pair
        enforce_staging_db_pair(host, db_name)   # raises unless both match
        # ... only now is it safe to open a connection / run pg_dump / etc.

    Returns (host, db_name) unchanged on success, raises
    DatabaseNameRejected on any rejection or missing input on either side.
    """
    _require_nonempty_str(db_name, "db_name", ALLOWED_DB_NAME)
    _require_nonempty_str(host, "host", ALLOWED_DB_HOST)

    if host in DENIED_HOSTS:
        raise DatabaseNameRejected(
            f"ABORT: host {host!r} is on the hard denylist {sorted(DENIED_HOSTS)} "
            f"and is refused unconditionally -- this is not affected by "
            f"ALLOWED_DB_HOST and cannot be bypassed by setting ALLOWED_DB_HOST "
            f"to this value. {host!r} is confirmed (2026-08-16 isolation pass) "
            f"to be, or resolve to, production's Postgres server. If staging "
            f"gets its own dedicated host later, that new host will not be on "
            f"this list -- this denylist exists specifically to catch the "
            f"known-dangerous values, not as a general substitute for the "
            f"allowlist below."
        )

    if ALLOWED_DB_HOST is None:
        raise DatabaseNameRejected(
            f"ABORT: no verified-safe staging Postgres host is configured "
            f"(ALLOWED_DB_HOST is unset). The isolation verification pass "
            f"(2026-08-16) found that database {ALLOWED_DB_NAME!r} currently "
            f"lives on production's Postgres instance, not a separate "
            f"staging host -- there is no safe value to allowlist yet. "
            f"Refusing every connection attempt until a human completes "
            f"remediation (00-intake/staging-isolation-verification-2026-08-16.md "
            f"section 7) and sets ALLOWED_DB_HOST deliberately."
        )

    if host != ALLOWED_DB_HOST or db_name != ALLOWED_DB_NAME:
        raise DatabaseNameRejected(
            f"REJECTED: (host={host!r}, db_name={db_name!r}) is not an exact "
            f"match for the only allowlisted pair "
            f"(host={ALLOWED_DB_HOST!r}, db_name={ALLOWED_DB_NAME!r}). "
            f"No prefix, substring, or partial match is accepted on either "
            f"field -- a correct database name on the wrong host is rejected, "
            f"not approved, and so is the reverse. If this is a genuine new "
            f"target, it must be added to this allowlist deliberately, by a "
            f"human, not inferred from a similar-looking name or host."
        )
    return (host, db_name)
