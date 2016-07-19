# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from datetime import timedelta

from openerp import _, api, exceptions, fields, models


class ProjectProposal(models.Model):
    """ProjectProposal contains future project set on market place to find
    partners and collaborators. """

    _name = 'project.proposal'
    _description = "Project proposal"
    _inherit = ["mail.thread", "ir.needaction_mixin"]

    name = fields.Char(
        string="Project Name",
        required=True
    )
    owner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Project Owner",
        required=True,
    )
    color_owner_id = fields.Integer(
        compute='_get_color_owner_id',
        string="Color index of owner",
        store=False)  # Color of owner
    location = fields.Char()
    teaser_text = fields.Char(string="Teaser text")
    description = fields.Text()
    start_date = fields.Date(string="Start date")
    stop_date = fields.Date(string="End date")
    duration = fields.Integer()
    industry_ids = fields.Many2many(
        comodel_name="project.industry",
        string="Industries",
    )
    expertise_ids = fields.Many2many(
        comodel_name="project.expertise",
        string="Expertises",
    )

    @api.depends('owner_id')
    def _get_color_owner_id(self):
        for rec in self:
            rec.color_owner_id = rec.owner_id.id

    @api.onchange('start_date', 'stop_date')
    def onchange_dates(self):
        if not self.start_date or not self.stop_date:
            return
        start = fields.Datetime.from_string(self.start_date)
        stop = fields.Datetime.from_string(self.stop_date)
        self.duration = (stop - start).days

    @api.onchange('duration')
    def onchange_duration(self):
        if not self.start_date or not self.duration:
            return
        start = fields.Datetime.from_string(self.start_date)
        end = start + timedelta(days=self.duration)
        self.stop_date = end

    @api.constrains('start_date', 'stop_date')
    def _check_date_order(self):
        for rec in self:
            if (rec.start_date and rec.start_date and
                    rec.stop_date < rec.start_date):
                raise exceptions.UserError(
                    _('End Date cannot be set before Start Date.'))
