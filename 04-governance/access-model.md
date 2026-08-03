# Access Model — Rationale and Enforcement

Expands on the access table in `AGENTS.md`. That table states *what* each
layer's access is; this file explains *why* each boundary exists and *how*
it's meant to be enforced mechanically, not just by convention.

## The table, restated

| Layer | Who writes | Agents may |
|---|---|---|
| `00-knowledge/` | Commercial Desk only | Read only |
| `01-templates/` | Commercial Desk only | Read only |
| `02-clients/<client>/` | SDR + agent | Read + write, except `05-issued/` |
| `03-library/` | Any SDR, reviewed | Append, via review |
| `04-governance/` | Sales leadership | Read only |
| `05-ops/` | Commercial Desk | Read only |

## Rationale, per layer

### `00-knowledge/` — read-only to agents/SDRs

Every number in every proposal has to trace to a key in this layer
(`AGENTS.md`: "never invent a rate, hour figure, or percentage"). If an
SDR — or an agent under deal pressure — could edit `pricing/*.yaml`
directly, that guarantee disappears: a single edited rate silently
becomes "policy" for every subsequent deal that reads it, with no review
step in between. `known-defects.md #1` (the rate-drift incident) is what
happens even with a *single* authorized editor cross-checking two files;
without a restricted write boundary, the same class of error becomes
routine rather than a one-time catch. Changes here go through the
Commercial Desk and get logged in `CHANGELOG.md` in semver, specifically
so an in-flight worksheet's `knowledge_version_used` pin means something
(`known-defects.md #14`).

### `01-templates/` — read-only to agents/SDRs

Same logic as `00-knowledge/`, applied to structure rather than numbers.
Templates encode the required sections (assumptions, exclusions, adoption
clause, clawback clause — Commercial Rules 9/10) that every proposal must
contain. An SDR editing a template to drop a section under deadline
pressure would silently remove a protection the whole repo is built
around. Template changes are a governance decision, not a per-deal one.

### `02-clients/<client>/` — SDR + agent, read + write except `05-issued/`

This is the one layer that *has* to be writable for the work to happen at
all — intake, calc, drafts, and reviews all live here and change per
deal. The single carve-out, `05-issued/`, exists because once a proposal
has been sent, the client has a copy of it; editing the repo's copy after
that point creates two documents that disagree with no record of why
(`known-defects.md #5`). Everything else in a client folder is fair game
for the SDR building that specific deal — the boundary is about
*immutability after send*, not about restricting deal work.

### `03-library/` — any SDR, append via review

The library (worked examples, objection handling, snippets) is meant to
grow from real deal experience, so it can't be locked to Commercial Desk
the way pricing is — the people closest to live objections are the SDRs
having the conversations. But it still needs a review gate: an
unreviewed addition could quietly assert a wrong number, an outdated
positioning claim, or bad sales advice, and unlike a single client
proposal, a library entry gets reused across many deals — an error here
propagates further than an error in one client's worksheet. "Append via
review" means new entries are proposed and reviewed before they're
treated as reusable guidance, not edited in place after acceptance.

### `04-governance/` — sales leadership, read-only to everyone else

Approval thresholds, escalation triggers, and the review log are the
control layer that governs how the other layers get used. If an SDR could
edit `approval-matrix.md` to raise their own approval ceiling, or edit
`review-log.md` to remove an inconvenient finding, the entire escalation
model becomes advisory rather than binding. This layer changes only by
deliberate leadership decision.

### `05-ops/` — Commercial Desk, read-only to everyone else

Naming conventions, the gate-validation procedure, and onboarding are
operational infrastructure — they need to be stable and consistent across
every deal and every new hire, not something each SDR can locally
reinterpret. Read access is unrestricted (everyone needs to follow the
procedure); write access is restricted to the team that owns process
consistency.

## Enforcement mechanism

**Primary: git branch protection.** In a environment with real git
remotes and branch protection rules, the correct enforcement is a
protected-branch policy: `00-knowledge/`, `01-templates/`, `04-governance/`,
and `05-ops/` changes require a PR reviewed and merged by an authorized
Commercial Desk / Sales leadership account, with CODEOWNERS routing
enforcing *who* can approve which paths. This is the mechanism to
implement first if/when the repo moves to a git host that supports it.

**Fallback: social convention + `.readonly-marker` files.** This was an
open question in the original design and remains one: not every
environment this repo runs in supports branch protection (a local clone,
a sandboxed agent workspace, a git host without CODEOWNERS support). In
those environments, enforcement falls back to:

1. **`AGENTS.md`'s absolute rules**, which every agent operating in this
   repo is required to read before touching a file — the contract itself
   is the enforcement when tooling can't be.
2. **A `.readonly-marker` file** (a plain marker file, e.g.
   `.readonly-marker` at the root of `00-knowledge/`, `01-templates/`,
   `04-governance/`, and `05-ops/`) as a machine-checkable signal that
   tooling or a pre-commit hook can look for, even without branch
   protection — a script that refuses to stage changes under a directory
   containing this marker is a cheap, portable enforcement layer that
   works the same on a laptop clone as it does in an agent sandbox.

Both mechanisms should coexist rather than being treated as either/or:
branch protection is the strong guarantee where the git host supports it;
the marker-file convention is the fallback that keeps the boundary
meaningful everywhere else. Neither currently exists as implemented
tooling in this repo as of this writing — flagging that gap here is
itself part of closing the open question, and it belongs on the
Commercial Desk / Sales leadership backlog to implement one or both.
