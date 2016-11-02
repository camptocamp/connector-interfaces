# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import json
from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.addons.website.models.website import slug


class JSHelpers(http.Controller):
    """Controller for some JS stuff."""

    @http.route(['/members/json'], type='http', auth="public", website=True)
    def member_aggr(self, *arg, **post):
        """Return JSON data for members aggregation."""

        env = request.env

        # FIXME
        domain = []

        members = env['res.partner'].sudo().search(domain, limit=24)
        res = []
        for item in members:
            res.append({
                'id': item.id,
                'name': item.name,
                'url': '/members/{}'.format(slug(item)),
                'avatar_url': request.website.image_url(
                    item, 'image', '128x36')
            })
        return json.dumps({
            'ok': True,
            'members': res,
        })
