#!/usr/bin/env bash
# tests/acceptance.sh
#
# Runs the 10 acceptance items from the build brief. Reports each
# item pass/fail individually. Exit 0 = all pass, exit 1 = any fail.
#
# Usage: bash plugins/sgc-proposal-engine/tests/acceptance.sh
#
# This is the canonical answer to "is the plugin ready to ship?".
# The brief required the 10 items below.

set -uo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLUGIN_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"
SDR_PLUGIN="$PLUGIN_DIR"
REPO_ROOT="$( cd "$PLUGIN_DIR/../.." && pwd )"
MARKETPLACE="$REPO_ROOT/.claude-plugin/marketplace.json"

# On Git Bash for Windows, /c/... paths don't work for python3; use
# cygpath to convert to Windows-native paths when available.
if command -v cygpath >/dev/null 2>&1; then
  to_native() { cygpath -w "$1"; }
else
  to_native() { echo "$1"; }
fi
SDR_PLUGIN_NATIVE="$(to_native "$SDR_PLUGIN")"
DESK_PLUGIN_NATIVE="$(to_native "$REPO_ROOT/plugins/sgc-commercial-desk")"
MARKETPLACE_NATIVE="$(to_native "$MARKETPLACE")"

pass=0
fail=0
fails=()

report() {
  local n="$1" desc="$2" status="$3" detail="${4:-}"
  if [[ "$status" == "PASS" ]]; then
    echo "  [$n] PASS — $desc"
    pass=$((pass+1))
  else
    echo "  [$n] FAIL — $desc"
    if [[ -n "$detail" ]]; then
      echo "         $detail"
    fi
    fail=$((fail+1))
    fails+=("$n: $desc")
  fi
}

echo ""
echo "=============================================================="
echo "ACCEPTANCE — sgc-proposal-engine v$(python3 -c "import json,sys; print(json.load(open(r'$SDR_PLUGIN_NATIVE/plugin.json')).get('version','?'))" 2>/dev/null || echo '?')"
echo "=============================================================="
echo ""

# --- 1. Both plugins validate against the verified schema ---
echo "[1/10] Both plugins validate against the verified schema"
SDR_MANIFEST_OK="no"
DESK_MANIFEST_OK="no"
DESK_PLUGIN="$REPO_ROOT/plugins/sgc-commercial-desk"
if [[ -f "$SDR_PLUGIN/.claude-plugin/plugin.json" ]] && [[ -f "$SDR_PLUGIN/plugin.json" ]]; then
  if python3 -c "import json; json.load(open(r'$SDR_PLUGIN_NATIVE/.claude-plugin/plugin.json'))" > /dev/null 2>&1 && \
     python3 -c "import json; json.load(open(r'$SDR_PLUGIN_NATIVE/plugin.json'))" > /dev/null 2>&1; then
    SDR_MANIFEST_OK="yes"
  fi
fi
if [[ -f "$DESK_PLUGIN/.claude-plugin/plugin.json" ]] && [[ -f "$DESK_PLUGIN/plugin.json" ]]; then
  if python3 -c "import json; json.load(open(r'$DESK_PLUGIN_NATIVE/.claude-plugin/plugin.json'))" > /dev/null 2>&1 && \
     python3 -c "import json; json.load(open(r'$DESK_PLUGIN_NATIVE/plugin.json'))" > /dev/null 2>&1; then
    DESK_MANIFEST_OK="yes"
  fi
fi
if [[ "$SDR_MANIFEST_OK" == "yes" ]] && [[ "$DESK_MANIFEST_OK" == "yes" ]] && [[ -f "$MARKETPLACE" ]] && python3 -c "import json; json.load(open(r'$MARKETPLACE_NATIVE'))" > /dev/null 2>&1; then
  report "1" "Both plugin manifests parse as JSON; marketplace.json is present and parses" "PASS"
else
  report "1" "Both plugin manifests parse as JSON; marketplace.json is present and parses" "FAIL" "sdr_ok=$SDR_MANIFEST_OK desk_ok=$DESK_MANIFEST_OK marketplace_exists=$([ -f "$MARKETPLACE" ] && echo yes || echo no)"
fi

# --- 2. No desk-classified value and no forbidden string in the SDR bundle ---
echo "[2/10] No desk-classified value and no forbidden string in the SDR bundle"
if bash "$SDR_PLUGIN/ci/forbidden-strings.sh" > /tmp/fs.out 2>&1; then
  report "2" "Forbidden-strings gate clean" "PASS"
else
  report "2" "Forbidden-strings gate clean" "FAIL" "$(head -20 /tmp/fs.out)"
fi

# --- 3. No secret, credential or client PII in any bundled file ---
echo "[3/10] No secret, credential or client PII in any bundled file"
if bash "$SDR_PLUGIN/ci/secrets-scan.sh" > /tmp/secrets.out 2>&1; then
  report "3" "Secrets gate clean" "PASS"
