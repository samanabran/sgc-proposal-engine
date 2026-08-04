#!/usr/bin/env python3
"""SGC Proposal Engine — agent helper.

Subcommands:
  root                  Resolve and print the engine root (env -> cwd walk-up -> default).
  clients               List client folders with their pipeline stage (from manifest.yaml).
  scaffold <name>       Scaffold a new client folder from 02-clients/_SCAFFOLD.
  validate <client>     Run 05-ops/validate.py on a client; annotate check-14 semantics.
  stage <client>        Print the client's manifest stage + the next required action.

Stdlib only (no PyYAML dependency). Engine contract lives in AGENTS.md; this script only
handles the mechanical parts — the LLM performs the pipeline itself.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_ROOT = Path(r"C:\sgc_proposal_engine")
ENV_VAR = "SGC_PROPOSAL_ENGINE"
REQUIRED_DIRS = ("00-knowledge", "02-clients", "05-ops")


def resolve_root() -> Path | None:
    """Resolution order: env var -> walk up from cwd -> default."""
    env = os.environ.get(ENV_VAR)
    candidates: list[Path] = []
    if env:
        candidates.append(Path(env))
    cwd = Path.cwd()
    for ancestor in (cwd, *cwd.parents):
        if (ancestor / "AGENTS.md").is_file() and (ancestor / "02-clients").is_dir():
            candidates.append(ancestor)
            break
    candidates.append(DEFAULT_ROOT)

    for cand in candidates:
        if (cand / "AGENTS.md").is_file() and all((cand / d).is_dir() for d in REQUIRED_DIRS):
            return cand.resolve()
    return None


def die(msg: str, code: int = 1) -> None:
    print(f"engine: error: {msg}", file=sys.stderr)
    sys.exit(code)


def read_manifest_field(client_dir: Path, field: str) -> str | None:
    """Naive key: value extraction from manifest.yaml (no PyYAML)."""
    manifest = client_dir / "manifest.yaml"
    if not manifest.is_file():
        return None
    for line in manifest.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(rf"^\s*{re.escape(field)}\s*:\s*(.*?)\s*$", line)
        if m:
            # strip trailing inline YAML comment (e.g. "draft  # intake | calc | ...")
            return m.group(1).split("#", 1)[0].strip()
    return None


def list_clients(root: Path) -> list[Path]:
    clients = root / "02-clients"
    if not clients.is_dir():
        return []
    return sorted(
        p for p in clients.iterdir()
        if p.is_dir() and p.name != "_SCAFFOLD" and (p / "manifest.yaml").is_file()
    )


def cmd_root(root: Path) -> None:
    print(root)


def cmd_clients(root: Path) -> None:
    clients = list_clients(root)
    if not clients:
        print("No client folders with manifest.yaml found.")
        return
    for c in clients:
        stage = read_manifest_field(c, "stage") or "?"
        gates = read_manifest_field(c, "gates_passed") or "?"
        print(f"{c.name:45s} stage={stage:14s} gates_passed={gates}")


def cmd_scaffold(root: Path, name: str) -> None:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name):
        die(f"invalid client name {name!r} (letters/digits/._- only, no spaces). "
            "Follow 05-ops/naming-conventions.md (e.g. MRD-meridianview-realty).")
    scaffold = root / "02-clients" / "_SCAFFOLD"
    target = root / "02-clients" / name
    if not scaffold.is_dir():
        die(f"_SCAFFOLD not found at {scaffold}")
    if target.exists():
        die(f"client folder already exists: {target}")
    shutil.copytree(scaffold, target)
    print(f"scaffolded {target}")
    print("next: fill 00-intake/client-brief.yaml (Stage 1 intake).")


def cmd_validate(root: Path, client: str) -> None:
    client_dir = root / "02-clients" / client
    if not client_dir.is_dir():
        die(f"client folder not found: {client_dir}")
    validate_py = root / "05-ops" / "validate.py"
    if not validate_py.is_file():
        die(f"validate.py not found: {validate_py}")
    print(f"running: python {validate_py} {client_dir}")
    proc = subprocess.run(
        [sys.executable, str(validate_py), str(client_dir)],
        capture_output=True, text=True,
    )
    if proc.stdout:
        print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    print(f"validate.py exit code: {proc.returncode}")
    if proc.returncode == 0:
        print("clean: proceed to human review / issue.")
    else:
        print("validate.py reported a FAILURE — fix the listed issues and re-run; do not proceed.")
    if "entity resolution" in proc.stdout or "BLOCKED" in proc.stdout:
        print(
            "NOTE check 14 (entity/legal-identity.yaml): reported BLOCKED-by-design until real "
            "entity facts are supplied by Commercial Desk. It blocks ISSUE (administratively), "
            "NOT the commercial gate. Do not issue until resolved; log an escalation in "
            "manifest.yaml and flag it to the human."
        )
    sys.exit(proc.returncode)


def cmd_stage(root: Path, client: str) -> None:
    client_dir = root / "02-clients" / client
    if not client_dir.is_dir():
        die(f"client folder not found: {client_dir}")
    manifest = client_dir / "manifest.yaml"
    if not manifest.is_file():
        die(f"no manifest.yaml at {client_dir} — scaffold it first")
    stage = read_manifest_field(client_dir, "stage") or "intake"
    gates = read_manifest_field(client_dir, "gates_passed")
    walkaway = read_manifest_field(client_dir, "walkaway_card_produced")
    print(f"client:       {client}")
    print(f"stage:        {stage}")
    print(f"gates_passed: {gates or 'not set'}")
    print(f"walkaway_card_produced: {walkaway or 'not set'}")
    next_actions = {
        "intake": "Stage 2 risk assessment -> 02-calc/risk-assessment.yaml",
        "risk_assessed": "Stage 3 calc -> complete 02-calc/pricing-worksheet.yaml",
        "calc": "Stage 4 exposure + walk-away card (G21/G22) -> 02-calc/deal-card.md",
        "draft": "Stage 7 QA checklists + run validate.py before human review",
        "review": "run validate.py, then Stage 8 human review (no self-approval)",
        "issued": "deal issued; further changes = new revision (05-issued is immutable)",
    }
    print(f"next:         {next_actions.get(stage, 'read 00-knowledge/runbook for next stage')}")


def main() -> None:
    root = resolve_root()
    if root is None:
        die("engine root unreachable (no AGENTS.md + 02-clients found). Set "
            f"{ENV_VAR} or run from inside the engine repo.")
    args = sys.argv[1:]
    cmd = args[0] if args else "root"
    if cmd == "root":
        cmd_root(root)
    elif cmd == "clients":
        cmd_clients(root)
    elif cmd == "scaffold":
        if len(args) < 2:
            die("usage: engine.py scaffold <client-name>")
        cmd_scaffold(root, args[1])
    elif cmd == "validate":
        if len(args) < 2:
            die("usage: engine.py validate <client-name>")
        cmd_validate(root, args[1])
    elif cmd == "stage":
        if len(args) < 2:
            die("usage: engine.py stage <client-name>")
        cmd_stage(root, args[1])
    else:
        die(f"unknown command {cmd!r} (root|clients|scaffold|validate|stage)")


if __name__ == "__main__":
    main()
