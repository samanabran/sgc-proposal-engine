# Odoo CES KPI/Target Banner — Discovery Report

Investigation date: 2026-08-16. Read-only investigation of production Odoo (`odoo-prod` / `odoo-prod-db`, DB `odoo19-sgc`) via SSH (`contabo-sgc`) and `docker exec`. No writes, no ORM calls, no module installs, no PII in this report.

---

## 1. Executive Summary

The target CES KPI/gate concept does **not exist yet** as a coherent feature, but the codebase already contains almost every building block it would need, built for an adjacent (but distinct) concept: **`sgc_sales_playbook`**, a custom addon that gates the CRM "Proposal" stage behind 4 "Verifiable Buyer Exit Criteria" questions (problem, cost of inaction, approver, timeline), with Sales-Manager override, dead-lead cleanup cron, and dashboard surfacing via `sgc_crm_dashboard`/`sgc_executive_dashboard`. This is a **stage-entry qualification gate**, not a rep-tenure/pipeline-value/staleness KPI gate — the two concepts share vocabulary ("gate") but are functionally different.

Key findings relevant to the CES hypothesis:
- **CES role confirmed** (correction to first pass — see Section 5): `hr.job` id=1, title "Telesales/Client Engagement Specialist", held by 4 active employees, all linked to `res.users`, joined via the Odoo 19 `hr_version` model (not `hr_employee` directly). 1,832 active `crm_lead` records are owned by these 4 users. No security group exists for the role — job title alone is authoritative.
- `crm_lead` already has `date_last_stage_update`, `x_days_since_activity`, `x_last_activity_date` — solid raw material for 45-day staleness (Confirmed from database metadata).
- No native Odoo `sign` module is usable (state = `uninstallable`). However, `crm_lead` has custom fields `x_envelope_id`, `x_signed_pdf_hash`, `x_frozen_pdf_hash`, `x_signing_actor_client`, `x_signing_actor_sgc` (added by `sgc_crm_fields`) that strongly suggest an **existing external e-signature integration**, plausibly tied to the `docuseal` Docker container observed on the host (Inferred — no direct DB-to-container linkage code was found in the addons searched).
- `sale_order` separately has native e-sign columns (`signed_on`, `client_sign_date`, `provider_sign_date`, `require_signature`, `signed_by`) — the standard Odoo online-quote signature feature, independent of docuseal (Confirmed from database metadata).
- `gamification` and `gamification_sale_crm` modules are installed, with full `gamification_goal`/`gamification_challenge`/`gamification_badge` tables present — this is the closest thing to existing "daily/monthly KPI target" infrastructure (Confirmed from database metadata), though it's unclear if it's actively configured for CRM targets (Unresolved — contents not queried, only table existence, per PII/data-minimization rule).
- A floating/systray UI precedent exists: `sgc_app_home` ships a working OWL systray component (`SgcHomeSystray`) registered via `registry.category("systray")`, proving the asset-bundling/OWL pattern needed for a floating KPI banner is already proven out in this codebase (Confirmed from source code).
- `crm_lead` volume: ~14,565 live rows per `pg_stat_user_tables` estimate; a stricter default-domain count returned 8,984, implying roughly 5,500 archived/inactive leads (Confirmed from aggregate data, with the discrepancy flagged as Unresolved pending an explicit `active` column check).

---

## 2. Environment Findings

- **Odoo version**: 19.0.1.3, confirmed from `ir_module_module.latest_version` for the `base` module. — *Confirmed from database metadata.*
- `docker exec odoo-prod odoo-bin --version` failed (`odoo-bin` not on PATH inside container); version was instead confirmed via the DB query above. — *Confirmed from database metadata* (environment-level confirmation via odoo-bin itself is Unresolved).
- **Containers**: `odoo-prod` (image `odoo:19.0-sgc`), `odoo-prod-db` (postgres:16). Also present on host but untouched: `odoo19-sgc-staging`, `sgc_staging` DB, `docuseal` (image `docuseal/docuseal`), `signature-handler` (image `python:3.12-slim`). — *Confirmed from database metadata / docker inspection.*
- **Volume mounts for `odoo-prod`** (`docker inspect`):
  - `/opt/odoo-prod/extra-addons` → `/mnt/extra-addons` (bind, read-only) — this is where all custom (`sgc_*` and other) addons live.
  - `/opt/odoo-prod/data/odoo-prod-filestore` → `/var/lib/odoo` (bind, read-write) — filestore.
  - `/opt/odoo-prod/odoo-prod.conf` → `/etc/odoo/odoo.conf` (bind, read-only).
  — *Confirmed from environment (docker inspect).*
- DB `odoo19-sgc` reachable and owned by `odoo` user, confirmed via `psql -l` (per task setup, already verified prior to this session).

---

## 3. Installed Modules Relevant to CRM/CES/KPI

From `ir_module_module WHERE state='installed'` (full list captured; only CRM/Sales/Accounting/Payments/HR/Gamification/Dashboard-relevant subset shown here) — *Confirmed from database metadata*:

