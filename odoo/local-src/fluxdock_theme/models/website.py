# Copyright 2016 Simone Orsi (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, api, fields
from odoo.http import request


def smart_truncate(text, length=100, suffix='...'):
    """Smart truncate text."""
    # http://stackoverflow.com/questions/250357/
    # truncate-a-string-without-ending-in-the-middle-of-a-word
    text = text or ''
    if len(text) <= length:
        return text
    else:
        return ' '.join(text[:length + 1].split(' ')[0:-1]) + suffix


class Website(models.Model):
    _inherit = 'website'

    @api.model
    def truncate_text(self, text, length=100, suffix='...'):
        """Truncate text."""
        return smart_truncate(text, length=length, suffix=suffix)

    @api.model
    def image_url(self, record, field, size=None):
        if record._name == 'res.partner':
            if field == 'image' and not record.image:
                return '/fluxdock_theme/static/img/member-placeholder.png'
        return super(Website, self).image_url(record, field, size=size)

    @api.model
    def get_extra_body_klass(self, _request=None):
        _request = _request or request
        klasses = []
        if _request.session.uid:
            klasses.append('authenticated_user')
        return ' '.join(klasses)

    @staticmethod
    def menu_item_is_active(path):
        return request.httprequest.path.startswith(path)

    def _get_dock_context_menu(self):
        """Centralized menu for `dock` section."""

        # TODO: get rid of this once we have cms.page
        # w/ auto context nav in place.
        return []


class WebsiteMixin(models.AbstractModel):
    _inherit = 'website.published.mixin'

    # placeholder fields to make image_url compute method happy
    image = fields.Binary('image')
    image_url = fields.Char(
        string='Main image URL',
        compute='_compute_image_url',
        default='',
        readonly=1,
    )

    @api.multi
    @api.depends('image')
    def _compute_image_url(self):
        ws_model = self.env['website']
        for item in self:
            image_url = ''
            if item.image:
                image_url = ws_model.image_url(item, 'image')
            item.image_url = image_url
