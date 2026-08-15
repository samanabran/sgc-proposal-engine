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
"""

ALLOWED_DB_NAME = "sgc_staging"


class DatabaseNameRejected(Exception):
    """Raised by enforce_staging_db_name on any non-exact-match or missing
    input. Callers must let this propagate -- do not catch-and-continue."""


def enforce_staging_db_name(db_name):
    """The single choke point every DB-touching path in this repo's
    tooling must call before connect/snapshot/restore/migrate/dump/seed.

    Usage:
        from db_guard import enforce_staging_db_name
        enforce_staging_db_name(db_name)   # raises on anything but "sgc_staging"
        # ... only now is it safe to open a connection / run pg_dump / etc.

    Returns the db_name unchanged on success (so it can be used inline),
    raises DatabaseNameRejected on any rejection or missing input.
    """
    if db_name is None:
        raise DatabaseNameRejected(
            f"ABORT: db_name is None (missing). Expected exactly {ALLOWED_DB_NAME!r}. "
            f"Refusing to proceed -- a check that passes on missing input manufactures "
            f"assurance, which this repo treats as worse than no check."
        )
    if not isinstance(db_name, str):
        raise DatabaseNameRejected(
            f"ABORT: db_name is not a string (got {type(db_name).__name__}: {db_name!r}). "
            f"Expected exactly {ALLOWED_DB_NAME!r}."
        )
    if db_name.strip() == "":
        raise DatabaseNameRejected(
            f"ABORT: db_name is empty or whitespace-only ({db_name!r}). "
            f"Expected exactly {ALLOWED_DB_NAME!r}."
        )
    if db_name != ALLOWED_DB_NAME:
        raise DatabaseNameRejected(
            f"REJECTED: db_name {db_name!r} is not an exact match for the only "
            f"allowlisted database ({ALLOWED_DB_NAME!r}). No prefix, substring, "
            f"or partial match is accepted -- a name merely containing "
            f"{ALLOWED_DB_NAME!r} is rejected, not approved. If this is a genuine "
            f"new target, it must be added to this allowlist deliberately, by a "
            f"human, not inferred from a similar-looking name."
        )
    return db_name
