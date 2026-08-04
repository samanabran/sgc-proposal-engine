#!/usr/bin/env bash
# init-workspace.sh
#
# Creates <cwd>/sgc-proposals/<CLIENT-CODE>/ from the workspace bootstrap
# the first time an SDR starts a new client. Idempotent: if the
# destination folder already exists, do nothing.
#
# Usage: bash plugins/sgc-proposal-engine/init-workspace.sh <CLIENT-CODE>
#   or:  bash init-workspace.sh                (interactive)
#
# The script never deletes, never overwrites anything in sgc-proposals/.
# A plugin upgrade MUST NOT touch this script's effect: sgc-proposals/
# stays outside the plugin.

set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLUGIN_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"
BOOTSTRAP_DIR="$PLUGIN_DIR/workspace-bootstrap"

if [[ ! -d "$BOOTSTRAP_DIR" ]]; then
  echo "FATAL: workspace-bootstrap/ not found at $BOOTSTRAP_DIR" >&2
  exit 1
fi

# Determine the workspace root (CWD by default).
WORKSPACE_ROOT="${SGC_PROPOSALS_ROOT:-$PWD}"

# Determine the client code.
if [[ $# -ge 1 ]]; then
  CLIENT_CODE="$1"
else
  read -rp "Client code (e.g. VGE-vongeyern-realestate): " CLIENT_CODE
fi

if [[ -z "$CLIENT_CODE" ]]; then
  echo "FATAL: client code is required" >&2
  exit 1
fi

# Validate the client code matches the brief's pattern: PREFIX-slug
# where PREFIX is 3+ uppercase letters, slug is lowercase-hyphenated.
if ! [[ "$CLIENT_CODE" =~ ^[A-Z]{3,}-[a-z0-9-]+$ ]]; then
  echo "WARN: client code '$CLIENT_CODE' does not match the standard PREFIX-slug pattern (e.g. VGE-vongeyern-realestate)." >&2
  echo "      Continuing anyway. If this is correct, ignore this warning." >&2
fi

DEST="$WORKSPACE_ROOT/sgc-proposals/$CLIENT_CODE"

if [[ -d "$DEST" ]]; then
  echo "OK: $DEST already exists. Idempotent — nothing to do."
  echo "    To re-bootstrap (DESTRUCTIVE), delete the directory first."
  exit 0
fi

# Create the parent directory if it doesn't exist.
mkdir -p "$WORKSPACE_ROOT/sgc-proposals"

# Copy the bootstrap to the destination. Use `cp -R` to preserve
# the structure; never use `rm` or `mv` against an existing destination.
cp -R "$BOOTSTRAP_DIR" "$DEST"

# Replace the manifest placeholders with the actual client code.
# The bootstrap's manifest.yaml is a template; the values are
# filled in by proposal-intake on step 1.
# (We do not pre-fill from the CLI; intake reads from the bootstrap.)

echo "OK: created $DEST"
echo ""
echo "Next steps:"
echo "  1. cd $DEST"
echo "  2. Invoke the proposal-intake skill — it will read the bootstrap"
echo "     and ask the tiered question bank."
echo "  3. The fact-ledger confirmation step is where fabrication gets caught."
echo "  4. The verbal-promises question is mandatory; 'none' is a valid answer."
echo ""
echo "Plugin upgrade note:"
echo "  This script is the only writer of <workspace>/sgc-proposals/."
echo "  A plugin upgrade does NOT touch this directory. Re-running"
echo "  init-workspace.sh on an existing client is a no-op (idempotent)."
