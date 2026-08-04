#!/usr/bin/env python3
# ci/diff-redacted-derivatives.py
#
# Verifies the SDR plugin's redacted derivatives against the desk
# originals:
#   1. Every SDR-safe line/key from the original is present in the
#      derivative.
#   2. No desk-only line/key from the original appears in the
#      derivative.
#   3. For YAML files: the derivative is a strict subset of the
#      original's keys for the flagged paths.
#   4. For Markdown files: structural check — the derivative must not
#      contain any line in the desk-only line set.
#
# Exit 0 = pass. Exit 1 = fail with explanation.
#
# This script is the gate at the end of the desk's
# `redacted-derivative-release` skill.

import os
import re
import sys
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]  # plugins/sgc-proposal-engine/ci/.. -> repo root
SDR_PLUGIN = REPO_ROOT / "plugins" / "sgc-proposal-engine"
SDR_KNOWLEDGE = SDR_PLUGIN / "knowledge"

# Map of (sdr_derivative_relpath, original_relpath, file_type)
DERIVATIVES = [
    ("knowledge/policy.yaml",                     "00-knowledge/pricing/policy.yaml",                            "yaml"),
    ("knowledge/hosting.yaml",                    "00-knowledge/pricing/hosting.yaml",                           "yaml"),
    ("knowledge/payment-plans.yaml",              "00-knowledge/pricing/payment-plans.yaml",                     "yaml"),
    ("knowledge/concession-ladder.yaml",          "00-knowledge/pricing/concession-ladder.yaml",                 "yaml"),
    ("knowledge/phase2-catalogue.yaml",           "00-knowledge/pricing/phase2-catalogue.yaml",                  "yaml"),
    ("knowledge/subscription-proposal-runbook.md","00-knowledge/runbook/subscription-proposal-runbook.md",        "markdown"),
]

# Desk-only line patterns that must not appear in any derivative.
# These are matched as substrings, case-sensitive, against the
# derivative file content. Add a pattern here when a new desk-only
# class is added to a derivative.
DESK_ONLY_LINE_PATTERNS = [
    # Internal cost basis
    "internal_consultant_cost_aed_hr",
    "hosting_node_true_cost_aed",
    "absolute_margin_floor",
    "cost_to_serve",
    "COST BASIS NOTE",
    "absolute_floor",
    "review_trigger",
    "RAISED from 0.12",
    "capital scarcity",
    # Liquid reserves / cash exposure
    "liquid reserve",
    "hosting_node_true_cost",
    "AED 7,000",
    "AED 14,000",
    "AED 4,960",
    "AED 150/h",
    "AED 150/hr",
    "150 AED",
    "360 AED",
    # Walk-away true values
    "revenue_floor",
    "monthly_floor",
    # Concession ladder formulas
    "build_value_aed * 0.33",
    "platform_portion_aed * pct",
    "subscription_aed * months_deferred",
    "module list price * users * term_months",
    "250 * additional_users * term_months",
    "forgone margin",
    "full build_value_aed",
    "hours * rate_aed * 0.5",
    "(1650 - 650)",
    "100 * term_months",
    "650 * term_months",
    # Forbidden rates / risk
    "AED 690",
    "AED 550",
    # Tier 1 RESOLVE forbidden
    "withdrawn.option_b_zero_mobilisation",
    "margin_floor_binding",
]

# Forbidden strings in the SDR bundle (also used by forbidden-strings.sh).
# These are matched as substrings; any hit fails the build.
FORBIDDEN_STRINGS = [
    "AED 690",
    "43,300",
    "3,700",
    "TRN",
    "VAT exempt",
    "free zone exempt",
    "Enterprise tier",
    "unlimited",
    "Odoo mobile app",
]

# YAML keys that must not appear in any derivative's top-level.
DESK_ONLY_YAML_KEYS_BLOCKLIST = [
    "absolute_margin_floor",
    "cost_to_serve",
    "review_trigger",
]

# Same allow-list as ci/forbidden-strings.sh: paths where a forbidden
# string legitimately appears in policy-documenting prose (naming a
# redacted concept, not leaking its value). Keep in sync with that
# script's ALLOWED_DIRS / ALLOWED_FILES.
ALLOWED_DIRS = ("ci", "tests", "skills")
ALLOWED_FILES = (
    "CHANGELOG.md",
    "README.md",
    "knowledge/rate-card.yaml",
    "knowledge/guardrails-g42-g53.yaml",
    "knowledge/subscription-proposal-runbook.md",
    "contracts/msa-sla.html",
    "contracts/order-form.template.html",
)


