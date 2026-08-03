# Onboarding a New SDR

Four steps, in order. Don't skip ahead to step 4 because a real deal is
waiting — the first three steps are what make step 4 safe to do without
supervision on every deal after the first.

## Step 1 — Read the runbook

Read `runbook/subscription-proposal-runbook.md` start to finish, alongside
`AGENTS.md` (the operating contract it sits under). Don't skim — the
runbook's sequence (`intake → calc → gate check → draft → QA checklist →
human review → issue`) is the spine of every proposal this repo produces,
and the absolute rules in `AGENTS.md` (never write to `00-knowledge/`,
never invent a number, never edit `05-issued/`) are non-negotiable, not
suggestions to be reinterpreted under deadline pressure.

**Done looks like**: the new SDR can explain, without looking it up, what
the seven stages of the sequence are, what the three model codes (`SUB`,
`PRJ`, `RET`) mean, and why `05-issued/` is immutable.

## Step 2 — Read the known defects

Read `failure-modes/known-defects.md` in full — all fifteen entries. This
is described in that file itself as "the highest-value onboarding asset in
the repo," and it's not exaggeration: every gate, every access
restriction, and every naming convention in this repo exists because one
of these fifteen things happened or was identified as a real risk before
it happened. Reading the mechanisms without reading the failure they
prevent makes the mechanisms feel like arbitrary bureaucracy; reading the
failures first makes them make sense.

**Done looks like**: the new SDR can, for any of the ten gates (G1–G10),
name the specific known-defect scenario that gate exists to catch —
without re-reading the file to answer. See
`04-governance/escalation-triggers.md` for the gate-to-defect mapping if
a check is needed.

## Step 3 — Walk the worked example end to end

Work through `03-library/worked-examples/boutique-brokerage-5users-24mo.md`
by hand — not by reading it passively, but by reproducing the arithmetic
yourself with a calculator or spreadsheet, section by section: cost-to-
serve, build hours, financing, assembly, then all ten gates. Compare your
numbers to the file's at each step before moving to the next.

This is the single best way to internalize how the pieces connect —
reading the runbook tells you the *order* of the calc; doing this exercise
by hand tells you how a change in one number (say, moving `finance_setup`
from medium to high band) ripples through documentation hours, QA hours,
the subtotal, PM, contingency, build value, and then G1/G8/G9
simultaneously.

**Done looks like**: the new SDR reproduces every number in the worked
example independently and can explain, for at least three of the file's
flagged "judgment call" notes, what the alternative interpretation would
have been and why it matters.

## Step 4 — Run a first deal, gate report reviewed before issue

Take on a real (or realistic training) deal and run it through the full
sequence — intake through gate check through draft. Before this deal
reaches `04-review` / human sign-off in the normal runbook sense, a human
reviewer (Sales Lead or Commercial Desk, per `04-governance/
approval-matrix.md`) additionally reviews the **gate report specifically**
with the new SDR, line by line, before the proposal is allowed to issue.
This is a heavier review than a normal deal gets — it exists to catch
onboarding-specific mistakes (a segment misassignment, a rate not
correctly pinned, a rounding convention applied inconsistently) while
they're still cheap to fix, before the new SDR is running deals solo.

**Done looks like**: the gate report for this first deal is reviewed and
signed off by a human reviewer with zero unresolved discrepancies, and
the new SDR can explain every number in their own gate report without the
reviewer having to explain it back to them first. Once this deal issues
cleanly, subsequent deals follow the normal runbook review cadence — this
extra review step is a one-time onboarding gate, not a permanent
requirement for that SDR.
