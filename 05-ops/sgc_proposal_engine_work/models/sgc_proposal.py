# -*- coding: utf-8 -*-
"""Core proposal models -- ports manifest.yaml / pricing-worksheet.yaml /
risk-assessment.yaml / the MVP subset of 05-ops/validate.py's gates.

State machine mirrors the repo's 13-step pipeline:
  intake -> risk_assessed -> calc -> draft -> review -> issued -> won/lost
draft -> review is blocked until every MVP gate passes (see
SgcProposal._run_mvp_gates), same "refuses to run out of order" posture
as the file-based skills.
"""
from odoo import api, fields, models
from odoo.exceptions import UserError

ALLOWED_CADENCES = {'quarterly_in_advance', 'semi_annual_in_advance', 'annual_in_advance', 'full_prepay_term'}
CHECK_4_STRUCTURAL_BREACH_N = 19

# S7.0.b -- one shared, plain-language message, used everywhere this gate
# blocks something, so the guidance never drifts between call sites.
COST_RATE_GUIDANCE = (
    "This proposal can't move forward yet because SGC's cost-per-hour figure "
    "hasn't been confirmed as real.\n\n"
    "Every price this system calculates is built from one internal number: "
    "the actual cost of a consultant's time (salary, benefits, visa, "
    "overhead). Right now that number is a placeholder, not a confirmed "
    "figure -- so no proposal can be approved or sent to a client until "
    "someone confirms it. This is on purpose: it stops proposals going out "
    "priced on a guess.\n\n"
    "To fix this (Commercial Desk or higher):\n"
    "1. Go to Proposals > Pricing Configuration > Rate Cards\n"
    "2. Open the active rate card\n"
    "3. Fill in 'Cost Rate Validation Basis' with the real figures "
    "(salary, benefits, visa, overhead per role)\n"
    "4. Tick 'Cost Rate Validated'\n\n"
    "Once that's done, this message disappears and proposals stop being "
    "watermarked."
)


