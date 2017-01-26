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
        'mail.thread',
        'ir.needaction_mixin',
        'website.published.mixin',
    ]

    # we use this for website template add action
    cms_add_url = '/references/add'
    cms_after_delete_url = '/my/home'

    @api.multi
    def _compute_cms_edit_url(self):
        for item in self:
            item.cms_edit_url = item.website_url + '/edit'

    name = fields.Char(
        string="Reference title",
        required=True
    )
    implementation_date = fields.Date(
        string="Implementation date",
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

    @api.model
    def create(self, vals):
        res = super(ProjectReference, self).create(vals)
        if not self.env.context.get('no_profile_update'):
            partner = res.create_uid.partner_id
            if partner:
                # TODO: set proper rule/permission to do this w/ no sudo
                partner.sudo().update_profile_state()
        return res
