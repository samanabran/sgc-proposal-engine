# Odoo CES KPI Discovery — Verification Addendum

Read-only verification pass against the `odoo19-sgc` cluster on `contabo-sgc`. Companion to `odoo-ces-kpi-discovery-report.md`. All queries were SELECT-only against Postgres via `docker exec odoo-prod-db psql`, plus read-only `grep`/`find`/`docker ps`/`docker inspect` on the host. No writes were made to any system.

---

## 1. Staging availability

**Finding:** Staging exists and is reachable, with an addons path isolated from prod.

- Container `odoo19-sgc-staging` is running (`docker ps` showed "Up 2 hours").
- Database `sgc_staging` exists on the same Postgres instance (`odoo-prod-db`) as prod's `odoo19-sgc` DB (confirmed via `psql -U odoo -l` inside `odoo-prod-db`, which listed both `odoo19-sgc` and `sgc_staging`).
- `docker inspect odoo19-sgc-staging` mounts: `/opt/staging/odoo19-sgc-feature -> /mnt/staging-addons` (staging-only addons path) **and** `/opt/odoo-prod/extra-addons -> /mnt/extra-addons` (prod addons, also mounted read-through into staging) plus a dedicated data volume for `/var/lib/odoo`.
- `/opt/staging/odoo19-sgc-feature` already contains working copies of several `sgc_*` modules (`sgc_executive_dashboard`, `sgc_lead_scoring`, `sgc_meeting_ai`, `sgc_proposal_engine`, `sgc_crm_dashboard`, `sgc_sales_playbook`, `sgc_onboarding_documents`), indicating the established deploy pattern: drop/copy a new module folder into `/opt/staging/odoo19-sgc-feature/`, it becomes visible to the staging container without affecting prod's `/opt/odoo-prod/extra-addons`.

**Evidence:** `docker ps`; `docker inspect odoo19-sgc-staging --format '{{range .Mounts}}...'`; `docker exec odoo-prod-db psql -U odoo -l`; `ls -la /opt/staging/odoo19-sgc-feature`.

**Confidence:** Confirmed from database/host metadata.

---

## 2. CRM stage count

