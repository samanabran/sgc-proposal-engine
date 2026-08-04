---
name: redacted-derivative-release
description: Desk-only skill. Authors and verifies the redacted derivatives that the SDR plugin ships. Runs the diff gate. Pushes the new versions.
version: 1.0.0
owner: Commercial Desk
position: desk-side; runs whenever a derivative needs authoring, re-cut, or re-issued
---

# redacted-derivative-release

The desk's authoring and verification skill for the redacted
derivatives the SDR plugin ships. Five files (six with the runbook)
interleave desk-only values with SDR-safe content; this skill cuts
the SDR-safe versions and verifies the diff gate.

## When to use

- Trigger phrases: "cut the SDR-safe derivative", "verify the diff gate", "re-issue the SDR plugin's knowledge", "what's the desk-only line set for policy.yaml", "what's the diff status", "publish the derivative".

If the floor table needs authoring, route to `published-floor-authoring`.
If the deal needs reviewing, route to `deal-card-review`. This skill
is structural — it operates on the plugin's content, not on a deal.

## Bundled knowledge files to read, in order

1. The original `00-knowledge/pricing/policy.yaml` (desk-only)
2. The original `00-knowledge/pricing/hosting.yaml` (desk-only)
3. The original `00-knowledge/pricing/payment-plans.yaml` (desk-only)
4. The original `00-knowledge/pricing/concession-ladder.yaml` (desk-only)
5. The original `00-knowledge/pricing/phase2-catalogue.yaml` (desk-only)
6. The original `00-knowledge/runbook/subscription-proposal-runbook.md` (desk-only)
7. The current SDR plugin's `plugins/sgc-proposal-engine/knowledge/` (the file being re-cut)
8. `DISTRIBUTION-MANIFEST.md` — the classification of every file
9. `plugins/sgc-proposal-engine/ci/diff-redacted-derivatives.py` — the diff gate

## What it writes, where

- `plugins/sgc-proposal-engine/knowledge/<redacted-file>` — the re-cut derivative
- `plugins/sgc-proposal-engine/CHANGELOG.md` — entry recording the re-issue (file, version, author, summary)
- `plugins/sgc-proposal-engine/plugin.json` — version bump per the semantic-version protocol

The skill is the only authorised writer of the SDR plugin's
redacted derivatives.

## What it refuses

- **Re-cut without a clean diff gate** — refuses to push a derivative that fails any of `diff-redacted-derivatives.py`, `forbidden-strings.sh`, or `secrets-scan.sh`. Cite the failing gate and the specific line.
- **Derivative that omits an SDR-safe line from the original** — refuses to publish a derivative that drops any line, key, or section that the original carries in the SDR-safe set. The derivative is a strict subset of the original for the flagged paths and the union for the SDR-safe paths.
- **Re-cut that introduces a new desk-only line in the derivative** — refuses to publish a derivative that contains any line on the desk-only line set. Cite `DISTRIBUTION-MANIFEST.md` forbidden-strings list.
- **Re-cut without a version bump** — refuses to publish a new derivative at the same plugin version. Any rate, formula, guardrail, or clause change is a version bump with the author recorded.
- **Re-cut that contradicts the canonical desk originals** — refuses to publish a derivative whose figures, gate statements, or policy decisions differ from the desk's canonical version. The derivative is a *redaction* of the original, not a re-interpretation.
- **Re-cut that introduces a forbidden string** — refuses to publish a derivative containing `AED 690`, `43,300`, `3,700`, `TRN`, `VAT exempt`, `free zone exempt`, `Enterprise tier`, `unlimited`, `AWS`, `Odoo mobile app`, `hosting_node_true_cost`, `liquid reserve`, `AED 7,000`, `AED 14,000`, `AED 4,960`, `internal_consultant_cost`, `absolute_margin_floor`, `AED 150/h`, `AED 150/hr`, `AED 360`, `150 AED`, `360 AED`. Cite the `DISTRIBUTION-MANIFEST.md` forbidden-strings list.

## The re-cut process

For each derivative:

1. Load the original from `00-knowledge/...`.
2. Apply the line-set redaction defined in the plan (`DISTRIBUTION-MANIFEST.md` §"Redacted derivatives (5 + 1)").
3. Write the derivative to `plugins/sgc-proposal-engine/knowledge/<redacted-file>`.
4. Run `diff-redacted-derivatives.py` against the original. The script verifies that:
   - All SDR-safe lines from the original are present in the derivative.
   - No desk-only line from the original appears in the derivative.
   - For YAML files, the derivative has a strict subset of original keys for any flagged path.
5. Run `forbidden-strings.sh` against the derivative.
6. Run `secrets-scan.sh` against the derivative.
7. Bump the plugin version in `plugins/sgc-proposal-engine/plugin.json`.
8. Update `plugins/sgc-proposal-engine/CHANGELOG.md` with the re-issue entry (file, version, author, summary, diff-gate result).
9. The desk's `PUBLISHING.md` describes the push mechanism; this skill does not push.

## What this skill does NOT do

- It does not write the deal card. The desk's `walk-away-authoring` does.
- It does not review a deal. The desk's `deal-card-review` does.
- It does not author the floor table. The desk's `published-floor-authoring` does.
- It does not invoke the SDR plugin's skills. The SDR plugin's skills run in the SDR plugin.
- It does not push. `PUBLISHING.md` describes the push mechanism; this skill produces the verified artefact and bumps the version.

## Escalation path

- **A line that is neither clearly SDR-safe nor clearly desk-only** — emit `RESOLVE: <file>:<line> = <text>` and route to the founder + Commercial Desk for joint classification. The re-cut pauses until the line is classified.
- **A clause-library file with internal notes** — `RESOLVE:` and route to the desk's `walk-away-authoring` for an editorial pass; the clause library is verbatim by intent.
- **A gate that needs to be re-numbered** — the gate number is in the canonical `commercial-rules/`. This skill never changes a gate number; the desk authors a new guardrail in `guardrails-g42-g53.yaml` (or a successor file) and bumps the version.