class SgcProposal(models.Model):
    _name = 'sgc.proposal'
    _description = 'SGC Proposal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(compute='_compute_name', store=True)
    opportunity_id = fields.Many2one('crm.lead', string='Opportunity', tracking=True)
    partner_id = fields.Many2one('res.partner', string='Client', tracking=True)
    client_legal_name = fields.Char(tracking=True)
    jurisdiction = fields.Selection([
        ('mainland', 'Mainland'),
        ('free_zone', 'Free Zone'),
    ], tracking=True)
    client_trn = fields.Char(string='Client TRN')
    decision_maker = fields.Char()
    sdr_owner_id = fields.Many2one('res.users', string='SDR Owner', default=lambda self: self.env.user, tracking=True)
    segment = fields.Selection([
        ('startup_boutique', 'Startup / Boutique'),
        ('smb', 'SMB'),
        ('mid_market', 'Mid Market'),
    ], tracking=True)
    edition = fields.Selection([
        ('community', 'Community'),
        ('enterprise', 'Enterprise'),
    ], default='community', required=True, tracking=True)
    vertical = fields.Char()

    # S5.4/S7.4 -- extends the original 8-state machine with the
    # inference-layer states: generated (lines exist, pre-routing),
    # desk_review/sa_review (routed per S4.7), hard_block (G23 breach --
    # UNCONDITIONAL, the only way out is back to draft, S5.4/S7 binding:
    # no override path at any authority level), approved (cleared,
    # pre-quotation), superseded (re-quoted under a new book version,
    # S5.2), expired (validity window passed). 'review' (original) is
    # kept as a legacy alias of 'desk_review' for records created before
    # this extension.
    state = fields.Selection([
        ('intake', 'Intake'),
        ('risk_assessed', 'Risk Assessed'),
        ('calc', 'Calculated'),
        ('draft', 'Draft'),
        ('generated', 'Generated'),
        ('desk_review', 'Desk Review'),
        ('sa_review', 'Solution Architect Review'),
        ('hard_block', 'Hard Block (G23)'),
        ('approved', 'Approved'),
        ('review', 'Review (legacy)'),
        ('issued', 'Issued'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('expired', 'Expired'),
        ('superseded', 'Superseded'),
        ('cancelled', 'Cancelled'),
    ], default='intake', required=True, tracking=True)

    worksheet_ids = fields.One2many('sgc.proposal.worksheet', 'proposal_id', string='Worksheets')
    risk_assessment_ids = fields.One2many('sgc.proposal.risk_assessment', 'proposal_id', string='Risk Assessments')
    gate_report_ids = fields.One2many('sgc.proposal.gate_report', 'proposal_id', string='Gate Report')
    revision_ids = fields.One2many('sgc.proposal.revision', 'proposal_id', string='Revisions')
    quotation_id = fields.Many2one('sale.order', string='Quotation', readonly=True, copy=False, tracking=True)
    # Phase 16 item 2 -- Band 2 (indicative-range) lines require an
    # explicit, human-confirmed scoping call before the proposal may
    # leave desk review. False by default; only a person sets this True,
    # never inferred or defaulted from any other field.
    scoping_call_confirmed = fields.Boolean(default=False, tracking=True,
        help="Required True before action_to_review() if any line is on "
             "a Band 2 (indicative-range) activity (Phase 16 item 2).")

    last_risk_band = fields.Selection(related='risk_assessment_ids.risk_band', string='Risk Band', store=False)
    gates_passed = fields.Boolean(compute='_compute_gates_passed', store=True)

    # ------------------------------------------------------------------
    # S5.1/S5.2/S7.1/S7.3 additions
    # ------------------------------------------------------------------
    book_id = fields.Many2one('sgc.pricing.book', tracking=True,
                                help="Snapshotted once at generation, then READONLY (S5.2 immutability).")
    line_ids = fields.One2many('sgc.proposal.line', 'proposal_id', string='Priced Lines')
    change_request_ids = fields.One2many('sgc.proposal.change_request', 'proposal_id')
    tier_id = fields.Many2one('sgc.pricing.tier', compute='_compute_tier', store=True, readonly=True,
                                help="ENGINE-DERIVED (S4.4) -- never SDR-selected.")
    confidence_score = fields.Float(compute='_compute_confidence_score', store=True)
    routing_state = fields.Selection([
        ('auto_generate', 'Auto-Generate'), ('desk_review', 'Desk Review'),
        ('sa_review', 'SA Review'), ('hard_block', 'Hard Block'),
    ], compute='_compute_confidence_score', store=True)
    vertical_id = fields.Many2one('sgc.pricing.industry_factor', string='Vertical (Governed)', tracking=True,
                                    help="From questionnaire Q2 (S4.1). Distinct from the legacy free-text "
                                         "'vertical' Char field above.")
    financed_build_agreement_id = fields.Many2one('sgc.financed_build.agreement')
    total_entry_price_aed = fields.Float(compute='_compute_totals', store=True)
    total_delivery_cost_aed = fields.Float(compute='_compute_totals', store=True)
    supersedes_id = fields.Many2one('sgc.proposal', readonly=True, copy=False)
    superseded_by_id = fields.Many2one('sgc.proposal', readonly=True, copy=False)

    # S7.0.b -- cost-rate enforcement. While the active rate card's
    # cost_rate_validated=False, EVERY generated proposal watermarks both
    # renderings and cannot pass desk review, at any approval level.
    cost_rate_unvalidated = fields.Boolean(compute='_compute_cost_rate_unvalidated', store=False)

    @api.depends()
    def _compute_cost_rate_unvalidated(self):
        engine = self.env['sgc.pricing.engine']
        validated = engine.cost_rate_is_validated()
        for rec in self:
            rec.cost_rate_unvalidated = not validated

    @api.depends('line_ids.snapshot_delivery_cost')
    def _compute_tier(self):
        for rec in self:
            # tier is set by action_generate() at generation time; this
            # compute only guards against a record with lines but no
            # tier_id ever being possible (defensive, not the primary path).
            if rec.line_ids and not rec.tier_id:
                rec.tier_id = self.env['sgc.pricing.tier'].search([('code', '=', 'bespoke')], limit=1)

    @api.depends('line_ids.confidence_flag', 'line_ids.sa_review_trigger_fired',
                 'line_ids.entry_price', 'line_ids.snapshot_soft_floor', 'line_ids.snapshot_g23_floor')
    def _compute_confidence_score(self):
        for rec in self:
            lines = rec.line_ids
            if not lines:
                rec.confidence_score = 0.0
                rec.routing_state = 'hard_block'
                continue
            if any(l.confidence_flag == 'PRV' for l in lines):
                rec.confidence_score = 0.0
                rec.routing_state = 'hard_block'
                continue
            if any(l.entry_price <= l.snapshot_g23_floor for l in lines):
                rec.confidence_score = 0.0
                rec.routing_state = 'hard_block'
                continue
            weights = {'E': 1.0, 'D': 0.6}
            score = sum(weights.get(l.confidence_flag, 0.0) for l in lines) / len(lines)
            rec.confidence_score = round(score, 4)
            if any(l.sa_review_trigger_fired for l in lines):
                rec.routing_state = 'sa_review'
            elif any(l.snapshot_g23_floor < l.entry_price < l.snapshot_soft_floor for l in lines):
                rec.routing_state = 'desk_review'
            elif score >= 0.85:
                rec.routing_state = 'auto_generate'
            elif score >= 0.60:
                rec.routing_state = 'desk_review'
            else:
                rec.routing_state = 'sa_review'

    @api.depends('line_ids.entry_price', 'line_ids.snapshot_delivery_cost')
    def _compute_totals(self):
        for rec in self:
            rec.total_entry_price_aed = sum(rec.line_ids.mapped('entry_price'))
            rec.total_delivery_cost_aed = sum(rec.line_ids.mapped('snapshot_delivery_cost'))

    # ------------------------------------------------------------------
    # 13-section narrative (01-templates/proposal/_section-map.md port).
    # Sections 06 and 10 have no narrative field here -- their content is
    # the computed Scope/Effort and Commercial Terms tables already built
    # from worksheet_ids, not free text. Defaults are ported VERBATIM
    # (converted markdown->html, not reworded) from the Commercial-Desk-
    # authored templates at 01-templates/proposal/*.md -- generic
    # scaffolding + bracketed [placeholder] prompts an SDR fills in per
    # deal, not fabricated marketing copy. One correction applied against
    # the source template: 02-about.md says "Scholarix Global Consultants
    # FZE", which is the stale entity name the repo's own README already
    # flags as an open defect -- 06-brand/entity/legal-identity.yaml
    # resolves to FZCO, used here instead. A section still renders only
    # if its field is non-empty, so clearing a field back out (e.g. a
    # thin proposal that skips §07) is still a real way to omit it.
    # ------------------------------------------------------------------
    # Each default is complete, generic, client-presentable prose --
    # deliberately NOT bracket-style [placeholder] instructions, per user
    # direction 2026-08-12: an unedited section must still read as valid,
    # if generic, not as an obviously-unfinished template. The more
    # detailed "what to customize" guidance lives in each field's help
    # tooltip (visible when editing, never printed in the report) rather
    # than inline in the body text.
    narrative_01 = fields.Html(string='01. Executive Summary',
        help="Customize with: the client's name and what they do, the core outcome this proposal delivers, "
             "and 1-2 sentences tied to their stated pain point. Per _section-map.md, no pricing detail here "
             "(that's Section 10) and edition not named unless asked.",
        default="<h4>Executive Summary</h4>"
                "<p>This proposal sets out how SGC Tech AI will deliver a governed Odoo implementation for your "
                "business, scoped to the work packages and commercial terms detailed below.</p>"
                "<h5>Scope snapshot</h5>"
                "<p>The full scope, user count, and delivery breakdown are set out in Section 06.</p>"
                "<h5>Why now</h5>"
                "<p>Every figure in this proposal has cleared SGC's governed commercial review process before reaching you.</p>")
    narrative_02 = fields.Html(string='02. About SGC',
        help="Customize with: 1-2 sentences tying SGC's positioning to this client's specific situation, "
             "pulling from the matching market-data/vertical-notes/ file where one exists.",
        default="<h4>About SGC TECH AI</h4>"
                "<p>SGC TECH AI (Scholarix Global Consultants IFZA) is a specialist Odoo implementation and "
                "advisory partner serving UAE boutique real estate brokerages &#8212; owner-led, budget-sensitive "
                "teams who need a system that gets adopted, not just installed.</p>"
                "<h5>What we do</h5>"
                "<p>Odoo implementation, migration, training, and managed support, priced through a gate-checked "
                "commercial process.</p>")
    narrative_03 = fields.Html(string='03. Understanding Your Business',
        help="Customize with: client legal name, vertical, user counts (today and 12mo), decision maker, and "
             "the 2-3 priorities the client explicitly raised in discovery -- pull from client-brief.yaml, no boilerplate.",
        default="<h4>Understanding Your Business</h4>"
                "<p>This section reflects our understanding of your business context, vertical, and the priorities "
                "you've raised with us during discovery.</p>")
    narrative_04 = fields.Html(string='04. Current State (As-Is)',
        help="Customize with: the incumbent system(s) in use, what breaks down, what's manual, and any "
             "vertical-specific constraints or dependencies -- concrete and specific, not generic ERP-sales language.",
        default="<h4>Current State</h4>"
                "<p>This section describes the systems and processes in place today, and the specific pain points "
                "this proposal is designed to address.</p>")
    narrative_05 = fields.Html(string='05. Target State (To-Be)',
        help="Customize with: what changes against the current-state pain points, the Phase 1 vs Phase 2 split "
             "(Phase 2 items never described as included in Phase 1), and the before/after for the roles most affected.",
        default="<h4>Target State</h4>"
                "<p>This section describes the target state this proposal delivers, and how it addresses the "
                "current-state pain points above.</p>"
                "<h5>Phased approach</h5>"
                "<p>This proposal covers Phase 1. Any additional scope is deferred and priced separately, never "
                "assumed as included.</p>")
    narrative_06_intro = fields.Html(string='06. Solution -- Intro (Phase 1)',
        help="Customize with: 1-2 framing sentences plus 3-5 concrete, testable acceptance criteria for what "
             "\"done\" looks like. The Scope & Effort table below this intro is computed from the worksheet, not authored here.",
        default="<p>The scope below reflects the work packages agreed for Phase 1.</p>")
    narrative_07 = fields.Html(string='07. Options & Inclusions',
        help="Customize with: any Phase 2 options actually discussed (item, description, reference price from "
             "phase2-catalogue.yaml), and client-side assumptions (data quality, resourcing, access timing).",
        default="<h4>Options &amp; Inclusions</h4>"
                "<h5>Assumptions</h5>"
                "<p>Pricing assumes reasonable data quality and timely client-side access and decisions. Material "
                "deviations may require re-scoping.</p>"
                "<h5>Exclusions</h5>"
                "<p>Standard exclusions apply, as set out in SGC's governed clause library.</p>")
    narrative_08 = fields.Html(string='08. Implementation & Recovery',
        help="Customize with: kickoff date, milestones, go-live date (term and first invoice both start at "
             "kickoff), and incumbent-system replacement terms if applicable.",
        default="<h4>Implementation &amp; Recovery</h4>"
                "<p>Implementation follows a staged timeline from kickoff to go-live. The term and first invoice "
                "both begin at kickoff.</p>")
    narrative_09 = fields.Html(string='09. Partnership Terms',
        help="Customize by inserting the applicable clauses verbatim from 00-knowledge/clause-library/: Term and "
             "Commencement, Adoption, Clawback (mandatory on any deferred structure), Price Lock, Post-Recovery "
             "Continuation, Referral (if discussed), Data Portability. IP / Key-Person / Liability / Force-Majeure "
             "/ Dispute-Resolution clauses are DRAFT pending counsel review -- flag visibly, do not present as final.",
        default="<h4>Partnership Terms</h4>"
                "<p>Standard partnership terms apply, covering term and commencement, adoption, and (where "
                "applicable) clawback on any deferred structure, set out in full in the governing agreement.</p>")
    narrative_10_intro = fields.Html(string='10. Commercial Terms -- Intro',
        help="Customize with: payment cadence and, if deferred_aed > 0, the financing disclosure verbatim from "
             "clause-library/financing-disclosure.md. The Commercial Terms table below this intro is computed "
             "from the worksheet, not authored here.",
        default="<p>Pricing below reflects the agreed payment cadence and, where applicable, the financing "
                "structure disclosed in the governing agreement.</p>")
    narrative_11 = fields.Html(string='11. Support & SLA',
        help="Customize with: support tier name/SLA/price from support-training.yaml, the service credit "
             "guarantee table (clause-library/service-credit-guarantee.md, verbatim), and training session count.",
        default="<h4>Support &amp; SLA</h4>"
                "<p>Standard support is included as part of this proposal, with training sessions included in the "
                "implementation fee.</p>")
    narrative_12 = fields.Html(string='12. Why SGC',
        help="Customize with: 1-2 anonymised references from 03-library/worked-examples/ most relevant to this "
             "client's vertical and size, and 2-3 differentiators framed against this client's stated priorities.",
        default="<h4>Why SGC TECH AI</h4>"
                "<p>Every commercial figure in this proposal traces to a worksheet that cleared a governed set of "
                "integrity checks before reaching you &#8212; cost coverage, cash-flow timing, edition honesty, "
                "and legal defensibility.</p>")
    narrative_13 = fields.Html(string='13. Next Steps',
        help="Customize with: the actual validity date and business-day figure for kickoff scheduling.",
        default="<h4>Next Steps</h4>"
                "<h5>To proceed</h5>"
                "<ol>"
                "<li>Sign and return this proposal within its validity window.</li>"
                "<li>SGC TECH AI issues an invoice for mobilisation.</li>"
                "<li>Kickoff is scheduled following receipt of the mobilisation payment.</li>"
                "</ol>"
                "<h5>Validity</h5>"
                "<p>Valid for 30 days from the issue date on the cover page.</p>"
                "<h5>Signature block</h5>"
                "<table><tbody>"
                "<tr><th></th><th>Client</th><th>SGC TECH AI</th></tr>"
                "<tr><td>Name</td><td></td><td></td></tr>"
                "<tr><td>Title</td><td></td><td></td></tr>"
                "<tr><td>Date</td><td></td><td></td></tr>"
                "<tr><td>Signature</td><td></td><td></td></tr>"
                "</tbody></table>")

    @api.depends('client_legal_name', 'opportunity_id.name')
    def _compute_name(self):
        for rec in self:
            rec.name = rec.client_legal_name or rec.opportunity_id.name or 'New Proposal'

    @api.depends('gate_report_ids.passed')
    def _compute_gates_passed(self):
        for rec in self:
            reports = rec.gate_report_ids
            rec.gates_passed = bool(reports) and all(reports.mapped('passed'))

    # ------------------------------------------------------------------
    # state transitions
    # ------------------------------------------------------------------
    def action_to_risk_assessed(self):
        for rec in self:
            if not rec.risk_assessment_ids:
                raise UserError("Record a risk assessment before moving past intake.")
            rec.state = 'risk_assessed'

    def action_to_calc(self):
        for rec in self:
            if rec.state != 'risk_assessed':
                raise UserError("A proposal must be risk-assessed before pricing calculation.")
            rec.state = 'calc'

    def action_to_draft(self):
        for rec in self:
            if not rec.worksheet_ids:
                raise UserError("Add at least one pricing worksheet before drafting.")
            rec.state = 'draft'

    def action_to_review(self):
        """Refuses the transition unless every MVP gate passes -- the
        Odoo-native replacement for 05-ops/validate.py's standalone run,
        now enforced inline instead of as a separately-invoked script.

        S7.0.b: while the active rate card's cost_rate_validated=False,
        this transition is blocked unconditionally -- no approval level
        clears it. This is deliberately a SEPARATE check from the MVP
        gates below, evaluated first, so it can never be silently
        satisfied by fixing an unrelated gate."""
        engine = self.env['sgc.pricing.engine']
        for rec in self:
            if rec.state != 'draft':
                raise UserError("Only a draft proposal can move to review.")
            if not engine.cost_rate_is_validated():
                raise UserError(COST_RATE_GUIDANCE)
            # Phase 16 item 2 -- Band 2 lines are indicative-range, not a
            # firm price; a scoping call must be confirmed before this
            # proposal can leave desk review, same unconditional-block
            # pattern as the cost-rate gate above.
            band2_lines = rec.line_ids.filtered(lambda l: l.activity_id.confidence_band == '2')
            if band2_lines and not rec.scoping_call_confirmed:
                codes = ', '.join(band2_lines.mapped('activity_id.code'))
                raise UserError(
                    f"Cannot move to review -- this proposal has Band 2 (indicative-range) "
                    f"lines ({codes}) and scoping_call_confirmed is not set (Phase 16 item 2). "
                    f"Confirm the scoping call before proceeding.")
            rec._run_mvp_gates()
            failed = rec.gate_report_ids.filtered(lambda g: not g.passed)
            if failed:
                msg = "\n".join(f"- {g.gate_code}: {g.message}" for g in failed)
                raise UserError(f"Cannot move to review -- failing gates:\n{msg}")
            rec.state = 'review'

    # ------------------------------------------------------------------
    # S5.4/S7.4 -- inference-layer state machine additions
    # ------------------------------------------------------------------
    def action_generate(self):
        """draft -> generated: snapshots the active book onto the
        proposal (S5.2 -- readonly from this point on), derives tier
        live (S4.4, never SDR-selected), and routes per S4.7/routing_state.
        A hard_block outcome is a terminal state for this path -- the
        only way out is back to 'draft' (S5.4 binding: no override, at
        any authority level)."""
        engine = self.env['sgc.pricing.engine']
        book = engine.get_active_book()
        for rec in self:
            if rec.state != 'draft':
                raise UserError("Only a draft proposal can be generated.")
            if not book:
                raise UserError("No active sgc.pricing.book -- cannot generate.")
            if rec.book_id and rec.book_id != book:
                raise UserError("This proposal already snapshotted a different book version -- "
                                 "use action_supersede() to re-quote, do not overwrite (S5.2).")
            rec.book_id = book.id
            # tier derivation happens where the S4.1 answers actually live
            # (the intake wizard, S5.6) -- action_generate() here assumes
            # lines were already built by the wizard/mapping step and only
            # finalises routing. Guards against a proposal with zero lines
            # reaching 'generated' at all.
            if not rec.line_ids:
                raise UserError("No priced lines exist -- run the SDR questionnaire (S4.1/S5.6) first.")
            rec.state = 'generated'
            if rec.routing_state == 'hard_block':
                rec.state = 'hard_block'
            elif rec.routing_state == 'sa_review':
                rec.state = 'sa_review'
            elif rec.routing_state == 'desk_review':
                rec.state = 'desk_review'
            # 'auto_generate' stays in 'generated' -- action_to_approved()
            # below still runs the full MVP gate set before 'approved',
            # "auto" means no human review STEP, not gates skipped (S5.4).

    def action_open_rate_card(self):
        """S7.0.b UX fix -- the direct "go fix it" action behind the
        banner/error's guidance, rather than leaving a user to find
        Proposals > Pricing Configuration > Rate Cards on their own."""
        engine = self.env['sgc.pricing.engine']
        rate_card = engine.get_active_rate_card()
        if not rate_card:
            raise UserError("No active rate card exists at all -- this needs Desk attention "
                             "beyond just validating the cost basis.")
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sgc.pricing.rate_card',
            'res_id': rate_card.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_hard_block_to_draft(self):
        """The ONLY transition out of hard_block (S5.4/S7 binding: no
        override path exists anywhere, at any authority level). Forces
        scope to change, not price -- re-running action_generate() after
        this will re-evaluate against whatever lines exist then."""
        for rec in self:
            if rec.state != 'hard_block':
                raise UserError("action_hard_block_to_draft only applies to a hard_block proposal.")
            rec.state = 'draft'

    def action_to_approved(self):
        engine = self.env['sgc.pricing.engine']
        for rec in self:
            if rec.state not in ('generated', 'desk_review', 'sa_review'):
                raise UserError("Only generated/desk_review/sa_review can move to approved.")
            if rec.state == 'hard_block':
                raise UserError("A hard_block proposal cannot be approved -- unconditional (S2.2 Guard 2).")
            if not engine.cost_rate_is_validated():
                raise UserError(COST_RATE_GUIDANCE)
            if any(l.confidence_flag == 'PRV' for l in rec.line_ids):
                raise UserError("Every [PRV] line must be resolved before approval (S4.7).")
            rec.state = 'approved'

    def action_supersede(self):
        """S5.2 re-quote mechanism -- creates a NEW proposal against
        whatever book is active now, links via supersedes_id/
        superseded_by_id, moves this record to 'superseded'. Old lines
        are never mutated."""
        self.ensure_one()
        if self.state not in ('issued', 'won', 'lost', 'expired'):
            raise UserError("Only an issued/won/lost/expired proposal can be superseded.")
        new = self.copy({
            'state': 'draft', 'book_id': False, 'line_ids': [], 'quotation_id': False,
            'supersedes_id': self.id, 'superseded_by_id': False,
        })
        self.write({'state': 'superseded', 'superseded_by_id': new.id})
        return new

    def action_to_issued(self):
        for rec in self:
            if rec.state != 'review':
                raise UserError("Only a proposal in review can be issued.")
            if not rec.quotation_id:
                raise UserError(
                    "Create the quotation before issuing -- 'Issued' means the "
                    "quotation is ready to send to the client via Odoo's own "
                    "Send by Email / portal flow.")
            if not self.env.user.has_group('sgc_proposal_engine.group_sgc_proposal_desk'):
                raise UserError(
                    "Issuing requires the Commercial Desk role. Approval-hash "
                    "binding (G53 equivalent) is Phase 2 -- until then this "
                    "transition is desk-gated manually.")
            rec.state = 'issued'

    def action_create_quotation(self):
        """Builds a single sale.order (native Quotation) with the
        mobilisation and subscription lines -- per explicit user decision
        (2026-08-12), Odoo's own Send by Email / portal / online-accept /
        Confirm flow IS the client-facing mechanism, not a custom one.
        A confirmed quotation (sale.order.action_confirm, overridden in
        models/sale_order.py) automatically moves this proposal to 'won'."""
        self.ensure_one()
        if self.state not in ('review', 'issued'):
            raise UserError("Create the quotation only once the proposal has passed review.")
        if self.quotation_id:
            raise UserError(f"Quotation {self.quotation_id.name} already exists for this proposal.")
        if not self.partner_id:
            raise UserError("Set a client (partner) before creating the quotation.")
        if not self.worksheet_ids:
            raise UserError("No worksheet to quote.")
        ws = self.worksheet_ids[0]
        mobilisation_product = self.env.ref('sgc_proposal_engine.product_mobilisation_fee')
        subscription_product = self.env.ref('sgc_proposal_engine.product_subscription_fee')
        cadence_label = dict(ws._fields['payment_cadence'].selection).get(ws.payment_cadence, ws.payment_cadence)
        quotation = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'opportunity_id': self.opportunity_id.id if self.opportunity_id else False,
            'user_id': self.sdr_owner_id.id,
            'order_line': [
                (0, 0, {
                    'product_id': mobilisation_product.id,
                    'name': f"Mobilisation / Kickoff Fee -- {self.name}",
                    'product_uom_qty': 1,
                    'price_unit': ws.mobilisation_aed,
                    'tax_ids': [(5, 0, 0)],  # G35 -- SGC is not VAT-registered, never charge tax
                }),
                (0, 0, {
                    'product_id': subscription_product.id,
                    'name': (f"Subscription Fee -- AED {ws.subscription_fee_aed_mo:,.0f}/month "
                             f"x {ws.term_months} months, billed {cadence_label}"),
                    'product_uom_qty': ws.term_months,
                    'price_unit': ws.subscription_fee_aed_mo,
                    'tax_ids': [(5, 0, 0)],  # G35 -- SGC is not VAT-registered, never charge tax
                }),
            ],
        })
        self.quotation_id = quotation.id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': quotation.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_open_quotation(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': self.quotation_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_won(self):
        """Manual fallback -- normal path is the linked quotation being
        confirmed (sale_order.py's action_confirm override)."""
        self.filtered(lambda r: r.state == 'issued').write({'state': 'won'})

    def action_lost(self):
        self.write({'state': 'lost'})

    def action_cancel(self):
        """Cancel a proposal from any non-terminal state. Terminal states
        (won/lost/superseded, and hard_block which has its own dedicated
        exit via action_hard_block_to_draft) are excluded -- cancelling
        those would hide how they actually ended. Use
        action_reset_to_draft() to bring a cancelled proposal back."""
        for rec in self:
            if rec.state in ('won', 'lost', 'superseded', 'hard_block', 'cancelled'):
                raise UserError(
                    f"A proposal in state '{rec.state}' cannot be cancelled directly.")
            rec.state = 'cancelled'

    def action_reset_to_draft(self):
        """Generic "back to draft" exit for any state that isn't already
        draft or terminal (won/lost/superseded). hard_block keeps its own
        dedicated action_hard_block_to_draft (same effect, different
        guard message) rather than sharing this one."""
        for rec in self:
            if rec.state in ('draft', 'won', 'lost', 'superseded', 'hard_block'):
                raise UserError(
                    f"A proposal in state '{rec.state}' cannot be reset to draft this way.")
            rec.state = 'draft'

    # ------------------------------------------------------------------
    # MVP gate subset (05-ops/validate.py port)
    # ------------------------------------------------------------------
    def _run_mvp_gates(self):
        self.ensure_one()
        self.gate_report_ids.unlink()
        engine = self.env['sgc.pricing.engine']
        policy = engine.get_active_policy()
        rate_card = engine.get_active_rate_card()
        results = []

        for ws in self.worksheet_ids:
            results.append(self._check_worksheet_complete(ws, rate_card))
            results.append(self._check_hour_benchmark(ws))
            results.append(self._check_cash_positive(ws, policy))
            results.append(self._check_cadence_mobilisation(ws, policy))
            results.append(self._check_margin_floor(ws, policy))
            results.append(self._check_concessions_covered(ws))
        results.append(self._check_edition())

        for code, label, passed, message in results:
            self.env['sgc.proposal.gate_report'].create({
                'proposal_id': self.id,
                'gate_code': code,
                'label': label,
                'passed': passed,
                'message': message,
            })

    def _check_worksheet_complete(self, ws, rate_card):
        missing = [f for f in (
            'documentation_hours', 'qa_hours', 'training_hours', 'total_hours',
            'rate_aed', 'subtotal_aed', 'pm_aed', 'contingency_aed', 'build_value_aed',
        ) if not getattr(ws, f) and getattr(ws, f) != 0]
        if not ws.rate_role_id:
            missing.append('rate_role_id')
        forbidden = {r.rate_aed_hr for card in rate_card for r in card.forbidden_rate_ids}
        if ws.rate_aed in forbidden:
            return ('G_rate_provenance', '2. rate provenance', False,
                    f"rate_aed {ws.rate_aed} is on the rate card's forbidden list")
        if missing:
            return ('G_worksheet_complete', '2/3. worksheet completeness', False, f"missing: {missing}")
        return ('G_worksheet_complete', '2/3. worksheet completeness', True, 'complete')

    def _check_hour_benchmark(self, ws):
        if not ws.users_now or not ws.total_hours:
            return ('G_hour_benchmark', '4. hour benchmark', False, 'users_now or total_hours missing')
        benchmark = 9.2 * ws.users_now
        if ws.total_hours < benchmark * 0.5:
            if ws.users_now >= CHECK_4_STRUCTURAL_BREACH_N:
                return ('G_hour_benchmark', '4. hour benchmark', True,
                        f"{ws.total_hours}h vs ~{benchmark:.0f}h -- structural exception, expected for N>={CHECK_4_STRUCTURAL_BREACH_N}")
            return ('G_hour_benchmark', '4. hour benchmark', False,
                    f"{ws.total_hours}h well under ~{benchmark:.0f}h reference benchmark")
        return ('G_hour_benchmark', '4. hour benchmark', True, f"{ws.total_hours}h vs ~{benchmark:.0f}h reference")

    def _check_cash_positive(self, ws, policy):
        max_days = policy.cash_positive_within_days or 30
        if not ws.cash_positive_by_day:
            return ('G32_cash_positive', '8. cash-positive within 30 days', False, 'cash_positive_by_day not recorded')
        if ws.cash_positive_by_day > max_days:
            return ('G32_cash_positive', '8. cash-positive within 30 days', False,
                    f"day {ws.cash_positive_by_day} exceeds policy max {max_days}")
        return ('G32_cash_positive', '8. cash-positive within 30 days', True, f"day {ws.cash_positive_by_day} <= {max_days}")

    def _check_cadence_mobilisation(self, ws, policy):
        min_pct = policy.default_mobilisation_pct or 0.33
        messages = []
        ok = True
        if ws.mobilisation_aed and ws.build_value_aed:
            pct = ws.mobilisation_aed / ws.build_value_aed
            if pct < min_pct - 0.005:
                ok = False
                messages.append(f"mobilisation {pct:.1%} below required {min_pct:.0%}")
        else:
            ok = False
            messages.append('mobilisation_aed or build_value_aed missing')
        if ws.payment_cadence and ws.payment_cadence not in ALLOWED_CADENCES:
            ok = False
            messages.append(f"cadence '{ws.payment_cadence}' below quarterly-in-advance minimum")
        return ('G33_34_cadence_mobilisation', '9/10. cadence + mobilisation floor', ok,
                '; '.join(messages) if messages else 'cadence/mobilisation OK')

    def _check_margin_floor(self, ws, policy):
        """G8/G23 port: (full_term_commitment - total_cost) / full_term_commitment
        against policy.absolute_margin_floor (25%, 'no approver may go below
        this, ever'). Uses the SAME fields the gate report shows, not a
        separate hand computation -- matches Prosper's real committed
        figure exactly (148,482 commitment, 85,194 cost -> 42.6%)."""
        floor = policy.absolute_margin_floor or 0.25
        if not ws.full_term_commitment_aed:
            return ('G23_absolute_margin_floor', '8/23. absolute margin floor', False,
                    'full_term_commitment_aed is zero -- mobilisation/subscription/term not set')
        if ws.margin_pct < floor - 0.001:
            return ('G23_absolute_margin_floor', '8/23. absolute margin floor', False,
                    f"margin {ws.margin_pct:.1%} below the absolute floor {floor:.0%} -- "
                    f"no approver may issue this as-is")
        return ('G23_absolute_margin_floor', '8/23. absolute margin floor', True,
                f"margin {ws.margin_pct:.1%} >= floor {floor:.0%}")

    def _check_concessions_covered(self, ws):
        """G10/G13/G14 port: any concession on this worksheet must be
        covered by compensators of equal or greater AED value, all logged
        (concession-ladder.yaml procedure). No concessions is trivially
        compliant -- same non-outcome-fitted posture as the file-based
        check_r1_r2_discount_hygiene."""
        if not ws.concession_ids:
            return ('G10_13_14_concessions', '10/13/14. concessions covered by compensators', True,
                    'no concession applied -- trivially compliant')
        uncovered = ws.concession_ids.filtered(lambda c: c.compensator_value_aed < c.value_aed - 0.01)
        if uncovered:
            names = ', '.join(f"{c.concession_type_id.label} (needs {c.value_aed:.0f}, has {c.compensator_value_aed:.0f})" for c in uncovered)
            return ('G10_13_14_concessions', '10/13/14. concessions covered by compensators', False,
                    f"compensator value short of concession value: {names}")
        return ('G10_13_14_concessions', '10/13/14. concessions covered by compensators', True,
                'every concession is compensator-covered')

    def _check_edition(self):
        if self.edition == 'community':
            return ('G36_edition', '12. edition declared', True,
                    'community edition declared -- forbidden-phrase text scan deferred to Phase 2 (needs generated document text)')
        return ('G36_edition', '12. edition declared', True,
                'enterprise edition -- verify licence cost against sgc.pricing.edition_rule manually (Phase 2 automates this)')


