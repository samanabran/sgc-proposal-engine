# Why a full ERP is different from a point CRM tool

For use when a client is comparing SGC's Odoo proposal against a cheaper,
CRM-only competitor and asking "why would I pay more for more software
than I asked for?" Pair with `odoo-explained-plain.md` if the client hasn't
been introduced to Odoo yet, and
`objection-handling/price-too-high.md` if the comparison is really about
price rather than scope.

---

A point CRM tool does one job: it tracks leads, contacts, and deals. That's
useful, and if that's genuinely the only problem a business has, a
standalone CRM can be the right, cheaper answer.

The comparison changes once a deal in the CRM needs to turn into an
invoice, a stock movement, a payroll entry, or a project. A standalone
CRM doesn't do any of that — it hands off to whatever accounting or
operations software the company already uses, and someone has to move the
information across manually, or the two systems have to be connected with
a separate integration that has to be built, paid for, and maintained.

That handoff point is where most of the real cost and risk in "just use a
cheap CRM" actually lives, and it's usually invisible at the point of
comparison:

- **Double entry.** A deal closes in the CRM; someone re-types it into
  accounting to invoice it. Every re-type is a chance for the number, the
  tax treatment, or the customer record to not match between the two
  systems.
- **Reporting that doesn't add up.** Sales sees pipeline in one tool;
  finance sees revenue in another. Reconciling the two into one picture of
  the business becomes a manual, recurring task instead of a report that
  already exists.
- **Integration as a second project.** Connecting a CRM to separate
  accounting/inventory/HR software is its own implementation, with its own
  cost, its own maintenance burden, and its own failure point when either
  system updates independently.

An ERP like Odoo isn't "CRM plus extra modules nobody asked for" — it's
one system where a closed deal, an invoice, a stock movement, and a
payroll run share the same customer record and the same numbers, because
they're the same database, not three databases kept in sync by hand.

The right question isn't "why is this bigger than a CRM" — it's "does this
business's data need to leave the sales conversation and become an
invoice, a shipment, or a payroll entry without someone re-typing it."
If yes, the CRM-only quote is cheaper today and more expensive later, once
the manual reconciliation and integration cost is counted in.