**CRM/Sales core**: `crm`, `crm_executive_dashboard`, `crm_iap_enrich`, `crm_iap_mine`, `crm_livechat`, `crm_mail_plugin`, `crm_sms`, `sale`, `sale_crm`, `sale_management`, `sale_pdf_quote_builder`, `sale_project`, `sale_service`, `sale_sms`, `sale_timesheet`, `sales_team`, `sale_agreement_report`, `website_crm`, `website_crm_livechat`, `website_crm_sms`

**Accounting/Payments**: `account`, `account_check_printing`, `account_payment`, `accounting_pdf_reports`, `om_account_accountant`, `om_account_asset`, `om_account_budget`, `om_account_daily_reports`, `om_account_followup`, `om_fiscal_year`, `payment`, `payment_custom`, `payment_stripe`, `snailmail_account`, `statement_report`

**HR**: `hr`, `hr_attendance`, `hr_calendar`, `hr_gamification`, `hr_holidays`, `hr_homeworking`, `hr_hourly_cost`, `hr_livechat`, `hr_org_chart`, `hr_payroll_account_community`, `hr_payroll_community`, `hr_recruitment`, `hr_skills`, `hr_timesheet`

**Gamification/Dashboards**: `gamification`, `gamification_sale_crm`, `hr_gamification`, `spreadsheet_dashboard`, `spreadsheet_dashboard_sale`, `spreadsheet_dashboard_account`, `spreadsheet_dashboard_hr_timesheet`, `spreadsheet_dashboard_im_livechat`, `spreadsheet_dashboard_sale_timesheet`, `spreadsheet_dashboard_stock_account`, `spreadsheet_dashboard_website_sale`

**Custom `sgc_*` and related** (see Section 4 for full inventory).

**Notably NOT installed / not usable**: `sign` exists as a module row but `state = 'uninstallable'` (native Odoo Sign is not active on this instance). No module literally named `docuseal` or `esign` exists in `ir_module_module` — any docuseal integration is therefore either external-only (webhook/API, no Odoo addon) or lives inside a custom addon under a different name. — *Confirmed from database metadata.*

---

## 4. Custom Addons Inventory

Location: `/opt/odoo-prod/extra-addons` on host, mounted read-only at `/mnt/extra-addons` in `odoo-prod`. — *Confirmed from environment.*

Custom (`sgc_*`, `sttl_*`, and a few uniquely-named) addons identified as installed and relevant to CRM/CES/KPI, from directory listing + `ir_module_module`:

| Addon | Relevance |
|---|---|
| `sgc_sales_playbook` | Proposal-stage qualification gate (4-question "Verifiable Buyer Exit Criteria"), dead-lead cleanup cron, weekly gate-compliance review cron. Depends on `sgc_lead_scoring`, `sgc_executive_dashboard`. |
| `sgc_lead_scoring` | BANT fields feeding into the playbook gate (per playbook manifest description). |
| `sgc_executive_dashboard` | Generic pluggable KPI-provider framework (`sgc_kpi_provider.py`, `sgc_kpi_definition.py`, `providers/provider_crm_sales.py`, `providers/provider_commission.py`, `providers/provider_deals.py`, etc.) — an existing extensible KPI abstraction layer that a CES KPI could plug into. |
| `sgc_crm_dashboard` | CRM-specific dashboard, includes a "big screen" mode (`big_screen.xml`, `big_screen.js`) — TV/wallboard-style KPI display precedent. |
| `crm_executive_dashboard` | A second, separately-named CRM dashboard addon (`crm_dashboard_kpi.py`, `crm_dashboard_alert.py`, alerting infrastructure) — appears to overlap in purpose with `sgc_crm_dashboard`/`sgc_executive_dashboard` (Unresolved which is authoritative/active). |
| `sgc_crm_fields` | Adds custom fields to `crm.lead` including `x_envelope_id`, `x_signed_pdf_hash` (signature-integration fields). |
| `sgc_crm_ai_compat` | AI compatibility layer for CRM (purpose not further inspected). |
| `sgc_crm_outreach_popup` | Popup UI pattern precedent (name suggests floating/modal UI on CRM records). |
| `sgc_persona` | Purpose not inspected in depth (name suggests user/rep persona modeling — possibly relevant to CES role definition, Unresolved). |
| `sgc_user_hygiene` | Purpose not inspected in depth. |
| `sgc_employee_onboarding` / `sgc_onboarding_documents` | HR onboarding — possibly relevant to "tenure" tracking for CES gates. |
| `sgc_ai_powerbox` | AI utility addon. |
| `sgc_app_home` | Ships a working OWL **systray** component (`SgcHomeSystray`) — direct precedent for floating/clickable widget UI. |
| `sgc_meeting_ai` | Meeting notes AI, includes its own `gate_answers_apply_wizard.py` (separate "gate" concept — applies AI-extracted meeting answers into the sales-playbook gate fields, with rep confirmation required). |
| `sgc_employee_badges` | Uses `gamification_badge` data — ties into the installed gamification module. |

Two dashboard-style modules (`sgc_crm_dashboard`, `crm_executive_dashboard`, and `sgc_executive_dashboard`) coexist; which is the actively-used/primary one for CRM KPIs is **Unresolved** — would need a follow-up check of `ir_ui_menu`/`ir_actions` usage or asking the SGC team directly.