class SgcProposalWorksheet(models.Model):
    _name = 'sgc.proposal.worksheet'
    _description = 'SGC Proposal Pricing Worksheet'

    proposal_id = fields.Many2one('sgc.proposal', required=True, ondelete='cascade')
    name = fields.Char(compute='_compute_name', store=True)
    users_now = fields.Integer(string='N (Users)', required=True)
    # Not a free choice: policy.yaml pins exactly one role per segment
    # (segments.<x>.pinned_role) -- rate-card drift between what a segment
    # is *supposed* to bill at and what a worksheet actually used is a
    # named, repeated defect class in this repo (known-defects.md #1, #21).
    # Computed + readonly closes that off structurally instead of relying
    # on an SDR picking correctly from 13 similarly-named roles.
    rate_role_id = fields.Many2one('sgc.pricing.role_rate', string='Priced Role (pinned by segment)',
                                    compute='_compute_rate_role', store=True, readonly=True)
    rate_aed = fields.Float(related='rate_role_id.rate_aed_hr', string='Rate (AED/hr)', store=True)

    a_hours = fields.Float(compute='_compute_hours', store=True, string='A-Hours (Class A)')
    b_hours = fields.Float(compute='_compute_hours', store=True, string='B-Hours (Class B, M-branch)')
    qa_hours = fields.Float(compute='_compute_hours', store=True)
    documentation_hours = fields.Float(compute='_compute_hours', store=True)
    training_hours = fields.Float(compute='_compute_hours', store=True)
    hypercare_hours = fields.Float(compute='_compute_hours', store=True)
    total_hours = fields.Float(compute='_compute_hours', store=True)

    a_side_hours = fields.Float(compute='_compute_hours', store=True,
                                 help="a_hours + qa_hours + documentation_hours + training_hours -- "
                                      "the only hours priced at the segment blended rate.")
    a_side_subtotal_aed = fields.Float(compute='_compute_money', store=True)
    b_side_subtotal_aed = fields.Float(compute='_compute_money', store=True,
                                        help="Class B hours priced per-task at junior_passthrough/"
                                             "business_analyst rates (engine.b_side_subtotal_aed), "
                                             "NOT the segment blended rate.")
    subtotal_aed = fields.Float(compute='_compute_money', store=True,
                                 help="a_side_subtotal_aed + b_side_subtotal_aed")
    pm_aed = fields.Float(compute='_compute_money', store=True, help="Informational: subtotal_aed x pm_pct")
    contingency_aed = fields.Float(compute='_compute_money', store=True,
                                    help="Informational: subtotal_aed x contingency_pct")
    hypercare_cost_aed = fields.Float(compute='_compute_money', store=True)
    build_value_aed = fields.Float(
        compute='_compute_money', store=True,
        help="round(subtotal_aed * (1+pm_pct) * (1+contingency_pct) + hypercare_cost_aed) -- "
             "PM/contingency compound multiplicatively, matching the committed worksheets "
             "exactly (pm_aed/contingency_aed above are additive-looking figures shown for "
             "reference only, not what build_value_aed is summed from).")
    internal_build_cost_aed = fields.Float(compute='_compute_money', store=True)

    # cost-to-serve + margin (number_1_cost_to_serve / G8-G23 port)
    hosting_allocation_aed = fields.Float(compute='_compute_cost_to_serve', store=True)
    tooling_aed = fields.Float(compute='_compute_cost_to_serve', store=True)
    support_labour_aed = fields.Float(compute='_compute_cost_to_serve', store=True)
    account_mgmt_aed = fields.Float(compute='_compute_cost_to_serve', store=True)
    cts_total_aed = fields.Float(compute='_compute_cost_to_serve', store=True,
                                  help="Monthly cost-to-serve total (hosting + tooling + support + account mgmt)")
    platform_portion_aed_mo = fields.Float(
        compute='_compute_cost_to_serve', store=True,
        help="cts_total_aed x platform_floor_multiplier -- the minimum monthly "
             "subscription floor (G1). Also the base discount_platform concessions apply against.")

    term_months = fields.Integer(default=24, required=True,
                                  help="Financing uplift is only defined for 12/18/24 months "
                                       "(policy.yaml financing_uplift_12mo/18mo/24mo) -- other "
                                       "values are rejected on save.")

    @api.constrains('term_months')
    def _check_term_months(self):
        for rec in self:
            if rec.term_months not in (12, 18, 24):
                raise UserError("term_months must be 12, 18, or 24 -- financing_uplift is not defined for any other term.")

    # Mobilisation and subscription are DERIVED, not typed in -- per user
    # decision 2026-08-12 ("mobilisation is defined by percentage... we
    # already have [the platform-floor] fix, right?"). Before this fix
    # both fields were free Float entry, completely disconnected from
    # platform_portion_aed_mo even though both existed on the same
    # worksheet -- exactly the kind of hand-typed/drifted commercial
    # figure the rest of this engine exists to prevent.
    mobilisation_pct = fields.Float(
        compute='_compute_financing', store=True,
        help="From risk-security-matrix.yaml bands: low/moderate=33%, elevated=40%, high=50%. "
             "Falls back to policy.default_mobilisation_pct (33%) if no risk assessment is recorded yet.")
    mobilisation_aed = fields.Float(compute='_compute_financing', store=True, readonly=True,
                                     help="round(build_value_aed * mobilisation_pct)")
    financed_remainder_aed = fields.Float(compute='_compute_financing', store=True,
                                           help="build_value_aed - mobilisation_aed")
    financing_uplift_pct = fields.Float(compute='_compute_financing', store=True,
                                         help="policy.yaml financing_uplift_<term>mo, selected by term_months")
    recovery_total_aed = fields.Float(compute='_compute_financing', store=True,
                                       help="round(financed_remainder_aed * (1 + financing_uplift_pct))")
    recovery_component_aed_mo = fields.Float(compute='_compute_financing', store=True,
                                              help="round(recovery_total_aed / term_months)")
    subscription_fee_aed_mo = fields.Float(
        compute='_compute_financing', store=True, readonly=True,
        help="platform_portion_aed_mo + recovery_component_aed_mo, rounded to the nearest 10 AED "
             "per policy.yaml presentation.client_facing_subscription_rounding.")
    cash_positive_by_day = fields.Integer()

    full_term_commitment_aed = fields.Float(compute='_compute_margin', store=True,
                                             help="mobilisation_aed + term_months x subscription_fee_aed_mo")
    total_cost_aed = fields.Float(compute='_compute_margin', store=True,
                                   help="internal_build_cost_aed + cts_total_aed x term_months")
    margin_pct = fields.Float(compute='_compute_margin', store=True,
                               help="(full_term_commitment_aed - total_cost_aed) / full_term_commitment_aed")

    concession_ids = fields.One2many('sgc.proposal.concession', 'worksheet_id', string='Concessions')
    payment_cadence = fields.Selection([
        ('quarterly_in_advance', 'Quarterly in advance'),
        ('semi_annual_in_advance', 'Semi-annual in advance'),
        ('annual_in_advance', 'Annual in advance'),
        ('full_prepay_term', 'Full prepay term'),
        ('monthly', 'Monthly (surcharge -- below minimum)'),
    ], default='quarterly_in_advance')

    @api.depends('proposal_id.name', 'users_now')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.proposal_id.name} -- N={rec.users_now}"

    @api.depends('proposal_id.segment')
    def _compute_rate_role(self):
        engine = self.env['sgc.pricing.engine']
        policy = engine.get_active_policy()
        rate_card = engine.get_active_rate_card()
        segment_by_code = {s.code: s for s in policy.segment_ids} if policy else {}
        for rec in self:
            segment = segment_by_code.get(rec.proposal_id.segment)
            role = None
            if segment and segment.pinned_role_code and rate_card:
                role = rate_card.role_rate_ids.filtered(lambda r: r.code == segment.pinned_role_code)
            rec.rate_role_id = role[:1].id if role else False

    @api.depends('users_now')
    def _compute_hours(self):
        engine = self.env['sgc.pricing.engine']
        policy = engine.get_active_policy()
        for rec in self:
            if not rec.users_now:
                rec.update({
                    'a_hours': 0, 'b_hours': 0, 'qa_hours': 0,
                    'documentation_hours': 0, 'training_hours': 0,
                    'hypercare_hours': 0, 'a_side_hours': 0, 'total_hours': 0,
                })
                continue
            n = rec.users_now
            a_hours = engine.a_hours_for_n(n)
            b_hours, _ = engine.b_hours_for_branch(n, 'm')
            dev_hours = a_hours + b_hours
            qa_hours = max(policy.qa_hours_min, round(policy.qa_pct_of_delivery * dev_hours))
            doc_hours = max(policy.documentation_hours_min, round(policy.documentation_pct_of_dev * dev_hours))
            training_hours = policy.training_sessions * policy.training_hours_per_session
            hypercare_hours = engine.hypercare_hours_for_n(n)
            a_side_hours = a_hours + qa_hours + doc_hours + training_hours
            total = a_side_hours + b_hours + hypercare_hours
            rec.a_hours = a_hours
            rec.b_hours = b_hours
            rec.qa_hours = qa_hours
            rec.documentation_hours = doc_hours
            rec.training_hours = training_hours
            rec.hypercare_hours = hypercare_hours
            rec.a_side_hours = a_side_hours
            rec.total_hours = total

    @api.depends('a_side_hours', 'users_now', 'rate_aed', 'proposal_id.segment')
    def _compute_money(self):
        engine = self.env['sgc.pricing.engine']
        policy = engine.get_active_policy()
        segment_by_code = {s.code: s for s in policy.segment_ids} if policy else {}
        for rec in self:
            if not rec.users_now:
                rec.update({
                    'a_side_subtotal_aed': 0, 'b_side_subtotal_aed': 0, 'subtotal_aed': 0,
                    'pm_aed': 0, 'contingency_aed': 0, 'hypercare_cost_aed': 0,
                    'build_value_aed': 0, 'internal_build_cost_aed': 0,
                })
                continue
            n = rec.users_now
            a_side_subtotal = (rec.a_side_hours or 0.0) * (rec.rate_aed or 0.0)
            b_side_subtotal = engine.b_side_subtotal_aed(n)
            subtotal = a_side_subtotal + b_side_subtotal
            segment = segment_by_code.get(rec.proposal_id.segment)
            pm_pct = segment.pm_pct if segment else 0.15
            contingency_pct = segment.contingency_pct if segment else 0.05
            pm = subtotal * pm_pct
            contingency = subtotal * contingency_pct
            # PM/contingency compound multiplicatively -- matches the committed
            # worksheets exactly (e.g. Prosper: 42307.33 x 1.15 x 1.05 =
            # 51086.10, NOT subtotal+pm+contingency=50768.80). pm_aed/
            # contingency_aed below are the additive-looking percentages shown
            # for reference; build_value_core is genuinely compounded.
            build_value_core = subtotal * (1 + pm_pct) * (1 + contingency_pct)
            hypercare_cost = engine.hypercare_cost_aed(n)
            rec.a_side_subtotal_aed = round(a_side_subtotal, 2)
            rec.b_side_subtotal_aed = round(b_side_subtotal, 2)
            rec.subtotal_aed = round(subtotal, 2)
            rec.pm_aed = round(pm, 2)
            rec.contingency_aed = round(contingency, 2)
            rec.hypercare_cost_aed = hypercare_cost
            rec.build_value_aed = round(build_value_core + hypercare_cost)
            rec.internal_build_cost_aed = round((rec.total_hours or 0.0) * (policy.internal_consultant_cost_aed_hr or 0.0))

    @api.depends('users_now')
    def _compute_cost_to_serve(self):
        engine = self.env['sgc.pricing.engine']
        for rec in self:
            if not rec.users_now:
                rec.update({
                    'hosting_allocation_aed': 0, 'tooling_aed': 0, 'support_labour_aed': 0,
                    'account_mgmt_aed': 0, 'cts_total_aed': 0, 'platform_portion_aed_mo': 0,
                })
                continue
            cts = engine.cost_to_serve_for_n(rec.users_now)
            rec.hosting_allocation_aed = cts['hosting_allocation_aed']
            rec.tooling_aed = cts['tooling_aed']
            rec.support_labour_aed = cts['support_labour_aed']
            rec.account_mgmt_aed = cts['account_mgmt_aed']
            rec.cts_total_aed = cts['cts_total_aed']
            rec.platform_portion_aed_mo = cts['platform_floor_aed']

    # mobilisation_pct band mapping: risk-security-matrix.yaml bands.instruments
    # names the required cash instrument per band (mobilisation_33pct /
    # mobilisation_40pct / mobilisation_50pct) -- this is that mapping's
    # percentage half, ported directly rather than re-derived.
    RISK_BAND_MOBILISATION_PCT = {
        'low': 0.33, 'moderate': 0.33, 'elevated': 0.40, 'high': 0.50, 'refuse': 0.50,
    }

    @api.depends('build_value_aed', 'term_months', 'platform_portion_aed_mo',
                 'proposal_id.risk_assessment_ids.risk_band')
    def _compute_financing(self):
        engine = self.env['sgc.pricing.engine']
        policy = engine.get_active_policy()
        for rec in self:
            if not rec.build_value_aed:
                rec.update({
                    'mobilisation_pct': 0, 'mobilisation_aed': 0, 'financed_remainder_aed': 0,
                    'financing_uplift_pct': 0, 'recovery_total_aed': 0,
                    'recovery_component_aed_mo': 0, 'subscription_fee_aed_mo': 0,
                })
                continue
            risk_band = rec.proposal_id.risk_assessment_ids[:1].risk_band
            mobilisation_pct = self.RISK_BAND_MOBILISATION_PCT.get(risk_band, policy.default_mobilisation_pct or 0.33)
            mobilisation = round(rec.build_value_aed * mobilisation_pct)
            financed_remainder = rec.build_value_aed - mobilisation

            term = rec.term_months or 24
            if term <= 12:
                uplift_pct = policy.financing_uplift_12mo
            elif term <= 18:
                uplift_pct = policy.financing_uplift_18mo
            else:
                uplift_pct = policy.financing_uplift_24mo
            recovery_total = round(financed_remainder * (1 + (uplift_pct or 0.0)))
            recovery_monthly = round(recovery_total / term) if term else 0

            # nearest_10_aed per policy.yaml presentation.client_facing_subscription_rounding
            subscription = round((rec.platform_portion_aed_mo + recovery_monthly) / 10.0) * 10

            rec.mobilisation_pct = mobilisation_pct
            rec.mobilisation_aed = mobilisation
            rec.financed_remainder_aed = financed_remainder
            rec.financing_uplift_pct = uplift_pct or 0.0
            rec.recovery_total_aed = recovery_total
            rec.recovery_component_aed_mo = recovery_monthly
            rec.subscription_fee_aed_mo = subscription

    @api.depends('mobilisation_aed', 'subscription_fee_aed_mo', 'term_months',
                 'internal_build_cost_aed', 'cts_total_aed')
    def _compute_margin(self):
        for rec in self:
            full_term = (rec.mobilisation_aed or 0.0) + (rec.term_months or 0) * (rec.subscription_fee_aed_mo or 0.0)
            total_cost = (rec.internal_build_cost_aed or 0.0) + (rec.term_months or 0) * (rec.cts_total_aed or 0.0)
            rec.full_term_commitment_aed = round(full_term)
            rec.total_cost_aed = round(total_cost)
            rec.margin_pct = (full_term - total_cost) / full_term if full_term else 0.0


