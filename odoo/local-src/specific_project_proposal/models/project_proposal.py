# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from datetime import datetime, timedelta

from openerp import _, api, exceptions, fields, models
from openerp.addons.website.models.website import slug


class ProjectProposal(models.Model):
    """ProjectProposal contains future project set on market place to find
    partners and collaborators. """

    _name = 'project.proposal'
    _description = "Project proposal"
    _inherit = [
        'mail.thread', 'ir.needaction_mixin',
        'website.published.mixin']
    name = fields.Char(
        string="Project Name",
        required=True
    )
    owner_id = fields.Many2one(
        comodel_name='res.users',
        string="Project Owner",
        required=True,
    )
    color_owner_id = fields.Integer(
        compute='_get_color_owner_id',
        string="Color index of owner",
        store=False)  # Color of owner
    location = fields.Char()
    country_id = fields.Many2one(comodel_name='res.country', string="Country")
    website_short_description = fields.Char(string="Teaser text")
    website_description = fields.Text()
    start_date = fields.Date(string="Start date")
    stop_date = fields.Date(string="End date")
    duration = fields.Integer()
    industry_ids = fields.Many2many(
        comodel_name="res.partner.category",
        string="Industries",
    )
    expertise_ids = fields.Many2many(
        comodel_name="partner_project_expertise.expertise",
        string="Expertises",
    )

    is_new = fields.Boolean(
        compute='_is_new'
    )

    @api.depends('owner_id')
    def _get_color_owner_id(self):
        for rec in self:
            rec.color_owner_id = rec.owner_id.id

    @api.multi
    def toggle_published(self):
        """ Inverse the value of the field ``published`` on the records in
        ``self``.
        """
        for record in self:
            record.website_published = not record.website_published

    @api.multi
    @api.depends('name')
    def _website_url(self, name, arg):
        res = super(ProjectProposal, self)._website_url(name, arg)
        res.update({(p.id, '/proposals/detail/%s' % slug(p)) for p in self})
        return res

    @api.multi
    def _is_new(self):
        for rec in self:
            create_date = fields.Datetime.from_string(rec.create_date)
            rec.is_new = (datetime.now() - create_date).days < 15

    @api.multi
    def blacklist(self):
        self.env.user.proposal_blacklist_ids |= self

    @api.multi
    def unblacklist(self):
        self.env.user.proposal_blacklist_ids -= self

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
            if (rec.start_date and rec.stop_date and
                    rec.stop_date < rec.start_date):
                raise exceptions.UserError(
                    _('End Date cannot be set before Start Date.'))