---

## 5. CES Role — How It Is Represented (CORRECTED)

**Correction to original pass**: the first investigation pass queried `hr_employee.job_id` directly and got `column "job_id" does not exist`, then stopped without checking Odoo 19's actual schema. In Odoo 19, employee job/contract data was moved off `hr_employee` onto a new `hr.version` model (`hr_version` table, employee-versioning/history pattern replacing `hr.contract`). The job link lives at `hr_version.job_id`, not `hr_employee.job_id`. Re-queried directly:

- `hr_job` id=1, title **"Telesales/Client Engagement Specialist"** — this is the CES role. — *Confirmed from database metadata.*
- No separate `res.groups`, custom boolean/selection field, or literal "CES" string anywhere in source or `ir_model_data` — the role is represented **purely as an `hr.job` position**, joined via `hr_version.job_id`, not via security groups. — *Confirmed from database metadata + source grep (negative result on groups/fields).*
- **4 distinct employees** hold this job title (`SELECT count(DISTINCT employee_id) FROM hr_version WHERE job_id=1`), all currently active (`hr_employee.active=true`), 0 inactive/former holders found. — *Confirmed from aggregate data.*
- All 4 have a linked `res.users` account (`hr_employee.user_id IS NOT NULL`). — *Confirmed from aggregate data.*
- 2 distinct `hr_responsible_id` (manager) values and 2 distinct `department_id` values across the 4 — CES reps are not all under one manager/department. — *Confirmed from aggregate data (IDs only, no names, per no-PII rule).*
- `hr_version.contract_date_start` range across the 4: **2026-06-02 to 2026-08-06** — plausible tenure/start-date field for gate-month calculation. `hr_version.trial_date_end` is **empty for all 4** — probation-end tracking exists as a field but is unpopulated, so it cannot currently drive gate timing. — *Confirmed from aggregate data.*
- Direct CRM linkage confirmed: joining `crm_lead.user_id` → `hr_employee.user_id` → `hr_version.job_id=1` (active leads only) returns **1,832 active `crm_lead` records** owned by CES-titled users — this is real, non-trivial pipeline volume, not a dormant/unused role. — *Confirmed from aggregate data.*
- Existing CRM-relevant `res.groups` (from `ir_model_data`, XML IDs only, no data): `sales_team.group_sale_salesman`, `sales_team.group_sale_salesman_all_leads`, `sales_team.group_sale_manager`, `crm.group_use_lead`, `crm.group_use_recurring_revenues`. CES reps presumably hold `group_sale_salesman` like other sales reps, but this wasn't cross-checked in this pass — *Unresolved.*
- `sgc_persona` addon name suggests a persona/role framework that might also touch CES, but its contents were not inspected — *Unresolved.*

**Design implication**: the future module's "who is CES" query is now concrete: `res.users` joined through `hr.employee` (`user_id`) to the current `hr.version` row (`employee_id`, filtered to latest `date_version` per employee) where `job_id` = the CES `hr.job` record. No new group or custom field is needed to identify a CES user — `hr_version.job_id` is authoritative. Tenure/gate-month calculation should use `hr_version.contract_date_start` (populated) rather than `trial_date_end` (empty) or `hr_employee.create_date` (record-creation date, not necessarily employment start).

---

## 6. CRM Pipeline Implementation

`crm_stage` table (11 stages, id/name/sequence, no PII) — *Confirmed from database metadata*:

| id | sequence | name (en_US) |
|---|---|---|
| 1 | 0 | New |
| 10 | 1 | Valid Contact |
| 8 | 2 | Outreach Email |
| 5 | 3 | No Answer |
| 7 | 4 | Not Interested |
| 6 | 5 | Follow Up |
| 2 | 6 | Research Done |
| 3 | 7 | Meeting Booked |
| 9 | 8 | Proposal |
| 4 | 9 | Won |
| 11 | 10 | No Answer - Talha Pipeline (per-rep dead-end pipeline) |
| 12 | 11 | No Answer - John Pipeline (per-rep dead-end pipeline) |

Notable: stages were created **out-of-band directly on the live DB** — `sgc_sales_playbook`'s own code comments confirm "no crm.stage data file ships in this repo." The "Proposal" gate stage id (9) and the "dead-end" stage ids (5,7,11,12) are read from `ir.config_parameter` (`sgc_sales_playbook.gate_stage_id`, `sgc_sales_playbook.gate_excluded_stage_ids`) with hardcoded fallback defaults, specifically to survive a stage reshuffle without a code deploy. — *Confirmed from source code.*

`crm_lead` has `user_id`, `team_id`, `stage_id` columns for ownership/pipeline-team structure (values not queried, per no-PII rule; only null-rates queried, see Section 17). — *Confirmed from database metadata.*

---

## 7. 45-Day Staleness — Feasibility

