#!/usr/bin/env bash
# ci/forbidden-strings.sh
#
# Scans the SDR plugin for any forbidden string. The list is split
# into two tiers, both gated by the same path allow-list:
#
#   - "strict" patterns: desk-only internals (cost-to-serve, margin
#     floor, liquid reserve, desk-only AED figures). Any hit outside
#     the policy-documenting contexts fails the build.
#
#   - "policy" patterns: forbidden rate-card figures and forbidden
#     tax/vat claims that the rate card and the policy documentation
#     legitimately mention. Any hit outside the policy-documenting
#     contexts fails the build.
#
# Policy-documenting contexts (where any forbidden string may appear):
#   - ci/, tests/ (gate logic and test logic)
#   - skills/ (policy documentation)
#   - CHANGELOG.md, README.md (release notes and plugin description)
#   - knowledge/rate-card.yaml (forbidden_rates block is by design)
#   - knowledge/guardrails-g42-g53.yaml (gate definitions list the strings)
#   - knowledge/subscription-proposal-runbook.md (redacted derivative may
#     reference the strings in policy context)
#
# Run on every commit to plugins/sgc-proposal-engine/.

set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLUGIN_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Strict patterns: desk-only internals. Any hit outside the
# policy-documenting contexts fails the build.
STRICT_PATTERNS=(
  "43,300"
  "3,700"
  "hosting_node_true_cost"
  "liquid reserve"
  "AED 7,000"
  "AED 14,000"
  "AED 4,960"
  "internal_consultant_cost"
  "absolute_margin_floor"
  "AED 150/h"
  "AED 150/hr"
  "AED 360"
  "150 AED"
  "360 AED"
)

# Policy patterns: forbidden rate-card figures and forbidden
# tax/vat claims. Same allow-list applies.
POLICY_PATTERNS=(
  "AED 690"
  "AED 550"
  "TRN"
  "VAT exempt"
  "free zone exempt"
  "Enterprise tier"
  "unlimited"
  "AWS"
  "Odoo mobile app"
)

# Directories where any forbidden string is allowed (policy documentation).
ALLOWED_DIRS=(
  "ci"
  "tests"
  "skills"
)

# Files where any forbidden string is allowed (regardless of directory).
ALLOWED_FILES=(
  "CHANGELOG.md"
  "README.md"
  "knowledge/rate-card.yaml"
  "knowledge/guardrails-g42-g53.yaml"
  "knowledge/subscription-proposal-runbook.md"
  "contracts/msa-sla.html"
  "contracts/order-form.template.html"
)

is_allowed() {
  local rel_path="$1"
  for allowed in "${ALLOWED_FILES[@]}"; do
    if [[ "$rel_path" == "$allowed" ]]; then
      return 0
    fi
  done
  for allowed_dir in "${ALLOWED_DIRS[@]}"; do
    if [[ "$rel_path" == "$allowed_dir"/* ]] || [[ "$rel_path" == "$allowed_dir" ]]; then
      return 0
    fi
  done
  return 1
}

fail=0
echo "Forbidden-strings scan against $PLUGIN_ROOT"
echo ""

scan_patterns() {
  local label="$1"; shift
  local pattern
  for pattern in "$@"; do
    matches=$(grep -RIn --include='*' --exclude-dir='.git' -- "$pattern" "$PLUGIN_ROOT" 2>/dev/null || true)
    if [[ -n "$matches" ]]; then
      bad=$(echo "$matches" | while IFS= read -r line; do
        file_path="$(echo "$line" | sed -E 's|^([^:]+):.*|\1|')"
        rel="${file_path#$PLUGIN_ROOT/}"
        if ! is_allowed "$rel"; then
          echo "$line"
        fi
      done)
      if [[ -n "$bad" ]]; then
        echo "FAIL: $label forbidden pattern '$pattern' found outside policy-allowed contexts:"
        echo "$bad"
        fail=1
      fi
    fi
  done
}

scan_patterns "STRICT" "${STRICT_PATTERNS[@]}"
scan_patterns "POLICY" "${POLICY_PATTERNS[@]}"

if [[ $fail -ne 0 ]]; then
  echo ""
  echo "Forbidden-strings gate: FAIL"
  exit 1
fi

echo ""
echo "Forbidden-strings gate: PASS"
exit 0
