# Arabic (UAE) Locale

**status: SPEC INCOMPLETE — requires native reviewer**

Existing proposals in this repo's history contain Arabic lines with no
typography spec behind them — this file exists to stop that recurring
until a native reviewer has actually specified the following:

- **Font pairing**: candidate is IBM Plex Sans Arabic, paired with the
  Latin `tokens/type.yaml` families — **not confirmed**, needs native
  reviewer sign-off on legibility and weight matching.
- **RTL grid mirroring**: whether `tokens/grid.yaml` columns mirror
  wholesale for an Arabic-primary document, or whether Arabic content is
  always secondary/summary and stays LTR-framed with embedded RTL text
  blocks — **not decided**.
- **Numeral convention**: Eastern Arabic numerals (٠١٢٣...) vs. Western
  Arabic numerals (0123...) in commercial figures — UAE commercial
  practice commonly uses Western numerals even in Arabic text, but this
  needs explicit confirmation, not assumption, given this repo's own
  "don't invent numbers" discipline extends to formatting conventions too.
- **Parallel vs. summary-only**: whether Arabic content runs as a full
  parallel translation of every section, or as an executive-summary-only
  companion document — **not decided**, and materially changes the scope
  of every future Arabic-language proposal.

**Do not draft Arabic content into any client-facing proposal until this
file's status changes from SPEC INCOMPLETE.** If a client requires Arabic
now, escalate to the Commercial Desk rather than improvising a typography
or scope decision here.
