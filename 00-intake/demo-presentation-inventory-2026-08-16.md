# demo_presentation — Read-Only Evidence Inventory

**Date**: 2026-08-16
**Host**: SSH alias `vps-root` (alias `contabo-sgc` in the original instruction — this session connects to the same physical server via `vps-root`, the alias recorded on this machine; confirmed same server by matching container names/IPs to prior session records).
**Method**: Read-only `psql` (`PGOPTIONS='-c default_transaction_read_only=on -c statement_timeout=15000'`, `-v ON_ERROR_STOP=1`) and read-only `docker`/filesystem inspection. No INSERT/UPDATE/DELETE/CREATE/DROP/ALTER/TRUNCATE/VACUUM/ANALYZE/pg_dump/pg_restore was run. No Odoo module install/upgrade, no container restart, no config edit.

---

## 1. LOCATION (Phase 1)

**`demo_presentation` is NOT on the production Postgres instance.** It lives on its own dedicated Postgres container.

- Postgres container: **`demo_presentation_db`** (image `postgres:16`), network `demo_presentation_default`, IP **172.21.0.2**. Confirmed by `\l` showing a database literally named `demo_presentation` on this container and on no other reachable Postgres instance (`postgres-staging`, `demo_presentation_staging_db`, `odoo-test-db`, `odoo-prod-db`, `cip-db` were all checked — see §3 evidence log).
- `odoo-prod-db` (172.19.0.2, the production instance) holds only `odoo19-sgc` and `odoo_gmail_addin` — no `demo_presentation` database exists there.
- Odoo application container: **`demo_presentation`** (image `odoo:19.0`, port 127.0.0.1:18030→8069). Its running process command line is `--db-filter=^demo_presentation$` — this **does** match the database, so it is currently servable. Its `odoo.conf` on disk carries no `dbfilter`/`db_name` at all; the actual filter comes from a command-line flag not reflected in the config file.
- **Notable, distinct fact — not the same as "on production," but adjacent**: the `demo_presentation` *container* has a second network interface on `odoo-prod_odoo-prod-network` (172.19.0.7), alongside `odoo-prod` (172.19.0.6) and `odoo-prod-db` (172.19.0.2). Its actual DB connection (`HOST=db` resolves to 172.21.0.2, confirmed via `getent hosts db` run inside the container) goes to its own dedicated Postgres, not to prod. Flagged because network-adjacency to production is a real fact about this box's topology, even though the database itself is isolated.
- Database size: **167 MB** (`pg_size_pretty(pg_database_size('demo_presentation'))`).
- Database container created: **2026-07-04** (`docker inspect .Created`). Earliest real record (`min(create_date)` across `res_users`/`res_partner`/`ir_module_module`): **2026-07-04 21:21:07**. Earliest `crm_lead`: **2026-07-22**.
- Last activity: `max(write_date)` — `res_users`/`res_partner` 2026-08-16 13:08:13, `mail_message` 2026-08-16 13:00:56, `ir_attachment` 2026-08-16 08:13:06, `crm_lead` 2026-08-14 10:58:30. **Caveat**: recent writes on `res_users`/`res_partner` coincide with the container having been restarted ~16 minutes before this session started (`docker ps` showed "Up 16 minutes") — this could be session/login bookkeeping triggered by restart, not necessarily human activity. Not asserted as proof of active human use.
- `05-ops/db_guard.py`: **does not exist** — searched this repository (`Glob **/db_guard*` → no match) and the entire VPS filesystem (`find / -iname 'db_guard.py'` → no match). There was no tool to be refused by; proceeded directly with read-only `psql` per the instruction's own fallback.

---

## 2. VERDICT — CODE vs. DATABASE (Phase 2)

**The custom capability set is split roughly 29 tracked / 5 fully untracked at the module level, plus a materially-sized layer of true DB-only view customization.** Numbers, not impression:

| Category | Count | Detail |
|---|---|---|
| Custom/SGC-relevant module directories surveyed | 34 | 30 installed + 4 present-but-not-installed (`crm_executive_dashboard`, `ks_dynamic_financial_report`, `module_generator_v19`, `sgc_realestate_website`) |
| — fully git-tracked (redeployable from repo) | 29 | e.g. `sgc_offplan_rental_property_management` (581/584 files tracked, gap = `__pycache__`/one stray script, verified), `sgc_construction_management`, `sgc_commission`, `sgc_deals_management`, etc. |
| — **fully git-UNTRACKED** ("EXISTS ONLY ON THE BOX") | 5 | `sgc_crm_dashboard` (139 files, 0 tracked, **installed**), `crm_lead_ingestion_hub` (50 files, 0 tracked, **installed**), `aml_compliance` (58 files, 0 tracked, **installed**), `sgc_executive_dashboard` (80 files, 0 tracked, **installed**), `crm_executive_dashboard` (42 files, 0 tracked, not installed) |
| Modified-but-uncommitted change to a vendor/OCA module | 1 | `hr_payroll_community/models/hr_employee.py` — local edit sitting uncommitted in a third-party module |
| Manual (Studio) fields (`ir_model_fields.state='manual'`) | 2 | `account.analytic.line.x_plan2_id`, `project.project.x_plan2_id` (both "Construction Projects") |
| Manual models (`ir_model.state='manual'`) | 0 | — |
| Orphan views (`ir_ui_view` with no `ir_model_data` row) | 92 | 6 tied to real business models (see below); 86 appear to be website/theme snippet definitions (Paptic theme, page-builder snippets) by naming pattern — **not individually verified as orphan-by-design vs. true DB-only customization**, flagged as UNVERIFIED at that granularity |
| — of which, tied to a real business model | 6 | `property.project` (2, **archived/inactive**), `property.sub.project` (2, **archived/inactive**), `tenancy.details` (2, **active** — confirmed via prior-session memory note, §7, and cross-checked live: these are legitimately the only views for that model) |
| `ir_actions_server` with no module xml_id | 2 | Both belong to firing crons (#95/#96, "Web Research: Purge..."), unrelated to any catalogued SGC module |
| `base_automation` rows with no xml_id | N/A | **`base_automation` module is not installed** (`ir_module_module.state='uninstalled'`) — the table doesn't exist |
| `ir_cron` with no module xml_id | 0 | All 53 cron rows trace to a module xml_id |

**Reading this plainly**: the bulk of the *business logic* (Python models, security, most views) is code, and most of that code is in git. But four of the **installed, live** capabilities — the CRM dashboard, the lead-ingestion webhook hub, the AML compliance module, and the executive dashboard — exist **only as files on this one server**, in no repository. If this box is lost, those four modules are gone. Separately, a real (if small) amount of view-level customization exists only as database rows with no code counterpart at all.

---

## 3. EVIDENCE LOG — commands and verbatim output

### 3.1 Locate the database

```
$ ssh vps-root "docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'"
```
(Full output in session; relevant rows:)
```
demo_presentation              odoo:19.0                                 Up 16 minutes          8071/tcp, 127.0.0.1:18030->8069/tcp, 127.0.0.1:18031->8072/tcp
demo_presentation_staging      odoo:19.0                                 Up 5 weeks             8071/tcp, 0.0.0.0:18040->8069/tcp, 0.0.0.0:18041->8072/tcp
demo_presentation_staging_db   postgres:16                                Up 5 weeks (healthy)
demo_presentation_db           postgres:16                                Up 3 weeks (healthy)
odoo-prod-db                   postgres:16                                Up 8 weeks (healthy)
```

```
$ ssh vps-root "docker exec -e PGOPTIONS=... demo_presentation_db psql -v ON_ERROR_STOP=1 -U odoo -d postgres -c '\l'"
                                                       List of databases
       Name        | Owner
-------------------+-------
 demo_presentation | odoo
 postgres          | odoo
 template0         | odoo
 template1         | odoo
```
(`postgres-staging`, `demo_presentation_staging_db`, `odoo-test-db`, `odoo-prod-db`, `cip-db` were each queried the same way — none list a database named `demo_presentation`. `odoo-prod-db` lists only `odoo19-sgc`, `odoo_gmail_addin`, `postgres`.)

```
$ ssh vps-root "docker exec demo_presentation ps aux | grep -i odoo"
odoo   1  ...  /usr/bin/python3 /usr/bin/odoo --db_host=db --db_user=odoo --db_password=[REDACTED]
  --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons
  --log-level=warn --db-filter=^demo_presentation$ --db_host db --db_port 5432 --db_user odoo --db_password [REDACTED]
```

```
$ ssh vps-root "docker exec demo_presentation getent hosts db"
172.21.0.2      db
```
(172.21.0.2 = `demo_presentation_db`, confirmed via `docker inspect`.)

```
$ ssh vps-root "docker inspect demo_presentation --format '{{json .NetworkSettings.Networks}}'"
```
→ two networks: `demo_presentation_default` (172.21.0.3) and `odoo-prod_odoo-prod-network` (172.19.0.7).

```
$ docker exec ... psql ... -c "SELECT pg_size_pretty(pg_database_size('demo_presentation'));"
 167 MB
```

```
$ docker exec ... psql ... -c "SELECT 'res_users' t, max(write_date) mx FROM res_users UNION ALL ... "
       t       |             mx
---------------+----------------------------
 res_users     | 2026-08-16 13:08:13.693505
 res_partner   | 2026-08-16 13:08:13.693505
 ir_attachment | 2026-08-16 08:13:06.518899
 crm_lead      | 2026-08-14 10:58:30.531785
 mail_message  | 2026-08-16 13:00:56.278208
```

```
$ docker inspect -f '{{.Name}} Created={{.Created}}' demo_presentation demo_presentation_db demo_presentation_staging demo_presentation_staging_db
/demo_presentation Created=2026-07-26T13:43:11Z
/demo_presentation_db Created=2026-07-04T20:58:40Z
/demo_presentation_staging Created=2026-07-09T18:51:55Z
/demo_presentation_staging_db Created=2026-07-09T18:50:13Z
```

### 3.2 Git tracking of the addons repo

Host path (bind-mounted as `/mnt/extra-addons`): `/opt/odoo/demo_presentation/addons`.

```
$ ssh vps-root "git -C /opt/odoo/demo_presentation/addons status"
On branch main
Your branch is up to date with 'origin/main'.
Changes not staged for commit:
        modified:   hr_payroll_community/models/hr_employee.py
Untracked files:
        _stock_icons/
        account_statement_base/  account_statement_import_base/  account_statement_import_file/
        account_statement_import_sheet_file/  account_statement_import_sheet_file_xlsx/
        aml_compliance/
        crm_executive_dashboard/
        crm_lead_ingestion_hub/
        kyc_management/controllers/.claude/
        sgc_crm_dashboard/
        sgc_design_tokens/static/src/img/
        sgc_executive_dashboard/
        sgc_lead_scoring/models/llm_service.py.bank
        sgc_lead_scoring/models/website_scan.py
        sgc_lead_scoring/tests/test_website_scan.py
        sgc_offplan_rental_property_management/verify_luxury.py
        sgc_scroll_hero_v2/static/src/fonts/
        sgc_scroll_hero_v2/static/src/js_tmp_check/
        sgc_ui_brand_palette/static/icons.orig-backup-20260726/
        uae_einvoice_core/static/
```

```
$ git remote -v
origin  gh-demo-addons:samanabran/demo.git (fetch/push)
$ git log -1
commit 9d71007d59965fca520a28f4fa443e63d5c74d0a
Date: Thu Jul 30 00:28:25 2026 +0200
"Rebrand display font Fraunces->Gambetta, polish scroll-hero timing, fix black landing frame..."
```

Per-module manifest survey (name/version/summary/depends/external deps/data-view count/tracked-file count) was run for all 34 custom/SGC module directories via a single batched script (manifest parsed with `ast.literal_eval`, `git ls-files` per directory, `git status --porcelain` per directory). Full per-module output is reproduced in §4 below (Module Tables). The five 0%-tracked modules were double-checked individually — each shows `?? <module>/` as a single untracked-directory line in `git status --porcelain`, confirming zero files of that module are in any commit.

Two "tracked % less than 100%" cases were verified as **not** real gaps:
```
$ git status --porcelain --ignored sgc_dynamic_financial_report sgc_ui_brand_palette sgc_offplan_rental_property_management
?? sgc_offplan_rental_property_management/verify_luxury.py
?? sgc_ui_brand_palette/static/icons.orig-backup-20260726/
!! sgc_dynamic_financial_report/controllers/__pycache__/
!! sgc_dynamic_financial_report/models/__pycache__/
!! sgc_dynamic_financial_report/reports/__pycache__/
!! sgc_offplan_rental_property_management/ops/ops.env
!! sgc_offplan_rental_property_management/report/__pycache__/
```
`sgc_dynamic_financial_report`'s 67/84-tracked gap is `__pycache__` (gitignored, not a real gap). `sgc_ui_brand_palette`'s 28/51 gap: confirmed by direct count that `icons.orig-backup-20260726/` contains exactly 23 files (`find ... -type f | wc -l` → `23`), which fully accounts for the 51−28=23 difference.

**`sgc_offplan_rental_property_management/ops/ops.env` exists, is gitignored, 25 bytes** (`ls -la` → `-rw-r--r-- 1 197609 197609 25 Jul 12 22:00 ... ops.env`). **Not read** — flagged for §6.4 as a client/deployment-specific artifact requiring handling before reuse, contents unverified by this audit on purpose.

### 3.3 Filesystem search for related artifacts

```
$ ssh vps-root "find / -iname 'db_guard.py' 2>/dev/null"
(no output)
$ ssh vps-root "find / -maxdepth 6 -iname '*demo_presentation*' -o -iname '*demo-presentation*' 2>/dev/null"
```
Relevant hits (redacted where credential-bearing):
```
/backups/demo_presentation/demo_presentation-20260719T081008Z.dump
/backups/demo_presentation/demo_presentation-20260719T074308Z.dump
/opt/backups/demo_presentation_emergency_20260726.dump
/opt/odoo/demo_presentation/db_backups/demo_presentation_pre_ksdfr_update_20260718_093831.dump
/opt/odoo/demo_presentation/db_backups/demo_presentation_pre_stmt_import_install_20260718_110714.dump
/root/backups/demo_presentation_pre_image_migration_20260725_060019.dump
/root/addons-export/demo_presentation-addons.tar.gz
/root/addons-export/demo_presentation_staging-addons.tar.gz
/opt/backups/demo_presentation_extra-addons_20260706_215236.tar
/tmp/demo_presentation_addons_snapshot.tar.gz
/opt/odoo/demo_presentation/demo_presentation_introspect.py
/opt/odoo/demo_presentation/demo_presentation_migrate.py
/opt/odoo/demo_presentation/demo_presentation_migrate_gallery.py
/opt/odoo/demo_presentation/demo_presentation_seed_website.py
/opt/odoo/demo_presentation/demo_presentation_verify.py
/opt/odoo/demo_presentation/demo_presentation_verify_website.py
/root/.ssh/deploy_keys/demo_presentation-addons(.pub)
/root/.demo_presentation_admin_passwd_20260726
```
**None of the `.dump` files were opened** (pg_dump/pg_restore and reading dump contents were out of scope for read-only DB inspection — these are backup artifacts, not something this audit inspected). **`/root/.demo_presentation_admin_passwd_20260726` was not read** — flagged only as a security-relevant artifact name (a file whose name implies it stores the Odoo master password in plaintext on the host) for whoever owns credential hygiene here; not verified, not opened.

**`demo_presentation_seed_website.py` / `demo_presentation_migrate.py` / `demo_presentation_migrate_gallery.py` exist at `/opt/odoo/demo_presentation/` — outside the `addons/` git repository entirely.**
```
$ ssh vps-root "git -C /opt/odoo/demo_presentation status"
fatal: not a git repository (or any of the parent directories): .git
```
These are one-off data-seeding/migration scripts with no repository of their own. This is concrete evidence that at least some of the data in this database was populated by ad-hoc script, not by module-shipped `data/*.xml` — installing the modules on a fresh database would **not** reproduce whatever these scripts did.

### 3.4 Prior-session memory note (read for context, not part of the DB)

`/root/.claude/projects/-opt-merged-addons/memory/demo-presentation-rental-suite.md` — a note from an earlier Claude Code session working on this same box, describing an orphan-view bug in `property.project`/`tenancy.details` views (module rename from a predecessor `rental_management` module lost the `ir_model_data` xmlids) and a fix applied 2026-07-09 (archiving views 2904/2905/3011/3012). **This claim was independently verified against the live database, not taken on faith:**
```
$ psql ... -c "SELECT id, model, name, active, priority FROM ir_ui_view WHERE id IN (2904,2905,3011,3012,2906,2907,2908,2909,2999) ORDER BY id;"
  id  |       model        |          name              | active
------+---------------------+----------------------------+-------
 2904 | property.project    | property.project.tree      | f
 2905 | property.sub.project | property.sub.project.tree | f
 2906 | tenancy.details     | tenancy.details.tree        | t
 2907 | tenancy.details     | tenancy.details.form        | t
 3011 | property.project    | property.project.form      | f
 3012 | property.sub.project | property.sub.project.form | f
```
**Confirmed accurate**: the four claimed-archived views are `active=f`; the two claimed-must-not-touch views (`tenancy.details`) are `active=t`, matching the memory's own reasoning. Three other IDs the memory referenced (2908/2909/2999, `property.vendor`/`property.details`) returned **no rows at all** — not present in `ir_ui_view` today, a discrepancy against the memory noted but not chased further. The memory also names the database `demo_presentation_19`; the live database is named `demo_presentation` (`SELECT current_database()` → `demo_presentation`) — a minor inaccuracy in the memory note, stated plainly.

**The memory note also contains demo portal login credentials in plaintext** (tenant/landlord test accounts). **Redacted from this report per the standing constraint** — logins are listed in §5.4 without their passwords.

### 3.5 Module state, git survey, and full SQL evidence

Full 34-module manifest/git survey output, and all Phase 2.4/3/4/5 SQL (manual fields, orphan views, cron table, module list, row counts, crm_lead breakdown, mail state, report actions, PDF attachments, ir_rule/ir_model_access, Python package/wkhtmltopdf checks) were run exactly as specified (read-only session settings, `ON_ERROR_STOP=1`, `reltuples`-first policy) over the course of this audit. Selected verbatim results are reproduced inline in §4–§6 below rather than duplicated twice; every number in those sections traces to a query run this session, listed in full in the session transcript. Two queries hit real (non-timeout) SQL errors and were corrected rather than retried blind:
- `base_automation` table: `ERROR: relation "base_automation" does not exist` → confirmed via `SELECT name,state FROM ir_module_module WHERE name='base_automation'` → `uninstalled`. Table genuinely doesn't exist; not a typo.
- `ir_cron.model_id`: `ERROR: column c.model_id does not exist` → corrected via `\d ir_cron` (cron links to a model through `ir_actions_server_id`, not a direct `model_id` column).

No query timed out under the 15-second `statement_timeout`; none was abandoned.

---

## 4. MODULE TABLES

### 4.1 Installed modules — `SELECT name, shortdesc, state, latest_version, author FROM ir_module_module WHERE state IN (...)`

**163 modules installed.** Bucketed by `author` field (not guessed):

| Bucket | Count | Basis |
|---|---|---|
| Odoo core/standard (`author = 'Odoo S.A.'` or `'odoo'`) | ~120 | e.g. `base`, `crm`, `sale`, `account`, `hr`, `mail`, `website`, `hr_attendance`, `hr_holidays`... |
| Third-party / OCA | ~14 | `report_xlsx` (ACSONE/Creu Blanca/OCA), `account_statement_*` (Akretion/ForgeFlow/Tecnativa/OCA), `hr_payroll_community` (Cybrosys Techno Solutions), `muk_mcp`/`muk_web_utils` (MuK IT), `global_button_color_coding` (author `Custom`, ambiguous — not clearly SGC or third-party from the field alone) |
| SGC-authored (`author` contains `SGC`) | 27 | `sgc_construction_management`, `sgc_design_tokens`, `sgc_fix_context_eval` (author `SGC`); `eh_uae_payroll_wps` (author `SGC Construction`); `crm_lead_ingestion_hub` (author `SGC TECH`); `aml_compliance`, `kyc_management`, `sgc_ai_powerbox`, `sgc_appraisal`, `sgc_assessment`, `sgc_commission`, `sgc_deals_management`, `sgc_dynamic_financial_report`, `sgc_elearning`, `sgc_employment_certificate`, `sgc_executive_dashboard`, `sgc_hr_memos`, `sgc_invoicing_dashboard`, `sgc_lead_scoring`, `sgc_offplan_rental_property_management`, `sgc_recruitment`, `sgc_tech_ai_theme`, `sgc_ui_brand_palette`, `sgc_video_conferencing` (author `SGC TECH AI`); `sgc_crm_dashboard` (author `Cybrosys Technologies, SGC TECH AI` — mixed/co-authored) |
| `author` field blank, but named like SGC's own convention | 2 | `sgc_brochure_leadcapture`, `sgc_llm_router` — manifest declares no author at all; grouped here by naming convention only, **not** asserted as verified authorship |

Not installed but present on disk: `crm_executive_dashboard`, `ks_dynamic_financial_report`, `module_generator_v19` (no `__manifest__.py` at all — not a real Odoo module directory), `sgc_realestate_website`.

### 4.2 Demo data

```
SELECT name, demo FROM ir_module_module WHERE demo=true;
(0 rows)
```
No module has ever loaded its demo dataset. `res_company`:
```
 id | name
  1 | My Company
  2 | test
```
A second company literally named **"test"** exists alongside the default "My Company" placeholder — neither has been renamed to a real business identity. Checked for classic Odoo demo partner names (`Azure Interior`, `Deco Addict`, `Gemini Furniture`, `Wood Corner`, `Tony Fred`, `Ready Mat`) — **0 rows**, none present.

### 4.3 Per-module manifest + git-tracking survey (all 34 custom/SGC modules)

Full table (name / version / summary / depends / external deps / data-view file count / total files / git-tracked files):

| Module | Version | Depends (key) | External deps | data/views XML | Files (total / tracked) |
|---|---|---|---|---|---|
| sgc_brochure_leadcapture | 19.0.1.0.0 | website, crm, sgc_offplan... | — | 1 | 7 / 7 |
| sgc_llm_router | 19.0.1.0.1 | base, muk_mcp | — | 2 | 8 / 8 |
| global_button_color_coding | 19.0.1.0.0 | web, base | — | 0 | 5 / 5 |
| **sgc_crm_dashboard** | 19.0.1.2.0 | base, web, crm, sale_management, mail, portal, website | — | 19 | **139 / 0** |
| sgc_construction_management | 19.0.2.2 | base, mail, product, uom, account, report_xlsx, portal | — | 21 | 202 / 202 |
| sgc_design_tokens | 19.0.1.1.0 | web | — | 2 | 11 / 10 (gap = gitignored img dir) |
| sgc_fix_context_eval | 19.0.2.0.0 | base, web | — | 0 | 6 / 6 |
| sgc_scroll_hero_builder | 19.0.1.0.0 | website, sgc_scroll_hero_* | — | 0 | 4 / 4 |
| sgc_scroll_hero_homepage | 19.0.1.0.0 | website, sgc_offplan..., sgc_design_tokens | — | 4 | 253 / 253 |
| sgc_scroll_hero_v2 | 19.0.1.0.0 | website, sgc_offplan... | — | 4 | 238 / 234 |
| sgc_static_pages | 19.0.1.0.0 | website, sgc_design_tokens, sgc_offplan... | — | 3 | 5 / 5 |
| eh_uae_payroll_wps | 19.0.1.0.0 | hr_payroll_community, hr, report_xlsx | — | 3 | 20 / 20 |
| **crm_lead_ingestion_hub** | 19.0.1.0.0 | crm, mail, utm | — | 4 | **50 / 0** |
| **aml_compliance** | 19.0.1.0.0 | base, mail, kyc_management, account | — | 21 | **58 / 0** |
| kyc_management | 19.0.1.0.1 | base, contacts, mail, portal, web, website, crm | — | 7 | 38 / 37 (gap = stray `.claude` dir) |
| sgc_ai_powerbox | 1.5.5 | web | — | 0 | 5 / 5 |
| sgc_appraisal | 19.0.1.2 | hr, survey | — | 11 | 96 / 96 |
| sgc_assessment | 19.0.2.2 | base, web, portal, mail, hr_recruitment | **openai, anthropic, tiktoken, numpy, pandas** | 16 | 68 / 68 |
| sgc_commission | 19.0.4.0 | base, sale, purchase, account, project | (declared, empty list) | 25 | 73 / 73 |
| sgc_deals_management | 19.0.3.0 | base, sale, purchase, account, mail, hr, utm, sgc_commission | (declared, empty list) | 6 | 45 / 45 |
| sgc_dynamic_financial_report | 19.0.1.0.0 | account, report_xlsx, web, analytic, mail | — | 6 | 84 / 67 (gap = `__pycache__`, verified) |
| sgc_elearning | 19.0.1.2 | base, mail | — | 4 | 24 / 24 |
| sgc_employment_certificate | 19.0.1.1 | hr, mail, website | — | 5 | 36 / 36 |
| **sgc_executive_dashboard** | 19.0.1.1.0 | base, web | — | 4 | **80 / 0** |
| sgc_hr_memos | 19.0.2.1 | hr, mail, website | — | 3 | 26 / 26 |
| sgc_invoicing_dashboard | 19.0.2.1 | sale, account | — | 5 | 47 / 47 |
| sgc_lead_scoring | 19.0.1.8 | base, crm, mail | **requests** | 7 | 77 / 73 (gap = 3 untracked new/backup files) |
| sgc_offplan_rental_property_management | 19.0.2.26 | base, web, mail, contacts, account, hr, maintenance, crm, website, portal, sgc_commission, sgc_design_tokens | — | 73 | 584 / 581 |
| sgc_recruitment | 19.0.1.1 | base, hr, hr_recruitment, crm, mail | — | 3 | 27 / 27 |
| sgc_tech_ai_theme | 19.0.1.0.0 | web | — | 2 | 112 / 112 |
| sgc_ui_brand_palette | 19.0.1.0.2 | base, web, mail, calendar, contacts, crm, hr, account, ... (22 deps) | — | 1 | 51 / 28 (gap = gitignored icon backup, verified = 23 files) |
| sgc_video_conferencing | 19.0.1.2 | base_setup, mail, calendar, crm, sale_management, project, hr, hr_recruitment, contacts | **google_auth_oauthlib, google-api-python-client, requests, cryptography** | 19 | 104 / 104 |
| **crm_executive_dashboard** (not installed) | 19.0.1.1.0 | base, web, crm, sale_management, mail, portal, website | — | 11 | **42 / 0** |
| ks_dynamic_financial_report (not installed) | 19.0.1.0.0 | base, mail, account, sale_management | — | 8 | 126 / 126 |
| module_generator_v19 (not installed) | — | **no `__manifest__.py` found** | — | 0 | 44 / 44 |
| sgc_realestate_website (not installed) | 19.0.1.1.0 | base, web, website, website_mail, portal, mail | — | 11 | 58 / 58 |

### 4.4 Database-only customization (detail)

```
SELECT count(*) FROM ir_model_fields WHERE state='manual';  →  2
 model                   | name        | descr
 account.analytic.line   | x_plan2_id  | Construction Projects
 project.project         | x_plan2_id  | Construction Projects

SELECT count(*) FROM ir_model WHERE state='manual';  →  0

SELECT count(*) FROM ir_ui_view v WHERE NOT EXISTS (... ir_model_data ...);  →  92
SELECT count(*) FROM ir_act_server a WHERE NOT EXISTS (...);  →  2
  id=1079 model_id=2132 "Web Research: Purge Audit Log (90 days)"
  id=1080 model_id=2131 "Web Research: Purge Expired Cache (7 days)"
SELECT count(*) FROM ir_cron c WHERE NOT EXISTS (...);  →  0
```

---

## 5. DATA TABLES

### 5.1 Row counts (Phase 4.1)

Core tables (`pg_class.reltuples`, already analyzed):

| Table | Est. rows |
|---|---|
| ir_attachment | 3,977 |
| mail_message | 1,667 |
| account_move | 105 |
| res_partner | 57 |
| product_template | 35 |
| crm_lead | 21 |
| res_users | 20 |
| mail_activity | 10 |
| tenancy_details | 4 |

`crm_team`, `crm_stage`, `sale_order`, `calendar_event`, `property_project`, `property_sub_project`, `kyc_application`, `crm_lead_ingestion_log` all showed `reltuples=-1` (never analyzed — this is not a permitted-by-estimate confirmation, so per the letter of the constraint these needed either an estimate or a bounded `count(*)`). Given total database size is 167 MB, `count(*)` under the mandated 15-second `statement_timeout` was used as the bounding safeguard instead of an unavailable estimate — none came close to timing out. Results for all 86 unanalyzed SGC/custom tables (generated via one batched query, `string_agg`-built `UNION ALL`, executed once):

| Table | Rows | Table | Rows |
|---|---|---|---|
| aml_screening_result | 37 | property_amenities | 9 |
| aml_fatf_jurisdiction | 25 | property_images | 7 |
| sgc_dfr_account_type | 18 | aml_edd_enquiry_type | 6 |
| sgc_launcher_usage | 18 | property_project | 6 |
| aml_transaction_alert | 17 | aml_monitoring_rule | 6 |
| property_tag | 16 | sgc_kpi_definition | 6 |
| property_connectivity | 12 | sgc_llm_provider | 5 |
| aml_risk_factor | 10 | sgc_ai_preset | 5 |
| property_region | 10 | property_sub_project | 5 |
| rent_contract | 4 | property_vendor | 4 |
| property_website_inquiry | 3 | property_res_city | 3 |
| property_commission_line | 3 | property_portal_line | 3 |
| property_specification | 1 | property_documents | 1 |
| property_vendor_commission_line | 1 | | |

**Every other custom table queried (68 of 90 total) returned exactly 0 rows**, including the entire KYC data model (`kyc_application`, `kyc_approval`, all rel/notification/wizard tables), most of AML's case-management layer (`aml_investigation_case`, `aml_risk_assessment`, `aml_goaml_report` — despite screening/alert activity existing, see §6), `crm_lead_ingestion_log`, all `sgc_dfr_*` scheduling tables, `sgc_ai_job`, `rent_invoice`, `rent_active_contract`, `tenancy_inquiry`.

### 5.2 crm_lead detail (Phase 4.2)

```
SELECT s.name, count(l.id) FROM crm_lead l JOIN crm_stage s ... GROUP BY s.name;
 New: 23   Proposition: 1
SELECT t.name, count(l.id) FROM crm_lead l LEFT JOIN crm_team t ... GROUP BY t.name;
 Sales: 24
SELECT min(create_date), max(create_date), assigned, has_message FROM crm_lead;
 min=2026-07-22 12:02:40   max=2026-08-14 10:54:32   assigned=24   has_message=24
```
All 24 leads are assigned to a user and have at least one `mail_message`. 23 of 24 sit in the "New" stage — almost nothing has progressed through the pipeline.

### 5.3 Sample rows (Phase 4.3) — redacted to first character + length

`res_partner` (5 rows, redacted): `M...(12)`, `S...(9)`, `A...(17)`, `P...(6)`, `D...(22)` — mixed: some read as real company/person names, others (short, generic) as plausible fixture data. **Not classified further than that without de-redacting, which this audit does not do.**

`crm_lead` (5 rows, redacted): `L...(19)`, `W...(24)`, `B...(15)`, `I...(31)`, `N...(11)`. Given 23/24 leads sit untouched in "New" and none progressed past "Proposition," the shape reads as **seeded/fixture data exercised lightly**, not a live sales pipeline with real deal flow — this is an interpretation stated as such, not a verified fact from the redacted samples alone.

### 5.4 Users (Phase 4.4)

```
SELECT count(*) FROM res_users WHERE active=true AND share=false;  →  7
```
7 non-portal active accounts: `admin`, `b.noronha@sgctech.ai`, `d.pavey@sgctech.ai`, `j.roble@sgctech.ai`, `john@sgctech.ai`, `renbranmadelo@gmail.com`, `t.sheraz@sgctech.ai`. (10 further active accounts are portal/share users — demo tenant/landlord/customer logins, credentials redacted, see §3.4.)

`res_users_log` (real login events, not just `create_date`):
```
 login                    | login_time
 admin                    | 2026-08-14 10:27:00
 john@sgctech.ai          | 2026-08-14 06:48:23
 t.sheraz@sgctech.ai      | 2026-08-04 04:36:33
 renbranmadelo@gmail.com  | 2026-07-25 07:12:18
 [+ 9 portal/demo accounts, 2026-07-07 to 2026-07-27]
```
**3 of the 7 non-portal accounts — `b.noronha@sgctech.ai`, `d.pavey@sgctech.ai`, `j.roble@sgctech.ai` — have NO row in `res_users_log` at all.** They were created 2026-08-14 (same batch) and have never logged in, on this evidence. Only 4 of 7 real staff accounts show any login evidence.

---

## 6. EVIDENCE OF ACTUAL USE (Phase 5) & R1–R10 COVERAGE (Phase 6)

### 6.1 ir_cron — 53 rows total, selected relevant rows

| id | name | active | lastcall |
|---|---|---|---|
| 22 | **CRM: Lead Assignment** | **false** | **(blank — never completed)** |
| 30 | LLM Lead Scoring: Auto Enrich Leads | false | 2026-07-25 04:49:05 (ran once, then disabled) |
| 44/45 | Attendance: auto check-out / detect absences | true | 2026-08-16 10:49:52 / :53 |
| 84–89 | AML: monitoring/screening/sanctions/review crons | mostly true | recent (2026-08-16, except #88 review-reminder = disabled) |
| 91 | SGC DFR: Scheduled Report Template **(inactive)** | false | (blank) |
| 95/96 | Web Research: Purge Audit Log / Cache | true | 2026-08-16 12:24:00 (the 2 orphan server actions from §4.4) |
| 97/98 | SGC AI: process/garbage-collect jobs | true | recent — **but `sgc_ai_job` table = 0 rows** |
| 99/100 | CRM Lead Ingestion: retry / purge logs | true | recent — **but `crm_lead_ingestion_log` = 0 rows** |
| 102 | CRM Dashboard: Run scheduled reports | true | 2026-08-16 12:48:34 (module is git-untracked, §2) |

**Pattern found repeatedly**: several crons fire on schedule (`lastcall` recent) whose target table has **zero rows** — the mechanism runs, finds nothing queued, and exits. This is real evidence the scheduler works; it is not evidence the underlying feature has ever processed real input.

### 6.2 Reports (Phase 5.3)

**60 `ir_actions_report` rows** belong to SGC modules (AML, KYC, WPS payroll, construction management, dynamic financial reports, employment certificates, HR memos, property/rent contracts, recruitment offer letters — full list in evidence log). Checking `ir_attachment` for persisted PDFs against those report target models:
```
SELECT res_model, count(*) FROM ir_attachment WHERE mimetype='application/pdf' GROUP BY res_model;
 construction.project.contract.doc | 3
 maintenance.request                | 1
 property.documents                 | 1
```
**None of these 3 attachment rows' models match any of the 60 report actions' own target models** (`property.vendor`, `property.details`, `rent.contract`, `sale.contract`, `kyc.application`, `hr.payslip`, `construction.project`, etc.). **No persisted-PDF evidence exists for any of the 60 SGC report templates.** Caveat stated precisely: Odoo can stream a generated PDF to a browser without saving it as an `ir_attachment` (persistence is a per-report configuration, not automatic) — so this does not prove a PDF was *never* generated, only that there is **no record that one ever was**. Per the task's own definition, these 60 reports are **UNPROVEN**, not "proven false."

wkhtmltopdf (required for `qweb-pdf` rendering) **is present**: `/usr/local/bin/wkhtmltopdf`, version `0.12.6.1 (with patched qt)`.

### 6.3 Outbound messaging (Phase 5.4)

```
SELECT state, count(*) FROM mail_mail GROUP BY state;
 exception: 31    sent: 1
```
**31 of 32 outbound emails ever attempted are in `exception` state; exactly 1 succeeded.** One SMTP server is configured (`ir_mail_server`: "Resend SMTP (scholarixglobal.com)", `smtp.resend.com`). No WhatsApp/SMS provider configuration table exists at all (`information_schema.tables` search for `%whatsapp%`/`%sms%provider%` → 0 rows).

`mail_message` by model (top rows): `property.image` 459, `hr.attendance` 203, `property.details` 186, `account.move` 137, `res.partner` 103, `crm.lead` 66, `aml.screening.result` 37, `rent.bill` 35, `rent.contract` 23, `property.project` 19, `aml.transaction.alert` 17 — real, varied logged activity across multiple modules, not just CRM.

### 6.4 Access control (Phase 5.5)

```
ir_model_access rows for SGC/property/kyc/aml/rent/tenancy models: 168   (basic CRUD permissions exist)
ir_rule rows for the same model set: 18 total, e.g.
  kyc.application: 2   property.details: 2   property.vendor: 2   rent.contract: 2   tenancy.details: 3
  ... most SGC models (sgc.commission, sgc.deals*, crm_lead_ingestion's own models) have ZERO ir_rule rows
```
Basic per-model CRUD access exists everywhere (168 rows). **Row-level record rules — the mechanism a multi-agent brokerage needs to keep Agent A from seeing Agent B's leads/deals — exist for only 18 of the ~90 custom models/tables**, and are absent from the commission and deals-management models specifically.

### 6.5 Call logging / KPI tracking (Phase 5, R7/R8 support)

```
SELECT t.id, name, count(a.id) FROM mail_activity_type t LEFT JOIN mail_activity a ... GROUP BY t.id;
 id=2 "Call": 0 activities logged   (stock Odoo activity type — exists, never used)
information_schema search for %call%/%phonecall%  →  only discuss_call_history (Discuss/chat calls, unrelated to sales calls)
sgc_kpi_definition (6 rows): generic BI KPIs — Confirmed Sales Revenue, Customer Invoiced, Committed
  Procurement Spend, Open Pipeline Value, Project Tasks by Deadline, Video Meetings Held.
  No call-count or call-target KPI defined.
```

### 6.6 R1–R10 coverage matrix

| # | Requirement | Class | Evidence |
|---|---|---|---|
| R1 | Meta/Google lead capture | **BUILT** | `crm_lead_ingestion_hub` module installed, manifest explicitly targets Meta/Google Ads/LinkedIn/TikTok/Snapchat webhooks — but `crm_lead_ingestion_log` = 0 rows despite its retry/purge crons firing on schedule (§6.1). No evidence any inbound webhook lead was ever received. Also: this module is git-**untracked** (§2). |
| R2 | WhatsApp instant notification | **ABSENT** | No WhatsApp provider table anywhere in the schema (§6.3 search). `mail_mail` shows only SMTP email attempts (31 exception, 1 sent). |
| R3 | Automatic distribution + manual reassignment | **PARTIAL** | Odoo's own `CRM: Lead Assignment` cron exists but is **inactive**, `lastcall` blank — never completed a run (§6.1, cron id 22). Manual reassignment is a standard Odoo field-edit capability (structurally present) but no change-log evidence of it ever being exercised was checked/found. |
| R4 | Per-lead status and remarks | **PROVEN** | Stage differentiation exists (New:23, Proposition:1) and **all 24 leads** have at least one `mail_message` (§6.3) — both status and remarks are populated and exercised. |
| R5 | Lead volume handling | **ABSENT** | Only 24 `crm_lead` rows exist total; no queueing/rate-limit/volume-specific mechanism found; nothing in this dataset demonstrates behavior at volume. |
| R6 | 6–7 sales users | **PARTIAL** | 7 non-portal active accounts exist (§5.4), matching the requirement almost exactly by headcount — but only 4 of the 7 have any login evidence in `res_users_log`; 3 have never logged in. |
| R7 | Call logging | **ABSENT** | Stock Odoo "Call" activity type exists but has 0 activities logged against it, ever (§6.5). No SGC-built call-log table found. |
| R8 | Call-target tracking | **ABSENT** | `sgc_kpi_definition` (the only KPI-definition table found) defines revenue/invoicing/pipeline/task/meeting KPIs — no call-count or call-target metric exists in it (§6.5). |
| R9 | Attendance integration | **PARTIAL** | Standard Odoo `hr_attendance` is installed and genuinely active (203 `mail_message` rows on `hr.attendance`, 2 related crons firing on schedule with recent `lastcall`, §6.1/§6.3). No external attendance-hardware (biometric device) integration table or config was found — this is Odoo's native manual/kiosk attendance, not hardware integration. |
| R10 | Daily reporting | **PARTIAL** | `sgc_crm_dashboard`'s "Run scheduled reports" cron is active with a recent `lastcall` (§6.1) — but that module is git-**untracked** (§2), and no persisted report-output evidence (PDF/attachment) was found for it or for `sgc_dynamic_financial_report`'s scheduling tables, which show 0 rows across the board (§5.1). |

**Coverage as a fraction, not rounded, out of R1–R10**: **1 PROVEN** (R4), **1 BUILT** (R1), **4 PARTIAL** (R3, R6, R9, R10), **4 ABSENT** (R2, R5, R7, R8), **0 DB-ONLY**.

---

## 7. PACKAGEABILITY VERDICT (Phase 7)

### 7.1 Could this be redeployed to a new client database today, using only files in a repository? **PARTIAL.**

What redeploys cleanly from `git@gh-demo-addons:samanabran/demo.git` (29 of 34 custom modules, §2): install those modules fresh, and their code-defined models/views/security come with them.

What would **not** come along and must be rebuilt by hand:
- **4 installed, live modules with zero git history**: `sgc_crm_dashboard`, `crm_lead_ingestion_hub`, `aml_compliance`, `sgc_executive_dashboard`. These would need to be manually copied off this specific server (or recovered from `/root/addons-export/demo_presentation-addons.tar.gz` / `/tmp/demo_presentation_addons_snapshot.tar.gz`, both unverified by this audit) before a redeploy could include them at all.
- **6 orphan views** tied to real business models (`property.project`, `property.sub.project`, `tenancy.details`) with no `ir_model_data` — these exist only as this database's own rows.
- **2 manual (Studio) fields** (`x_plan2_id` on two models).
- **2 orphan server actions** ("Web Research: Purge...") with no module ownership at all.
- **The 3 standalone seed/migrate Python scripts** (`demo_presentation_seed_website.py`, `demo_presentation_migrate.py`, `demo_presentation_migrate_gallery.py`) that live outside any git repo (§3.3) — whatever data shape they produced is not reproducible by installing modules alone.
- Any effect of the **uncommitted edit** to `hr_payroll_community/models/hr_employee.py` (vendor module, locally modified, not committed anywhere).

### 7.2 DB-only rebuild scope — record counts, not hours

Per instruction, **no hours estimate is given.** What would need manual recreation, by count:
- 2 manual fields
- 6 orphan views on real models (+ ~86 further orphan views not individually verified as true customization vs. theme-snippet-by-design, see §2)
- 2 orphan server actions
- The data shape produced by 3 untracked seed/migrate scripts — **unknown record count**, since this audit did not read those scripts' contents or diff their output against a fresh install (out of scope for a read-only inventory pass; flagged as a next step, not attempted here)

### 7.3 External dependencies — required and checked present-on-this-box

| Dependency | Required by | Present on this box? |
|---|---|---|
| Python: `openai`, `anthropic`, `tiktoken`, `numpy`, `pandas` | `sgc_assessment` | **Yes** — versions confirmed (openai 2.44.0, anthropic 0.116.0, tiktoken 0.13.0, numpy 2.5.1, pandas 3.0.3) |
| Python: `requests` | `sgc_lead_scoring` | **Yes** (2.34.2) |
| Python: `google_auth_oauthlib`, `google-api-python-client`, `requests`, `cryptography` | `sgc_video_conferencing` | **Yes** (cryptography 41.0.7; oauthlib/googleapiclient import successfully, version not exposed) |
| `wkhtmltopdf` | Every `qweb-pdf` report (60 SGC report actions) | **Yes** — `/usr/local/bin/wkhtmltopdf`, 0.12.6.1 |
| WhatsApp BSP account | R2 (WhatsApp notifications) | **No configuration found at all** — would need to be sourced and configured from scratch |
| Meta/Google Ads app credentials | R1 (lead capture) | Not checked directly (no credential table found in the schema search performed; `crm_lead_ingestion_hub`'s own config storage was not separately audited for credential rows) |
| Telephony/call system | R7/R8 | **No integration found** — would need to be sourced from scratch |
| Attendance hardware (biometric device integration) | R9 | **No integration found** — current attendance is Odoo's native manual/kiosk entry only |
| SMTP | Outbound email | **Configured** (Resend SMTP, `smtp.resend.com`) but **31 of 32 send attempts are in `exception` state** — configuration exists, is not reliably working |

### 7.4 Client-specific data that would need stripping before reuse (named, not removed)

- `res_company` id=1 "My Company" (unrenamed default) and id=2 **"test"** — both need real identity or removal before this is a template.
- 7 real staff email addresses (`@sgctech.ai` × 6, plus `renbranmadelo@gmail.com`) as `res_users.login` values.
- 10 portal/demo accounts with test credentials (tenant/landlord/customer/test.com addresses) — credentials themselves redacted from this report, but the accounts and their emails are real rows in this database.
- `ir_mail_server` row naming a real domain (`scholarixglobal.com`) and SMTP provider (Resend) — credential fields not read by this audit but the row itself is client-identifying and must be stripped or replaced.
- `sgc_offplan_rental_property_management/ops/ops.env` — a 25-byte, gitignored env file on the host, contents not read, flagged for handling.
- `/root/.demo_presentation_admin_passwd_20260726` — a host file whose name implies a plaintext admin password; existence noted only, not opened, not part of the database itself but a same-box security-hygiene item.
- Branding: `sgc_tech_ai_theme`, `sgc_design_tokens` ("Deep Navy + Gold + Ivory" per its own manifest summary) are SGC's own brand system, not generic — would need re-theming for a different client's brand.
- 57 `res_partner` rows and 24 `crm_lead` rows of unknown real-vs-fixture status (§5.3) — not individually classified beyond the redacted sample; would need a full pass before any of them ship to a buyer as "reference data."

---

## 8. WHAT THIS DATABASE DOES NOT PROVE

Stated plainly, so it isn't quietly assumed later:

- **It does not prove any real client, agent, or tenant has ever used this system.** Every login with any evidence traces to an `@sgctech.ai` address, a personal gmail, or an explicitly-named `demo`/`test` account. No independent third-party identity was found anywhere in the sampled data.
- **It does not prove Meta or Google lead capture works.** The module exists and is installed; its own log table has never recorded a single row despite its retry cron running on schedule for weeks. "Installed" is not "received a lead."
- **It does not prove WhatsApp notification exists at all**, proven or otherwise — no code, no config, no table.
- **It does not prove automatic lead distribution has ever run.** The dedicated cron for it is disabled and has never completed once (`lastcall` is blank, not just old).
- **It does not prove any of the 60 SGC report templates can actually render a PDF end-to-end.** wkhtmltopdf is present and 3 unrelated PDFs exist in the attachment table, but zero PDFs trace back to any of the 60 named report actions. Absence of a persisted attachment is not proof of failure (Odoo can stream without saving) — but it is proof of **no positive evidence**, which is the standard this report holds to throughout.
- **It does not prove outbound email works reliably.** 31 of 32 attempts are in an exception state. One success is not a working notification pipeline.
- **It does not prove call logging or call-target tracking exist as features at all** — not built, not evidenced, not present under any table name searched.
- **It does not prove attendance *hardware* integration** — only that Odoo's own manual attendance module is installed and has real check-in/out message activity. A physical device integration is a different, unevidenced claim.
- **It does not prove per-agent data isolation is enforced.** `ir_model_access` (CRUD) is populated everywhere; `ir_rule` (row-level, who-sees-what) exists for only 18 of ~90 custom models, and is absent from the commission and deals-management models specifically — the two most likely to need it in a real multi-agent brokerage.
- **It does not prove the four git-untracked modules (`sgc_crm_dashboard`, `crm_lead_ingestion_hub`, `aml_compliance`, `sgc_executive_dashboard`) can be redeployed at all**, only that they currently run on this one server. No second copy of their source was verified to exist and be restorable (the export tarballs referenced in §3.3 were located but not opened or verified).
- **It does not establish real headcount usage.** 7 accounts roughly matches "6-7 sales users," but 3 of those 7 have zero login history — matching a headcount number is not the same as that headcount actively using the system.
- **It does not establish that the 24 CRM leads or 57 partner records are genuine prospects** rather than seeded/fixture data — the redacted sample is consistent with either reading, and this audit deliberately did not de-redact records to settle it.
- **A "reltuples=-1, so I counted directly" pattern was used for 86 tables** (§5.1) — this is a `count(*)` under a 15-second timeout used as a bounding safeguard where the instructed estimate-first method returned "never analyzed," not a violation of intent, but stated here so the method is auditable rather than assumed compliant.