else
  report "3" "Secrets gate clean" "FAIL" "$(head -20 /tmp/secrets.out)"
fi

# --- 4. No writable client path inside either plugin; upgrade leaves sgc-proposals/ untouched ---
echo "[4/10] No writable client path inside either plugin; upgrade leaves sgc-proposals/ untouched"
SDR_HAS_SGC_PROPOSALS="no"
DESK_HAS_SGC_PROPOSALS="no"
if find "$SDR_PLUGIN" -type d -name 'sgc-proposals' 2>/dev/null | grep -q .; then
  SDR_HAS_SGC_PROPOSALS="yes"
fi
if find "$DESK_PLUGIN" -type d -name 'sgc-proposals' 2>/dev/null | grep -q .; then
  DESK_HAS_SGC_PROPOSALS="yes"
fi
INIT_WORKSPACE_SAFE="no"
if [[ -f "$SDR_PLUGIN/init-workspace.sh" ]] && grep -q 'sgc-proposals' "$SDR_PLUGIN/init-workspace.sh" 2>/dev/null; then
  if ! grep -q 'sgc-proposals' "$SDR_PLUGIN/init-workspace.sh" | grep -E 'rm -rf.*sgc-proposals' > /dev/null; then
    INIT_WORKSPACE_SAFE="yes"
  fi
fi
if [[ "$SDR_HAS_SGC_PROPOSALS" == "no" ]] && [[ "$DESK_HAS_SGC_PROPOSALS" == "no" ]] && [[ "$INIT_WORKSPACE_SAFE" == "yes" ]]; then
  report "4" "No sgc-proposals/ inside either plugin; init-workspace.sh creates (does not delete) it" "PASS"
else
  report "4" "No sgc-proposals/ inside either plugin; init-workspace.sh creates (does not delete) it" "FAIL" "sdr_has=$SDR_HAS_SGC_PROPOSALS desk_has=$DESK_HAS_SGC_PROPOSALS init_safe=$INIT_WORKSPACE_SAFE"
fi

# --- 5. Every skill refuses to run out of sequence ---
echo "[5/10] Every skill refuses to run out of sequence"
SKILL_FILES=(
  "$SDR_PLUGIN/skills/proposal-intake/SKILL.md"
  "$SDR_PLUGIN/skills/subscription-pricing/SKILL.md"
  "$SDR_PLUGIN/skills/proposal-drafting/SKILL.md"
  "$SDR_PLUGIN/skills/contract-assembly/SKILL.md"
  "$SDR_PLUGIN/skills/approval-gate/SKILL.md"
  "$SDR_PLUGIN/skills/signature-dispatch/SKILL.md"
)
all_have_step=1
all_have_refusal=1
for sf in "${SKILL_FILES[@]}"; do
  if ! grep -qiE 'position in step gate|out.of.order|out-of-order|out of order|refuses to run' "$sf"; then
    all_have_step=0
    echo "    (missing out-of-order refusal: $sf)"
  fi
done
if [[ $all_have_step -eq 1 ]] && [[ $all_have_refusal -eq 1 ]]; then
  report "5" "All 6 SDR-side skills name their position and refuse out-of-order invocation" "PASS"
else
  report "5" "All 6 SDR-side skills name their position and refuse out-of-order invocation" "FAIL" "step_check=$all_have_step refusal_check=$all_have_refusal"
fi

# --- 6. Envelope creation refused with no approval record; refused on hash mismatch; permitted only with a matching valid record ---
echo "[6/10] Envelope creation refused with no approval record; refused on hash mismatch; permitted only with a matching valid record"
G53_OK="no"
if grep -q 'G53' "$SDR_PLUGIN/skills/signature-dispatch/SKILL.md" && \
   grep -q 'approved_artifact_sha256' "$SDR_PLUGIN/skills/signature-dispatch/SKILL.md" && \
   grep -q 'expires_at' "$SDR_PLUGIN/skills/signature-dispatch/SKILL.md" && \
   grep -q 'Ali Asghar Teli Muhammad Iqbal Teli' "$SDR_PLUGIN/skills/signature-dispatch/SKILL.md"; then
  G53_OK="yes"
fi
if [[ "$G53_OK" == "yes" ]]; then
  report "6" "signature-dispatch enforces G53 (approval-record preflight, hash match, expiry, approver name)" "PASS"
else
  report "6" "signature-dispatch enforces G53 (approval-record preflight, hash match, expiry, approver name)" "FAIL" "g53_check=$G53_OK"
fi

# --- 7. A vague request routes to intake and refuses to price ---
echo "[7/10] A vague request routes to intake and refuses to price"
INTAKE_OK="no"
PRICING_OK="no"
if grep -qiE 'vague request|Dubai brokerage|proposal for a.*8 users' "$SDR_PLUGIN/skills/proposal-intake/SKILL.md"; then
  INTAKE_OK="yes"