**Finding:** Exactly **12** stages exist (prior report's "11" was incorrect; it did list 12 by name but miscounted).

Full list (id | sequence | name, en_US label shown):

| id | sequence | name (en_US) |
|----|----------|--------------|
| 1  | 0 | New |
| 10 | 1 | Valid Contact |
| 8  | 2 | Outreach Email |
| 5  | 3 | No Answer |
| 7  | 4 | Not Interested |
| 6  | 5 | Follow Up |
| 2  | 6 | Research Done |
| 3  | 7 | Meeting Booked |
| 9  | 8 | Proposal |
| 4  | 9 | Won |
| 11 | 10 | No Answer - Talha Pipeline |
| 12 | 11 | No Answer - John Pipeline |

**Evidence:** `SELECT count(*) FROM crm_stage;` → 12. `SELECT id, sequence, name FROM crm_stage ORDER BY sequence;` (full listing above).

**Confidence:** Confirmed from database.

---

## 3. hr.version "current version" semantics

**Finding:** There is **no boolean/computed "current" indicator** on `hr_version`. All 68 columns were enumerated via `information_schema.columns`; the only relevant date columns are `date_version`, `contract_date_start`, `contract_date_end`, `trial_date_end` — none of them a status flag.

"Current" record for an employee must be derived in application code as `MAX(date_version) WHERE date_version <= CURRENT_DATE` per `employee_id`. This was validated against the 4 known CES employees: each currently has exactly **one** `hr_version` row (see item 4), so for this specific job the derivation is trivially correct today, but the logic must still be implemented generically since employees with multiple versions do exist elsewhere in the system's data model.

**Evidence:** `SELECT column_name, data_type FROM information_schema.columns WHERE table_name='hr_version' ORDER BY ordinal_position;` (68 rows, no boolean/current column). `SELECT employee_id, date_version, job_id FROM hr_version WHERE employee_id IN (...)` for the 4 CES employees.

**Confidence:** Confirmed from database metadata + aggregate data.

---

## 4. Job transfer history for CES employees

**Finding:** All 4 CES-job employees (job_id=1) have **exactly one** `hr_version` row each — no job/comp change history, no transfers into the role from a different job.

| employee_id | count | min(date_version) | max(date_version) |
|---|---|---|---|
| 7  | 1 | 2026-06-02 | 2026-06-02 |
| 8  | 1 | 2026-07-01 | 2026-07-01 |
| 17 | 1 | 2026-08-06 | 2026-08-06 |
| 19 | 1 | 2026-08-06 | 2026-08-06 |

Since each has only one version row, `contract_date_start` and the CES role-entry date are identical for all 4 — there is currently no case where they'd diverge.

**Evidence:** `SELECT employee_id, date_version, job_id FROM hr_version WHERE employee_id IN (SELECT employee_id FROM hr_version WHERE job_id=1) ORDER BY employee_id, date_version;` and the GROUP BY aggregate query.

**Confidence:** Confirmed from aggregate data.

---

## 5. sale.order signature fields

**Finding:** All fields exist as expected:

| column | data_type |
|---|---|
| require_signature | boolean |
| signed_on | timestamp without time zone |
| client_sign_date | date |
| provider_sign_date | date |
| opportunity_id | integer |
| signed_by | character varying |

`opportunity_id` exists and links to `crm_lead`, but is populated on only **2 of 27** sale_order rows (92.6% null).

Aggregates: `signed_on IS NOT NULL` → **0** rows. `require_signature = true` → **26 of 27** rows.

**Evidence:** `information_schema.columns` query on `sale_order`; `SELECT count(*), count(opportunity_id) FROM sale_order;` → 27, 2; `SELECT count(*) FILTER (WHERE signed_on IS NOT NULL), count(*) FILTER (WHERE require_signature=true) FROM sale_order;` → 0, 26.

**Confidence:** Confirmed from database metadata + aggregate data.

---

## 6. DocuSeal linkage

**Finding:** No real DocuSeal integration exists — the fields that look like e-signature linkage are explicitly documented in source as **Zoho Sign** fields, not DocuSeal, and there is zero DocuSeal-referencing code anywhere in the custom addons tree despite a `docuseal` Docker container running on the same host.

- Case-insensitive grep for `docuseal` across `/opt/odoo-prod/extra-addons` (recursively, all files): **zero matches**.
- The fields `x_envelope_id`, `x_signed_pdf_hash` (asked about specifically) live in `/opt/odoo-prod/extra-addons/sgc_crm_fields/models/crm_lead.py`, under a comment block explicitly headed `# --- Zoho Sign envelope linkage ---`, with field labels "Zoho Sign Envelope ID" and help text "Envelope ID assigned by Zoho Sign when the proposal is sent for signature." Related fields in the same file: `x_frozen_pdf_hash`, `x_sent_date`, `x_completed_date`, `x_signing_actor_client`, `x_signing_actor_sgc`, `x_decline_reason` — all plain stored fields with no compute methods and no controller/webhook writing to them found anywhere in the addon tree.
- No webhook controller, model, or cron references DocuSeal anywhere on the host under `/opt/odoo-prod`.

**Evidence:** `grep -rli "docuseal" /opt/odoo-prod/extra-addons` → no output. `grep -rli "docuseal" /opt/odoo-prod` (whole prod tree) → no output. Full read of `sgc_crm_fields/models/crm_lead.py`.

**Confidence:** Confirmed from source code (absence of integration) + confirmed from source code (Zoho Sign framing).

---

## 7. Payment/invoice linkage

**Finding:**

- `account_move.payment_state` is `character varying`. Observed distinct values in data: `blocked`, `paid`, `not_paid` (only 3 distinct values present; Odoo's enum also supports `partial`/`in_payment`/`reversed` but none appear in current data).
- There is **no direct `sale_line_ids` column** on `account_move_line`. The actual link table found via `information_schema.tables` is `sale_order_line_invoice_rel` (a many-to-many relation table between `sale_order_line` and `account_move_line`/invoice lines) — not a scalar FK column.
- Aggregate: posted invoices with `payment_state IN ('paid','partial')` → **28** rows (all were 'paid'; no 'partial' rows exist in current data).

**Evidence:** `information_schema.columns` on `account_move`; `SELECT DISTINCT payment_state FROM account_move;`; `information_schema.tables` search for `%sale_order_line%rel%`; `SELECT count(*) FROM account_move WHERE state='posted' AND payment_state IN ('paid','partial');` → 28.

**Confidence:** Confirmed from database metadata + aggregate data.

---

## 8. x_days_since_activity / x_last_activity_date provenance

**Finding — important reliability caveat:**

- `x_days_since_activity` (Integer, `sgc_lead_scoring/models/crm_lead.py` line ~139) is declared but has **no compute method and no write site anywhere in the codebase** — the only other reference to it in the entire addons tree is in `sgc_lead_scoring/views/crm_lead_views.xml` (displaying it). It is a **dead/orphan field**: never populated by any code path found. **Not trustworthy as a staleness signal** — likely always shows a stale or default value.
- `x_last_activity_date` (Datetime, same file, line ~108) **is** written, but only by lead-enrichment helper methods: `abstract_enrichment.py` (line 160), `hunter_enrichment.py` (line 154), `llm_enrichment.py` (line 183) — each sets `to_update['x_last_activity_date'] = now` (or `changes[...]`) as part of writing enrichment results (Apollo/Hunter/LLM company enrichment) back onto the lead. This means the field reflects **"last time enrichment ran on this lead,"** not real CRM/sales activity (calls, emails, stage changes). It will go stale between enrichment runs and does not track genuine engagement events (no mail_activity cron, no crm_lead write override tied to real activity).

**Evidence:** `grep -rn "x_days_since_activity\|x_last_activity_date" /opt/odoo-prod/extra-addons` across all sgc_lead_scoring files; read of `abstract_enrichment.py` lines 140-165 showing the `to_update['x_last_activity_date'] = now` assignment inside an enrichment write block.

**Confidence:** Confirmed from source code.

---

## 9. hr.employee manager field

**Finding:**

- `hr_employee.parent_id` exists (confirmed via information_schema) and is populated for **3 of 4** CES employees.
- `hr_version.hr_responsible_id` (per prior report) is populated for **4 of 4** CES employees.

`hr_responsible_id` on `hr_version` is the more reliably populated field for this cohort and should be preferred.

**Evidence:** `information_schema.columns` for `parent_id` on `hr_employee`; `SELECT count(*) FILTER (WHERE he.parent_id IS NOT NULL), count(*) FILTER (WHERE hv.hr_responsible_id IS NOT NULL) FROM hr_employee he JOIN hr_version hv ON hv.employee_id=he.id WHERE hv.job_id=1;` → 3, 4.

**Confidence:** Confirmed from aggregate data.

---

## 10. Existing security groups

**Finding:** Relevant groups from `ir_model_data` where `model='res.groups'` and `module IN ('crm','sales_team','hr','account')`:

- account: group_account_basic, group_account_invoice, group_account_manager, group_account_readonly, group_account_secured, group_account_user, group_cash_rounding, group_delivery_invoice_address, group_partial_purchase_deductibility, group_validate_bank_account
- crm: group_use_lead, group_use_recurring_revenues
- hr: group_hr_manager, group_hr_user
- sales_team: group_sale_manager, group_sale_salesman, group_sale_salesman_all_leads

No CES-named group exists: `SELECT name FROM res_groups WHERE name::text ILIKE '%CES%' OR name::text ILIKE '%engagement%';` returned 8 rows, none of which are CES/engagement-related (matches were incidental substrings in unrelated group labels — attendance/access-rights groups). **No group named for the CES role exists anywhere in the system.**

**Evidence:** the two SQL queries above.

**Confidence:** Confirmed from database.

---

## 11. sgc_executive_dashboard KPI provider framework

**Finding:** Stable, clean extension point — safe for a new addon to register into without modifying `sgc_executive_dashboard`.

Base class: `sgc.kpi.provider` (`models.AbstractModel`), file `/opt/odoo-prod/extra-addons/sgc_executive_dashboard/models/sgc_kpi_provider.py`.

- Docstring: "Base contract for every SGC dashboard data provider. Subclass, set the `_sgc_*` attributes and implement `_sgc_collect`. The aggregator auto-discovers any registry model inheriting this one."
- Key override points: `_sgc_module`, `_sgc_label`, `_sgc_icon`, `_sgc_accent`, `_sgc_sequence`, `_sgc_pitch` (descriptor attributes) and `_sgc_collect(self, ctx)` (returns `{'kpis': [...], 'charts': [...]}`).
- Safe entry point `_sgc_run(ctx)` checks `_sgc_is_installed()` (via `ir.module.module` state) and wraps `_sgc_collect` in a try/except so one broken provider can't break the dashboard.
- Shared helpers provided: `_sgc_company_domain`, `_sgc_sum`, `_sgc_count`, `_sgc_series`, `_sgc_kpi` (normalizes KPI envelope for the OWL layer), `_sgc_delta`, `_sgc_previous_range`.

A new addon can define `class SgcCesKpiProvider(models.AbstractModel): _inherit = 'sgc.kpi.provider'` (or a fresh model inheriting it) with its own `_sgc_module='sgc_ces_kpi_banner'` and override `_sgc_collect`, and it will be auto-discovered — no edits needed to `sgc_executive_dashboard` itself.

**Evidence:** full read of `sgc_kpi_provider.py`. (`sgc_kpi_definition.py` located but not read in full — file exists at same path, not required for this determination.)

**Confidence:** Confirmed from source code.

---

## 12. Odoo 19 OWL/systray API surface (sgc_app_home reference pattern)

**Finding:** `sgc_app_home`'s systray component confirms current Odoo 19 conventions to mirror for the new floating banner.

File: `/opt/odoo-prod/extra-addons/sgc_app_home/static/src/js/home_systray.js`

```js
/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";

export class SgcHomeSystray extends Component {
    static template = "sgc_app_home.HomeSystray";
    static props = {};

    setup() {
        this.action = useService("action");
    }

    goHome() {
        this.action.doAction("sgc_app_home.action_sgc_app_home");
    }
}

registry.category("systray").add(
    "sgc_app_home.HomeSystray",
    { Component: SgcHomeSystray },
    { sequence: 1 }
);
```

- Import paths: `@web/core/registry`, `@web/core/utils/hooks` (for `useService`), `@odoo/owl` (for `Component`; `useState`/`onWillStart` etc. would come from the same `@odoo/owl` module if needed).
- Registration pattern: `registry.category("systray").add(<unique_key>, { Component }, { sequence })`.
- Asset bundle: registered under `web.assets_backend` in `sgc_app_home/__manifest__.py`, alongside its scss/xml:
  ```
  "web.assets_backend": [
      "sgc_app_home/static/src/scss/app_home.scss",
      "sgc_app_home/static/src/js/app_home.js",
      "sgc_app_home/static/src/xml/app_home.xml",
      "sgc_app_home/static/src/scss/home_systray.scss",
      "sgc_app_home/static/src/js/home_systray.js",
      ...
  ]
  ```

**Confidence:** Confirmed from source code.

---

## Blockers for implementation

1. **DocuSeal vs Zoho Sign decision needed.** The prompt assumed a DocuSeal integration; the actual (unused) fields are labeled for Zoho Sign, and neither has any real write-back code. Before building signature-status KPIs, the business needs to decide which e-signature provider is actually in use / intended, and a real webhook/controller integration needs to be built for whichever is chosen — currently the fields are 100% orphaned (0 rows have `signed_on` set).
2. **x_days_since_activity is dead code.** If any KPI banner intends to show "days since last activity," it cannot rely on this field (never written). Either implement fresh compute logic or repurpose `x_last_activity_date` with the caveat that it only reflects enrichment runs, not real engagement.
3. **CES security group does not exist.** If the new addon needs role-based visibility/access restricted to CES staff, a new `res.groups` entry (and its assignment to the 4 relevant users) must be created — no existing group can be reused.
4. **opportunity_id null-rate (92.6%) limits sale_order → crm_lead joins.** Any KPI relying on linking sale_order back to its originating opportunity will only work for a small minority of orders; needs a business decision on whether/how to backfill this link or whether to join via another path (e.g., partner_id).
5. **hr.version multi-version handling is currently untested against real multi-version data** — all 4 CES employees happen to have single-version histories today, so the `MAX(date_version)` "current version" derivation logic should be written defensively/generically but cannot be validated against a real multi-row case within this cohort.