`crm_lead` has multiple usable date fields — *Confirmed from database metadata*:
- `date_last_stage_update` (native Odoo field — set automatically whenever `stage_id` changes)
- `x_days_since_activity` (custom integer field, likely a stored/computed staleness counter already)
- `x_last_activity_date`, `date_action_last` equivalent not directly seen but `date_automation_last` and `x_nurture_flagged_on`/`x_nurture_state` exist, suggesting a nurture-tracking mechanism already watches lead activity recency.

`sgc_sales_playbook`'s dead-lead cleanup cron (`ir_cron` name: "SGC Sales Playbook: Dead-Lead Cleanup (dry-run by default)") is architecturally the closest existing precedent for computing "stalled N days" — but it is keyed off an **activity summary marker** ("Stale Lead: set Lost Reason") + a 7-day grace period, not a raw dwell-time arithmetic threshold, specifically because the code comments state raw dwell-time arithmetic was rejected in favor of "has this lead actually been warned." A 45-day pipeline-staleness gate for CES would need its own logic (likely `date_last_stage_update` + `NOW() - INTERVAL '45 days'`), but the pattern of driving it via `ir.config_parameter`-configurable stage exclusions and a dry-run-by-default cron is directly reusable. — *Confirmed from source code (pattern) + Inferred (reusability for CES).*

A separate `ir.cron` "CRM: Redistribute Dead Leads Daily" also exists, confirming dead/stale-lead handling is an active operational concern in this system already. — *Confirmed from database metadata.*

---

## 8. Signed Proposal — Feasibility (including docuseal/signature-handler)

Two independent signature mechanisms coexist:

1. **Native Odoo `sale_order` e-sign fields** (from the standard `sale`/portal online-quote flow): `signed_on`, `client_sign_date`, `provider_sign_date`, `require_signature`, `client_signer_name`, `signed_by`, `provider_signer_name`. — *Confirmed from database metadata.* This is Odoo's built-in "sign to accept quotation" feature and does not require the `sign` app (which is `uninstallable` here anyway).

2. **Custom crm_lead signature fields** added by `sgc_crm_fields`: `x_envelope_id`, `x_signed_pdf_hash`, `x_frozen_pdf_hash`, `x_signing_actor_client`, `x_signing_actor_sgc`. — *Confirmed from database metadata + source code.* The naming (`envelope_id`, `_pdf_hash`, "signing actor") strongly suggests an external e-signature workflow feeding data back into `crm.lead`, consistent with a docuseal-style integration. However, grepping custom addon source for the literal string "docuseal" returned **zero matches** in `/mnt/extra-addons` — meaning either (a) the integration lives in a component not scanned (e.g., the `signature-handler` container, which is a separate Python service outside the Odoo codebase and was not inspected — out of scope for this Odoo-only discovery), or (b) the field names are legacy/aspirational and not actually wired to docuseal today. — *Unresolved — requires inspecting the `signature-handler` container's own code/config, not the Odoo DB, to confirm the linkage.*

No `sign.request` or equivalent Odoo Sign tables exist to check (module uninstallable). — *Confirmed from database metadata.*

**Feasibility conclusion**: "Signed proposal" detection for a CES gate could be built on `sale_order.signed_on IS NOT NULL` (native, well-supported) and/or `crm_lead.x_envelope_id IS NOT NULL` (custom, but linkage to actual docuseal completion status is unconfirmed) — the former is the safer foundation today.

---

## 9. Closed/Paid Deal — Feasibility

`sale_order.state` distribution (aggregate counts, no PII) — *Confirmed from aggregate data*:

| state | count |
|---|---|
| draft | 5 |
| sent | 2 |
| sale | 20 |

(Total 27 orders — small dataset; matches the `pg_stat_user_tables` estimate.) No orders in `cancel` or `done` state currently. `payment_state` field presence on `sale_order`/`account_move` was not separately confirmed in this pass (only sign-related and the state column were queried) — *Unresolved, needs a follow-up `information_schema.columns` check for `payment_state`.*

`account_move` has an estimated 109 rows (`pg_stat_user_tables.n_live_tup`). Standard Odoo `sale_order.state = 'sale'` (confirmed order) plus `account_move`/`account_payment` reconciliation is the standard mechanism for detecting a paid deal in unmodified Odoo, and nothing in the custom addons contradicts or replaces this — the `sgc_payment` module (installed) likely adds payment-specific logic but its contents were not inspected in this pass. — *Confirmed from database metadata (base mechanism) + Unresolved (sgc_payment specifics).*

---

## 10. Daily KPI Targets — Existing Infrastructure