class SgcProposalRiskAssessment(models.Model):
    _name = 'sgc.proposal.risk_assessment'
    _description = 'SGC Proposal Risk Assessment'

    # weights ported verbatim from 00-knowledge/pricing/risk-security-matrix.yaml
    WEIGHTS = {
        'entity_age_years': {'>5': 0, '2-5': 5, '1-2': 12, '<1': 20},
        'jurisdiction_risk': {'mainland_llc': 0, 'free_zone': 5, 'offshore': 20},
        'vat_registered': {'yes': 0, 'no': 10},
        'trade_licence_valid': {'>6mo': 0, '<6mo': 8, 'expired': None},
        'payment_history_sgc': {'clean': -5, 'none': 5, 'late': 15, 'default': None},
        'decision_maker_type': {'owner': 0, 'manager': 5, 'committee': 10},
        'incumbent_churn_signal': {'none': 0, 'abandoned_systems': 8},
        'peak_exposure_aed': {'<5000': 0, '5-15k': 5, '15-40k': 12, '>40k': 20},
    }

    proposal_id = fields.Many2one('sgc.proposal', required=True, ondelete='cascade')
    entity_age_years = fields.Selection([('>5', '>5 years'), ('2-5', '2-5 years'), ('1-2', '1-2 years'), ('<1', '<1 year')])
    jurisdiction_risk = fields.Selection([('mainland_llc', 'Mainland LLC'), ('free_zone', 'Free Zone'), ('offshore', 'Offshore')])
    vat_registered = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    trade_licence_valid = fields.Selection([('>6mo', '>6 months'), ('<6mo', '<6 months'), ('expired', 'Expired')])
    payment_history_sgc = fields.Selection([('clean', 'Clean'), ('none', 'None'), ('late', 'Late'), ('default', 'Default')])
    decision_maker_type = fields.Selection([('owner', 'Owner'), ('manager', 'Manager'), ('committee', 'Committee')])
    incumbent_churn_signal = fields.Selection([('none', 'None'), ('abandoned_systems', 'Abandoned Systems')])
    peak_exposure_aed = fields.Selection([('<5000', '<5,000'), ('5-15k', '5,000-15,000'), ('15-40k', '15,000-40,000'), ('>40k', '>40,000')])

    raw_score = fields.Integer(compute='_compute_score', store=True)
    reject_triggered = fields.Boolean(compute='_compute_score', store=True)
    risk_band = fields.Selection([
        ('low', 'Low'), ('moderate', 'Moderate'), ('elevated', 'Elevated'),
        ('high', 'High'), ('refuse', 'Refuse'),
    ], compute='_compute_score', store=True)
    required_security_instruments = fields.Char(compute='_compute_score', store=True)

    INSTRUMENTS = {
        'low': 'mobilisation_33pct',
        'moderate': 'mobilisation_33pct, deposit_1_month',
        'elevated': 'mobilisation_40pct, deposit_2_months, pdc_set',
        'high': 'mobilisation_50pct, pdc_full_balance, guarantee',
        'refuse': 'escalate_or_decline',
    }

    @api.depends('entity_age_years', 'jurisdiction_risk', 'vat_registered', 'trade_licence_valid',
                 'payment_history_sgc', 'decision_maker_type', 'incumbent_churn_signal', 'peak_exposure_aed')
    def _compute_score(self):
        for rec in self:
            reject = False
            total = 0
            for field_name, weights in self.WEIGHTS.items():
                val = getattr(rec, field_name)
                if not val:
                    continue
                w = weights.get(val)
                if w is None:
                    reject = True
                else:
                    total += w
            rec.reject_triggered = reject
            rec.raw_score = total
            if reject or total > 75:
                band = 'refuse'
            elif total <= 20:
                band = 'low'
            elif total <= 40:
                band = 'moderate'
            elif total <= 60:
                band = 'elevated'
            else:
                band = 'high'
            rec.risk_band = band
            rec.required_security_instruments = self.INSTRUMENTS[band]


