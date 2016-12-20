# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from openerp import api, fields, models
from openerp.addons.website.models.website import slug

STATIC_FOLDER = '/specific_project/static'


class ProjectReference(models.Model):
    """ProjectReference contains projects to be shown on member's profile. Can
    link to other partners.
    """

    _name = 'project.reference'
    _description = "Project reference"
    _inherit = [
        'mail.thread', 'ir.needaction_mixin',
        'website.published.mixin']

    # we use this for website template add action
    website_add_url = '/references/add'

    name = fields.Char(
        string="Project Name",
        required=True
    )
    implementation_date = fields.Date(
        string="Date of implementation",
        required=False,
    )
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
        "Reference image",
        attachment=True,
    )
    website_short_description = fields.Text(string="Description")
    video_url = fields.Char(
        string='Video URL',
    )
    ext_website_url = fields.Char(
        string='External Website URL',
    )
    linked_partner_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Referenced partners",
    )
    create_uid = fields.Many2one(
        'res.users',
        'Owner',
        select=True,
        readonly=True,
    )
    image_url = fields.Char(
        string='Main image URL',
        compute='_compute_image_url',
        default='',
    )
    country_id = fields.Many2one(comodel_name='res.country', string="Country")

    @api.multi
    @api.depends('image')
    def _compute_image_url(self):
        ws_model = self.env['website']
        for item in self:
            if item.image:
                image_url = ws_model.image_url(item, 'image')
            else:
                image_url = STATIC_FOLDER \
                    + '/src/img/reference_placeholder.png'
            item.image_url = image_url

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
        res.update({(p.id, '/references/%s' % slug(p)) for p in self})
        return res