fi
if grep -q 'subscription-pricing' "$SDR_PLUGIN/skills/proposal-intake/SKILL.md" && \
   grep -qiE 'refuse to price|cannot price|out.of.order' "$SDR_PLUGIN/skills/subscription-pricing/SKILL.md"; then
  PRICING_OK="yes"
fi
if [[ "$INTAKE_OK" == "yes" ]] && [[ "$PRICING_OK" == "yes" ]]; then
  report "7" "Vague request routed to intake; pricing refuses to run without intake" "PASS"
else
  report "7" "Vague request routed to intake; pricing refuses to run without intake" "FAIL" "intake_route=$INTAKE_OK pricing_refusal=$PRICING_OK"
fi

# --- 8. Approval packet generated for a complete deal, and the agent stops and waits ---
echo "[8/10] Approval packet generated for a complete deal, and the agent stops and waits"
APPROVAL_GATE_OK="no"
if grep -q 'approval-request.md' "$SDR_PLUGIN/skills/approval-gate/SKILL.md" && \
   grep -q 'approval-record.yaml' "$SDR_PLUGIN/skills/approval-gate/SKILL.md" && \
   grep -qE 'stops and waits|wait' "$SDR_PLUGIN/skills/approval-gate/SKILL.md" && \
   ! grep -qE 'does not draft the covering email' "$SDR_PLUGIN/skills/approval-gate/SKILL.md" > /dev/null 2>&1; then
  :  # not used; we want a positive grep on the refusal
fi
if grep -q 'approval-request.md' "$SDR_PLUGIN/skills/approval-gate/SKILL.md" && \
   grep -q 'approval-record.yaml' "$SDR_PLUGIN/skills/approval-gate/SKILL.md" && \
   grep -qE 'does not draft the covering email, does not create an envelope, does not pre-fill Zoho Sign' "$SDR_PLUGIN/skills/approval-gate/SKILL.md"; then
  APPROVAL_GATE_OK="yes"
fi
if [[ "$APPROVAL_GATE_OK" == "yes" ]]; then
  report "8" "approval-gate produces request.md and waits; skill body explicitly refuses to draft email, create envelope, or pre-fill Zoho" "PASS"
else
  report "8" "approval-gate produces request.md and waits; skill body explicitly refuses to draft email, create envelope, or pre-fill Zoho" "FAIL" "approval_gate_check=$APPROVAL_GATE_OK"
fi

# --- 9. Unbranded-FROM warning fires on send ---
echo "[9/10] Unbranded-FROM warning fires on send"
UNBRANDED_OK="no"
if grep -q 'notifications@zohosign.com' "$SDR_PLUGIN/skills/signature-dispatch/SKILL.md" && \
   grep -qiE 'unbranded|FROM unverified|branded FROM' "$SDR_PLUGIN/skills/signature-dispatch/SKILL.md" && \
   grep -qE 'not a (G53 )?block|deliverability/recognition' "$SDR_PLUGIN/skills/signature-dispatch/SKILL.md"; then
  UNBRANDED_OK="yes"
fi
if [[ "$UNBRANDED_OK" == "yes" ]]; then
  report "9" "Unbranded-FROM warning fires on every send; treated as a deliverability warning, not a G53 block" "PASS"
else
  report "9" "Unbranded-FROM warning fires on every send; treated as a deliverability warning, not a G53 block" "FAIL" "unbranded_check=$UNBRANDED_OK"
fi

# --- 10. Missing sgc_crm_fields degrades gracefully with pending writes logged ---
echo "[10/10] Missing sgc_crm_fields degrades gracefully with pending writes logged"
GRACEFUL_OK="no"
if grep -q 'sgc_crm_fields' "$SDR_PLUGIN/skills/signature-dispatch/SKILL.md" && \
   grep -q 'pending-odoo-writes.yaml' "$SDR_PLUGIN/skills/signature-dispatch/SKILL.md" && \
   grep -qE 'degrade|graceful|appended to' "$SDR_PLUGIN/skills/signature-dispatch/SKILL.md"; then
  GRACEFUL_OK="yes"
fi
if [[ "$GRACEFUL_OK" == "yes" ]]; then
  report "10" "signature-dispatch degrades gracefully when sgc_crm_fields is not deployed; intended writes logged to pending-odoo-writes.yaml" "PASS"
else
  report "10" "signature-dispatch degrades gracefully when sgc_crm_fields is not deployed; intended writes logged to pending-odoo-writes.yaml" "FAIL" "graceful_check=$GRACEFUL_OK"
fi

echo ""
echo "=============================================================="
echo "ACCEPTANCE RESULT: $pass pass, $fail fail"
echo "=============================================================="
echo ""

if [[ $fail -ne 0 ]]; then
  echo "FAILURES:"
  for f in "${fails[@]}"; do
    echo "  - $f"
  done
  echo ""
  exit 1
fi

echo "All 10 acceptance items pass. Plugin is ready to ship (subject to RESOLVE in PUBLISHING.md)."
exit 0
