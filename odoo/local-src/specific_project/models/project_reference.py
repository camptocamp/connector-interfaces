# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from openerp import api, fields, models
from openerp.addons.website.models.website import slug


class ProjectReference(models.Model):
    """ProjectReference contains projects to be shown on member's profile. Can
    link to other partners.
    """

    _name = 'project.reference'
    _description = "Project reference"
    _inherit = [
        'mail.thread', 'ir.needaction_mixin',
        'website.published.mixin']
    name = fields.Char(
        string="Project Name",
        required=True
    )
    implementation_date = fields.Date(string="Date of implementation")
    location = fields.Char()
    industry_ids = fields.Many2many(
        comodel_name="res.partner.category",
        string="Industries",
    )
    expertise_ids = fields.Many2many(
        comodel_name="partner.project.expertise",
        string="Expertises",
    )
    image = fields.Binary(
        "Reference image"
    )
    description = fields.Text()
    video_url = fields.Char(
        string='Video URL',
    )
    owner_id = fields.Many2one(
        comodel_name='res.users',
        string="Project Owner",
        required=True,
    )
    linked_partner_ids = fields.Many2many(
        comodel_name="res.users",
        string="Referenced partners",
    )

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
        res = super(ProjectReference, self)._website_url(name, arg)
        res.update({(p.id, '/my/references/%s' % slug(p)) for p in self})
        return res
