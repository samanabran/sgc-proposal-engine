#!/usr/bin/env bash
# ci/secrets-scan.sh
#
# Scans the SDR plugin for credentials, API keys, cheque numbers, and
# non-canonical email addresses. Exit 1 on any hit.
# Run on every commit to plugins/sgc-proposal-engine/.

set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLUGIN_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

EXCLUDE_DIRS=( "ci" "tests" )

PRUNE_ARGS=""
for d in "${EXCLUDE_DIRS[@]}"; do
  PRUNE_ARGS+=" -path '$PLUGIN_ROOT/$d' -prune -o"
done

fail=0
echo "Secrets scan against $PLUGIN_ROOT"
echo "Excluding: ${EXCLUDE_DIRS[*]}"

# 1. AWS access keys
matches=$(eval "find '$PLUGIN_ROOT' $PRUNE_ARGS -type f -print" | xargs grep -nIE 'AKIA[0-9A-Z]{16}' 2>/dev/null || true)
if [[ -n "$matches" ]]; then
  echo "FAIL: AWS access key pattern (AKIA + 16 chars):"
  echo "$matches"
  fail=1
fi

# 2. Zoho refresh tokens (1000.<32-hex>.<32-hex>)
matches=$(eval "find '$PLUGIN_ROOT' $PRUNE_ARGS -type f -print" | xargs grep -nIE '1000\.[a-f0-9]{32}\.[a-f0-9]{32}' 2>/dev/null || true)
if [[ -n "$matches" ]]; then
  echo "FAIL: Zoho refresh token pattern:"
  echo "$matches"
  fail=1
fi

# 3. Generic API key patterns
matches=$(eval "find '$PLUGIN_ROOT' $PRUNE_ARGS -type f -print" | xargs grep -nIE 'api[_-]?key[[:space:]]*[:=][[:space:]]*['\''\"]?[A-Za-z0-9]{20,}' 2>/dev/null || true)
if [[ -n "$matches" ]]; then
  echo "FAIL: generic API key pattern:"
  echo "$matches"
  fail=1
fi

# 4. whsec_ keys other than the test placeholder
matches=$(eval "find '$PLUGIN_ROOT' $PRUNE_ARGS -type f -print" | xargs grep -nIE 'whsec_[A-Za-z0-9]+' 2>/dev/null | grep -v 'whsec_test_0000' || true)
if [[ -n "$matches" ]]; then
  echo "FAIL: whsec_ key other than the test placeholder:"
  echo "$matches"
  fail=1
fi

# 5. Long digit runs (cheque numbers) — 8+ consecutive digits
matches=$(eval "find '$PLUGIN_ROOT' $PRUNE_ARGS -type f -print" | xargs grep -nIE '[0-9]{8,}' 2>/dev/null || true)
# Allow long digits if they're in license/version/timestamp patterns (e.g. 604823000000000141, 20260804, 1.0.0)
filtered=$(echo "$matches" | grep -vE '(6048230000000001[0-9]{2}|0\.[0-9]+\.[0-9]+|version|sha256|timestamp|expires_at|G53|file_id|request_id|2026[0-9]{4})' || true)
if [[ -n "$filtered" ]]; then
  echo "FAIL: long digit run (possible cheque number / PII):"
  echo "$filtered"
  fail=1
fi

# 6. Plain-text email addresses. The allowed list:
#    - hello@sgctech.ai (SGC's general contact, per legal-identity.yaml)
#    - notifications@zohosign.com (Zoho Sign default FROM, surfaced as a warning)
#    - hello@scholarixglobal.com (Zoho Sign branded FROM target, not yet verified)
#    Any other email is a PII leak.
matches=$(eval "find '$PLUGIN_ROOT' $PRUNE_ARGS -type f -print" | xargs grep -nIE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' 2>/dev/null | grep -vE '(hello@sgctech\.ai|notifications@zohosign\.com|hello@scholarixglobal\.com)' || true)
if [[ -n "$matches" ]]; then
  echo "FAIL: non-allow-listed email address (only hello@sgctech.ai, notifications@zohosign.com, hello@scholarixglobal.com are allowed):"
  echo "$matches"
  fail=1
fi

if [[ $fail -ne 0 ]]; then
  echo ""
  echo "Secrets gate: FAIL"
  exit 1
fi

echo ""
echo "Secrets gate: PASS"
exit 0
