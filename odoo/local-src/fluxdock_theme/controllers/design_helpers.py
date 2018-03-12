# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import http
from odoo.http import request


class DesignHelpers(http.Controller):
    """Views for visual componentss."""

    @http.route(
        ['/flux-design/2-cols'],
        type='http', auth="public", website=True)
    def layout_2_cols(self, **post):
        vals = {
            'section_logo':
                '/fluxdock_theme/static/img/content-icons/collaborative.png',
            'section_title': 'Test section',
        }
        return request.render("fluxdock_theme.test_2cols_layout", vals)

    @http.route(
        ['/flux-design/gradients'],
        type='http', auth="public", website=True)
    def gradients(self, **post):
        return request.render("fluxdock_theme.gradients", {})