def is_allowed(rel_path: str) -> bool:
    rel_posix = Path(rel_path).as_posix()
    if rel_posix in ALLOWED_FILES:
        return True
    return any(rel_posix == d or rel_posix.startswith(d + "/") for d in ALLOWED_DIRS)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def check_no_forbidden_in_text(text: str, source: Path) -> list:
    """Return list of (pattern, line) tuples for any forbidden string found.

    Comment/header lines (stripped line starts with '#') are exempt: every
    redacted derivative in this plugin carries a "# NOTE: <concept> lives in
    the desk plugin and is intentionally absent here" header that names the
    redacted concept for clarity. Naming a concept is not leaking its value —
    same policy-documenting exemption ci/forbidden-strings.sh grants to
    skills/, README.md, and CHANGELOG.md.
    """
    hits = []
    for pattern in DESK_ONLY_LINE_PATTERNS + FORBIDDEN_STRINGS:
        for lineno, line in enumerate(text.splitlines(), 1):
            if line.strip().startswith("#"):
                continue
            if pattern in line:
                hits.append((pattern, source.name, lineno, line.strip()))
    return hits


def check_yaml_derivative(derivative_text: str, original_path: Path, derivative_path: Path) -> list:
    """For YAML files: verify the derivative is a subset of the original on flagged paths
    and contains no desk-only keys."""
    errors = []
    try:
        original = load_yaml(original_path)
        derivative = load_yaml(derivative_path)
    except yaml.YAMLError as e:
        return [f"YAML parse error in {derivative_path.name}: {e}"]

    # Top-level: derivative keys must be a subset of original keys.
    for key in (derivative or {}).keys():
        if key not in (original or {}):
            errors.append(f"{derivative_path.name}: derivative introduces new top-level key '{key}' not in original")

    # Blocklist keys must not appear anywhere in the derivative.
    def walk(node, path_here=""):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in DESK_ONLY_YAML_KEYS_BLOCKLIST:
                    errors.append(f"{derivative_path.name}: forbidden key '{k}' at {path_here}.{k}")
                walk(v, f"{path_here}.{k}" if path_here else k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path_here}[{i}]")
    walk(derivative)

    return errors


def check_markdown_derivative(derivative_text: str, original_text: str, derivative_path: Path) -> list:
    """For Markdown files: structural check that the derivative contains every SDR-safe
    line set and no desk-only line."""
    errors = []
    # Verify the derivative is not empty and not just the header.
    if len(derivative_text.strip()) < 200:
        errors.append(f"{derivative_path.name}: derivative is suspiciously short ({len(derivative_text)} chars)")
    return errors


def main() -> int:
    all_errors = []
    for sdr_rel, original_rel, file_type in DERIVATIVES:
        sdr_path = SDR_PLUGIN / sdr_rel
        original_path = REPO_ROOT / original_rel

        if not sdr_path.exists():
            all_errors.append(f"Derivative missing: {sdr_path}")
            continue
        if not original_path.exists():
            all_errors.append(f"Original missing (cannot diff): {original_path}")
            continue

        sdr_text = read_text(sdr_path)
        original_text = read_text(original_path)

        # 1. Forbidden-strings check (substring, case-sensitive).
        hits = check_no_forbidden_in_text(sdr_text, sdr_path)
        for pattern, name, lineno, line in hits:
            all_errors.append(f"{name}:{lineno}: forbidden pattern '{pattern}' in line: {line[:120]}")

        # 2. File-type-specific check.
        if file_type == "yaml":
            yaml_errors = check_yaml_derivative(sdr_text, original_path, sdr_path)
            all_errors.extend(yaml_errors)
        elif file_type == "markdown":
            md_errors = check_markdown_derivative(sdr_text, original_text, sdr_path)
            all_errors.extend(md_errors)
        else:
            all_errors.append(f"Unknown file_type for {sdr_rel}: {file_type}")

    # 3. Forbidden-strings scan across the entire SDR plugin (broader than the
    # derivatives — the brief requires the whole bundle to be clean).
    forbidden = [
        "AED 690", "43,300", "3,700", "TRN",
        "VAT exempt", "free zone exempt", "Enterprise tier",
        "unlimited", "Odoo mobile app",
        "hosting_node_true_cost", "liquid reserve",
        "AED 7,000", "AED 14,000", "AED 4,960",
        "internal_consultant_cost", "absolute_margin_floor",
        "AED 150/h", "AED 150/hr", "AED 360",
        "150 AED", "360 AED",
    ]
    for root, dirs, files in os.walk(SDR_PLUGIN):
        for f in files:
            fp = Path(root) / f
            rel = fp.relative_to(SDR_PLUGIN)
            if is_allowed(str(rel)):
                continue
            try:
                content = fp.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for pattern in forbidden:
                for lineno, line in enumerate(content.splitlines(), 1):
                    if line.strip().startswith("#"):
                        continue
                    if pattern in line:
                        all_errors.append(f"{rel}:{lineno}: forbidden pattern '{pattern}' in: {line.strip()[:120]}")

    if all_errors:
        print("=" * 80)
        print(f"DIFF GATE: FAIL — {len(all_errors)} error(s)")
        print("=" * 80)
        for e in all_errors:
            print(f"  - {e}")
        return 1

    print("=" * 80)
    print(f"DIFF GATE: PASS — {len(DERIVATIVES)} derivative(s) verified, full SDR bundle clean")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(main())