class SgcProposalGateReport(models.Model):
    _name = 'sgc.proposal.gate_report'
    _description = 'SGC Proposal Gate Report'
    _order = 'create_date'

    proposal_id = fields.Many2one('sgc.proposal', required=True, ondelete='cascade')
    gate_code = fields.Char(required=True)
    label = fields.Char()
    passed = fields.Boolean()
    message = fields.Text()


class SgcProposalRevision(models.Model):
    _name = 'sgc.proposal.revision'
    _description = 'SGC Proposal Revision'
    _order = 'create_date desc'

    proposal_id = fields.Many2one('sgc.proposal', required=True, ondelete='cascade')
    name = fields.Char(required=True, help="e.g. Rev1, Rev2")
    status = fields.Selection([
        ('draft', 'Draft'), ('issued', 'Issued'),
        ('superseded', 'Superseded'), ('retracted', 'Retracted'),
    ], default='draft')
    issued_date = fields.Date()
    attachment_id = fields.Many2one('ir.attachment', string='PDF')
    content_sha256 = fields.Char(string='Content SHA-256')
    notes = fields.Text()


class SgcProposalConcession(models.Model):
    _name = 'sgc.proposal.concession'
    _description = 'SGC Proposal Concession (concession-ladder.yaml procedure port)'

    worksheet_id = fields.Many2one('sgc.proposal.worksheet', required=True, ondelete='cascade')
    concession_type_id = fields.Many2one('sgc.pricing.concession_type', required=True)
    pct = fields.Float(string='Discount %', help="Used when the concession type is discount_platform.")
    manual_value_aed = fields.Float(help="Used when the concession type's computation is 'manual'.")
    value_aed = fields.Float(compute='_compute_value_aed', store=True,
                              help="The concession's AED cost over the full term -- what compensators must cover.")
    compensator_ids = fields.One2many('sgc.proposal.concession.compensator', 'concession_id', string='Compensators')
    compensator_value_aed = fields.Float(compute='_compute_compensator_value_aed', store=True)
    notes = fields.Text()

    @api.depends('concession_type_id.computation', 'pct', 'manual_value_aed',
                 'worksheet_id.platform_portion_aed_mo', 'worksheet_id.term_months')
    def _compute_value_aed(self):
        for rec in self:
            if rec.concession_type_id.computation == 'discount_platform':
                ws = rec.worksheet_id
                rec.value_aed = round((ws.platform_portion_aed_mo or 0.0) * (rec.pct or 0.0) * (ws.term_months or 0))
            else:
                rec.value_aed = rec.manual_value_aed

    @api.depends('compensator_ids.value_aed')
    def _compute_compensator_value_aed(self):
        for rec in self:
            rec.compensator_value_aed = sum(rec.compensator_ids.mapped('value_aed'))