`gamification` and `gamification_sale_crm` are installed with full table set present: `gamification_goal`, `gamification_goal_definition`, `gamification_challenge`, `gamification_challenge_line`, `gamification_badge`, `gamification_badge_user`, `gamification_karma_rank`, `gamification_karma_tracking`. `hr_gamification` and `sgc_employee_badges` (using `gamification_badge_data.xml`) also install. — *Confirmed from database metadata.* This is genuine, native daily/periodic-goal infrastructure (Odoo's Gamification app supports daily/weekly/monthly challenge periodicity out of the box) and is the most direct existing scaffold for a "daily KPI target" concept — whether it's actively configured with real CRM-relevant goal definitions was not queried (would require reading `gamification_goal_definition` row contents, deferred to respect the aggregate-only rule for this pass). — *Unresolved (configuration state).*

---

## 11. Monthly KPI Targets/Gates — Existing Infrastructure

No dedicated "monthly target" or "quota" model/table distinct from the Gamification challenge periodicity was found. `sgc_executive_dashboard`'s `sgc_kpi_provider.py` / `sgc_kpi_definition.py` framework is a generic, extensible KPI-definition layer (provider pattern, with per-domain providers like `provider_crm_sales.py`, `provider_commission.py`, `provider_deals.py`) that could plausibly be extended with a CES-specific provider rather than building parallel infrastructure — this looks like the more natural integration point for monthly/gate-based KPIs than Gamification. — *Confirmed from source code (existence of the provider framework) + Inferred (suitability for CES).*

---

## 12. Ownership/Historical Attribution

`crm_lead.user_id` and `crm_lead.team_id` are the native ownership columns (Confirmed from database metadata). `mail_message` has an estimated 37,686 rows system-wide (Confirmed from aggregate data) — a substantial chatter/tracking-value history exists that could support historical attribution/audit (e.g., "who moved this lead into Proposal and when"), consistent with `date_last_stage_update` plus mail.message stage-change tracking messages that Odoo generates by default. Exact per-lead attribution patterns were not queried (would require non-aggregate row inspection). — *Confirmed from aggregate data (volume) + Unresolved (attribution pattern detail).*

---

## 13. Access Control

CRM/Sales-relevant `res.groups` (XML IDs only) — *Confirmed from database metadata*: `sales_team.group_sale_salesman`, `sales_team.group_sale_salesman_all_leads`, `sales_team.group_sale_manager`, `crm.group_use_lead`, `crm.group_use_recurring_revenues`.

`sgc_sales_playbook`'s `x_gate_override_reason` field is restricted via `groups="sales_team.group_sale_manager"` at the field level, with a defense-in-depth re-check in `write()` — a good precedent for how a CES-gate override or manager-visibility field should be secured (ORM `groups=` is not sufficient alone; must also gate in `write()`/`create()` for sudo/XML-RPC/import paths). — *Confirmed from source code.*

`ir.rule` records scoped to `crm.lead` were not enumerated in this pass (time/scope-boxed) — *Unresolved.*

---

## 14. Frontend/Floating-Widget Feasibility

Strong existing precedent: `sgc_app_home/static/src/js/home_systray.js` implements a working OWL 2 systray component:

```js
/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";

export class SgcHomeSystray extends Component {
    static template = "sgc_app_home.HomeSystray";
    static props = {};
    setup() { this.action = useService("action"); }
    goHome() { this.action.doAction("sgc_app_home.action_sgc_app_home"); }
}
registry.category("systray").add(
    "sgc_app_home.HomeSystray",
    { Component: SgcHomeSystray },
    { sequence: 1 }
);
```
— *Confirmed from source code, verbatim (no secrets/PII).*

This confirms the Odoo 19 web client's `owl`-based, `registry.category("systray")` asset-bundling approach is already used and working in this codebase — a clickable floating KPI banner could follow the same registration pattern (systray icon that opens an action/dialog), or alternatively be built as a floating widget injected via a different registry (e.g., `main_components` for a persistent non-systray floating element). Other addons with popup/floating UI naming (`sgc_crm_outreach_popup`, `sgc_banne_popup`) exist as additional precedent but were not inspected in depth. — *Confirmed from source code (systray precedent) + Inferred (floating-widget extension path).*

---

## 15. Performance/Data Volume

`pg_stat_user_tables.n_live_tup` estimates (cheap, reltuples-based) — *Confirmed from aggregate data*:

| table | estimated rows |
|---|---|
| crm_lead | 14,565 |
| sale_order | 27 |
| account_move | 109 |
| mail_message | 37,686 |

These are small-to-moderate volumes; a KPI computation over `crm_lead` (e.g., 45-day staleness scan, pipeline-value sum) would be cheap even as a synchronous query, no batching/async concerns expected at this scale. `pg_indexes` on `crm_lead` was not separately enumerated in this pass. — *Unresolved (index detail); Confirmed (volume is small enough not to matter much for planning purposes).*

---

## 16. Existing Reports/Dashboards

Confirmed custom dashboard addons with CRM-relevant menus/actions: `sgc_crm_dashboard` (includes a "big screen" wallboard view), `crm_executive_dashboard` (KPI + alerting), `sgc_executive_dashboard` (generic KPI-provider framework spanning multiple business domains, not just CRM). Specific `ir_actions`/`ir_ui_menu` XML IDs were not individually enumerated in this pass (addon-file-level discovery was prioritized over exhaustive menu enumeration given the scope). — *Confirmed from source code (addon existence) + Unresolved (full menu/action XML-ID list).*

---

## 17. Data Quality Analysis

Aggregate null/populated counts on `crm_lead` (no PII, counts only) — *Confirmed from aggregate data*:

| metric | count |
|---|---|
| total rows counted (default query, likely `active=True` implicit or no filter applied) | 8,984 |
| has `user_id` | 8,982 (99.98%) |
| has `team_id` | 8,982 (99.98%) |
| has `stage_id` | 8,984 (100%) |
| has `date_last_stage_update` | 8,984 (100%) |
| has `expected_revenue` | 8,984 (100%) |

Note the discrepancy between this count (8,984) and the `pg_stat_user_tables` estimate (14,565) — likely explained by `pg_stat_user_tables` counting all rows including archived (`active=False`) leads, while this `SELECT count(*) FROM crm_lead` should actually include archived rows too since no domain/active filter was applied at the SQL level (raw SQL bypasses Odoo's ORM active-field default filter). This discrepancy is flagged as **Unresolved** and should be re-verified with an explicit `SELECT count(*), count(*) FILTER (WHERE active) FROM crm_lead` in a follow-up pass.

Data quality itself is excellent for gate-relevant fields: `stage_id`, `date_last_stage_update`, and `expected_revenue` are 100% populated, meaning a $100K pipeline gate and a 45-day staleness gate could both be computed with negligible null-handling logic. `user_id`/`team_id` are ~99.98% populated (2 leads unowned).

---

## 18. Business-Rule Reconstruction, Candidate KPI Definitions, Target Configuration, Click-Through Requirements, Unresolved Questions, Appendix

### Business-rule reconstruction (from what actually exists, not the hypothesis)

The codebase currently implements a **stage-entry qualification gate** (`sgc_sales_playbook`), not a **rep-performance/tenure gate** (the CES concept). They are complementary, not overlapping: the playbook gate stops a lead from *entering* Proposal without qualification data; a CES gate would be about a *rep's* cumulative pipeline/staleness/close performance. Both could read from the same `crm_lead` rows and the same `sgc_executive_dashboard` KPI-provider framework.

### Candidate KPI definitions (Inferred, for future design — not implemented)

- **Gate 1 (~$100K pipeline)**: `SUM(crm_lead.expected_revenue) WHERE user_id = :ces_user AND active = true AND stage_id NOT IN (won, dead-end stages)` — trivial given 100% `expected_revenue` population.
- **Gate 2 (~45-day stale proposal)**: `crm_lead WHERE stage_id = <Proposal stage id, from ir.config_parameter as sgc_sales_playbook already does> AND date_last_stage_update < NOW() - INTERVAL '45 days'` — reuse the existing config-parameter-driven stage-id pattern rather than hardcoding stage 9.
- **Gate 3 (signed proposal → closed/paid)**: `sale_order.signed_on IS NOT NULL AND state = 'sale'` as the safer native-field basis; treat `crm_lead.x_envelope_id`/`x_signed_pdf_hash` as supplementary evidence pending docuseal-linkage confirmation (Section 8).
- **Tenure**: no field found yet; would need a new field on `hr.employee`/`res.users` or derivation from `hr.employee.create_date`/contract start date (not confirmed to exist as a dedicated field).

### Target configuration design inputs (Inferred)

Follow `sgc_sales_playbook`'s established pattern: gate thresholds and stage IDs as `ir.config_parameter` entries (not hardcoded), a `mode` selection (`off`/`warn`/`block`) rather than a single on/off switch, and a manager-override wizard pattern (`gate_override_wizard.py`) logged to chatter — all directly reusable conventions.

### Click-through requirements (Inferred)

The systray precedent (`sgc_app_home`) shows the click handler pattern (`useService("action"); this.action.doAction(...)`) — a floating KPI banner's click-through would follow the same idiom, opening either a dashboard action (reusing `sgc_executive_dashboard`/`sgc_crm_dashboard` infrastructure) or a dedicated CES-gate detail view.

### Unresolved questions

1. Is `sgc_crm_dashboard` or `crm_executive_dashboard` (or `sgc_executive_dashboard`) the actively-used dashboard system? They appear to overlap.
2. Does the `docuseal` container actually write back into `crm_lead.x_envelope_id`/`x_signed_pdf_hash`, or are those fields currently unused/legacy? (Requires inspecting the `signature-handler` container, outside Odoo DB/addon scope.)
3. Is there a dedicated "CES" role anywhere in real usage (e.g., as a `crm.team` name or `hr.job` title) that wasn't caught by literal "CES" string search? Recommend a follow-up grep for "Customer Engagement" and a review of `crm_team` names (was not queried, to avoid pulling business-identifying data without clear necessity).
4. Does `sgc_payment` module implement its own paid-deal detection distinct from `account_move`/`payment_state`?
5. What does `gamification_goal_definition` actually contain — any CRM/sales goal definitions configured today?
6. Tenure tracking: does any field exist for employee start date / tenure milestones?
7. The `crm_lead` count discrepancy (8,984 vs 14,565) needs a definitive explanation.

### Source files inspected (paths only)

- `/mnt/extra-addons/sgc_sales_playbook/__manifest__.py`
- `/mnt/extra-addons/sgc_sales_playbook/models/crm_lead.py`
- `/mnt/extra-addons/sgc_app_home/static/src/js/home_systray.js`
- `/opt/odoo-prod/odoo-prod.conf` (path only, not read)
- `/mnt/extra-addons/sgc_crm_fields/models/crm_lead.py` (grep only, line numbers of matches)
- Directory listings of `/mnt/extra-addons/` (multiple `find`/`grep -l` passes, not full reads)

### Read-only SQL queries executed (verbatim)

```sql
SELECT latest_version FROM ir_module_module WHERE name='base';
SELECT name,state FROM ir_module_module WHERE state='installed' ORDER BY name;
SELECT name,state FROM ir_module_module WHERE name IN ('sign');
SELECT key FROM ir_config_parameter WHERE key ILIKE '%docuseal%' OR key ILIKE '%sign%';
SELECT column_name,data_type FROM information_schema.columns WHERE table_name='crm_lead' AND (column_name ILIKE '%date%' OR column_name ILIKE '%stage%' OR column_name ILIKE '%user%' OR column_name ILIKE '%team%' OR column_name ILIKE 'x_%') ORDER BY column_name;
SELECT id,name,sequence FROM crm_stage ORDER BY sequence;
SELECT state,count(*) FROM sale_order GROUP BY state;
SELECT column_name FROM information_schema.columns WHERE table_name='sale_order' AND (column_name ILIKE '%sign%' OR column_name ILIKE '%payment_state%');
SELECT tablename FROM pg_tables WHERE tablename ILIKE 'gamification%';
SELECT module, name FROM ir_model_data WHERE model='res.groups' AND module IN ('sales_team','crm');
SELECT cron_name FROM ir_cron WHERE cron_name ILIKE '%gate%' OR cron_name ILIKE '%dead%' OR cron_name ILIKE '%stale%' OR cron_name ILIKE '%kpi%' OR cron_name ILIKE '%nurture%';
SELECT relname, n_live_tup FROM pg_stat_user_tables WHERE relname IN ('crm_lead','sale_order','account_move','mail_message');
SELECT column_name FROM information_schema.columns WHERE table_name='hr_employee' AND column_name ILIKE '%job%';
SELECT count(*) total, count(user_id) has_user, count(team_id) has_team, count(stage_id) has_stage, count(date_last_stage_update) has_dlsu, count(expected_revenue) has_exprev FROM crm_lead;
```

Failed/errored queries (schema-mismatch, no data returned, no PII exposed): a `job_title` column query and an `imd.complete_name` join both errored against actual schema and were corrected/abandoned respectively.

### Access limitations

None blocking — SSH, docker exec, and DB access all worked throughout. Two queries hit real schema mismatches (`hr_employee.job_title` does not exist as a plain column; `ir_model_data` has no `complete_name` column in this version) and were not exhaustively chased down given the discovery-only scope and time-boxing; flagged as Unresolved rather than blockers.

```json
{
  "environment": {
    "odoo_version": "19.0.1.3",
    "version_source": "ir_module_module.base.latest_version",
    "db_name": "odoo19-sgc",
    "containers": ["odoo-prod", "odoo-prod-db", "odoo19-sgc-staging (untouched)", "sgc_staging (untouched)", "docuseal", "signature-handler"],
    "extra_addons_host_path": "/opt/odoo-prod/extra-addons",
    "extra_addons_container_path": "/mnt/extra-addons"
  },
  "ces_role": {
    "found": true,
    "model": "hr.job",
    "job_id": 1,
    "job_title": "Telesales/Client Engagement Specialist",
    "identification_method": "hr_version.job_id = 1, joined to hr_employee via employee_id, joined to res_users via hr_employee.user_id",
    "active_employee_count": 4,
    "inactive_employee_count": 0,
    "employees_with_linked_user": 4,
    "distinct_manager_count": 2,
    "distinct_department_count": 2,
    "active_crm_lead_owned_count": 1832,
    "group_xml_ids": [],
    "candidate_representations_note": "role already exists via hr.job; no new group/field needed",
    "existing_related_addon": "sgc_persona (contents not inspected)"
  },
  "tenure": {
    "field_found": true,
    "model": "hr.version",
    "start_date_field": "contract_date_start",
    "start_date_range_across_ces": "2026-06-02 to 2026-08-06",
    "trial_date_end_populated": false,
    "notes": "Odoo 19 moved job/contract data off hr_employee onto hr.version (hr_version table); hr_employee.job_id/job_title do not exist directly. trial_date_end field exists on hr_version but is empty for all 4 CES employees, so probation-based gate timing is not currently derivable; contract_date_start is populated and is the best available tenure-start candidate."
  },
  "pipeline": {
    "stage_table": "crm_stage",
    "stage_count": 11,
    "gate_stage_id_pattern": "ir.config_parameter sgc_sales_playbook.gate_stage_id, default 9 (Proposal)",
    "date_last_stage_update_populated_pct": 100.0,
    "expected_revenue_populated_pct": 100.0
  },
  "signed_proposal": {
    "native_sign_module_installed": false,
    "native_sign_module_state": "uninstallable",
    "sale_order_signature_fields": ["signed_on","client_sign_date","provider_sign_date","require_signature","client_signer_name","signed_by","provider_signer_name"],
    "crm_lead_custom_signature_fields": ["x_envelope_id","x_signed_pdf_hash","x_frozen_pdf_hash","x_signing_actor_client","x_signing_actor_sgc"],
    "docuseal_source_linkage_found": false,
    "docuseal_container_present": true
  },
  "paid_deal": {
    "sale_order_state_distribution": {"draft": 5, "sent": 2, "sale": 20},
    "account_move_row_estimate": 109,
    "payment_state_column_confirmed": null
  },
  "targets": {
    "gamification_installed": true,
    "gamification_tables_present": true,
    "gamification_configured_for_crm": null,
    "kpi_provider_framework": "sgc_executive_dashboard (sgc_kpi_provider.py, sgc_kpi_definition.py, providers/*)"
  },
  "frontend": {
    "owl_version_confirmed": "owl 2 (via @odoo/owl import)",
    "systray_precedent_found": true,
    "systray_precedent_file": "sgc_app_home/static/src/js/home_systray.js",
    "other_popup_precedents": ["sgc_crm_outreach_popup", "sgc_banne_popup"]
  },
  "security": {
    "crm_sales_groups": ["sales_team.group_sale_salesman","sales_team.group_sale_salesman_all_leads","sales_team.group_sale_manager","crm.group_use_lead","crm.group_use_recurring_revenues"],
    "field_level_group_restriction_precedent": "sgc_sales_playbook x_gate_override_reason (groups= plus write() re-check)",
    "ir_rule_crm_lead_enumerated": false
  },
  "performance": {
    "crm_lead_row_estimate": 14565,
    "sale_order_row_estimate": 27,
    "account_move_row_estimate": 109,
    "mail_message_row_estimate": 37686
  },
  "confirmed_rules": [
    "crm.lead has date_last_stage_update, x_days_since_activity for staleness computation",
    "Proposal stage id and dead-end stage ids are config-parameter-driven, not hardcoded, in sgc_sales_playbook",
    "gamification module and tables are installed",
    "sgc_app_home systray component is a working OWL floating/clickable UI precedent",
    "native sign module is uninstallable; sale_order has its own native e-sign fields instead"
  ],
  "unresolved_questions": [
    "Which of sgc_crm_dashboard / crm_executive_dashboard / sgc_executive_dashboard is authoritative",
    "Whether docuseal container actually writes into crm_lead.x_envelope_id/x_signed_pdf_hash",
    "Whether a CES-equivalent role exists under different naming (crm.team name, hr.job title)",
    "Whether sgc_payment implements custom paid-deal detection",
    "Contents/configuration of gamification_goal_definition",
    "Tenure tracking field existence",
    "crm_lead total row count discrepancy (8,984 vs 14,565 estimate)"
  ],
  "source_files_inspected": [
    "/mnt/extra-addons/sgc_sales_playbook/__manifest__.py",
    "/mnt/extra-addons/sgc_sales_playbook/models/crm_lead.py",
    "/mnt/extra-addons/sgc_app_home/static/src/js/home_systray.js"
  ],
  "read_only_queries_executed": [
    "SELECT latest_version FROM ir_module_module WHERE name='base';",
    "SELECT name,state FROM ir_module_module WHERE state='installed' ORDER BY name;",
    "SELECT name,state FROM ir_module_module WHERE name IN ('sign');",
    "SELECT key FROM ir_config_parameter WHERE key ILIKE '%docuseal%' OR key ILIKE '%sign%';",
    "SELECT column_name,data_type FROM information_schema.columns WHERE table_name='crm_lead' AND (column_name ILIKE '%date%' OR column_name ILIKE '%stage%' OR column_name ILIKE '%user%' OR column_name ILIKE '%team%' OR column_name ILIKE 'x_%') ORDER BY column_name;",
    "SELECT id,name,sequence FROM crm_stage ORDER BY sequence;",
    "SELECT state,count(*) FROM sale_order GROUP BY state;",
    "SELECT column_name FROM information_schema.columns WHERE table_name='sale_order' AND (column_name ILIKE '%sign%' OR column_name ILIKE '%payment_state%');",
    "SELECT tablename FROM pg_tables WHERE tablename ILIKE 'gamification%';",
    "SELECT module, name FROM ir_model_data WHERE model='res.groups' AND module IN ('sales_team','crm');",
    "SELECT cron_name FROM ir_cron WHERE cron_name ILIKE '%gate%' OR cron_name ILIKE '%dead%' OR cron_name ILIKE '%stale%' OR cron_name ILIKE '%kpi%' OR cron_name ILIKE '%nurture%';",
    "SELECT relname, n_live_tup FROM pg_stat_user_tables WHERE relname IN ('crm_lead','sale_order','account_move','mail_message');",
    "SELECT column_name FROM information_schema.columns WHERE table_name='hr_employee' AND column_name ILIKE '%job%';",
    "SELECT count(*) total, count(user_id) has_user, count(team_id) has_team, count(stage_id) has_stage, count(date_last_stage_update) has_dlsu, count(expected_revenue) has_exprev FROM crm_lead;"
  ]
}
```

```
Production modification status: NONE
Investigation mode: READ-ONLY
Secrets included: NONE
PII included: NONE
```