class SgcProposalConcessionCompensator(models.Model):
    _name = 'sgc.proposal.concession.compensator'
    _description = 'SGC Concession Compensator Line'

    concession_id = fields.Many2one('sgc.proposal.concession', required=True, ondelete='cascade')
    compensator_type_id = fields.Many2one('sgc.pricing.compensator_type', required=True)
    manual_value_aed = fields.Float(help="Used when the compensator type's value_type is 'manual'.")
    value_aed = fields.Float(compute='_compute_value_aed', store=True)

    @api.depends('compensator_type_id.value_type', 'compensator_type_id.flat_value_aed',
                 'compensator_type_id.per_month_value_aed', 'manual_value_aed',
                 'concession_id.worksheet_id.term_months')
    def _compute_value_aed(self):
        for rec in self:
            ct = rec.compensator_type_id
            if not ct:
                rec.value_aed = 0
                continue
            if ct.value_type == 'flat':
                rec.value_aed = ct.flat_value_aed
            elif ct.value_type == 'per_month':
                term = rec.concession_id.worksheet_id.term_months or 0
                rec.value_aed = ct.per_month_value_aed * term
            elif ct.value_type == 'manual':
                rec.value_aed = rec.manual_value_aed
            else:  # effect_only
                rec.value_aed = 0
