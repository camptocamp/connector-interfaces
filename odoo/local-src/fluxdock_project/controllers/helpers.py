# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import json
from odoo import http
from odoo.http import request


class JSHelpers(http.Controller):
    """Controller for some JS stuff."""

    @http.route(['/references/json'], type='http', auth="public", website=True)
    def references_aggr(self, *arg, **kwargs):
        """Return JSON data for references aggregation.

        References are loaded randomly as requested here:
        https://redmine.iart.ch/issues/16412
        """

        env = request.env
        query = (
            "SELECT * FROM ("
            "SELECT DISTINCT id FROM project_reference "
            "WHERE website_published = %s "
            ") items "
            "ORDER BY random()"
        )
        qargs = [True, ]
        if kwargs.get('limit'):
            query += ' limit %s'
            qargs.append(kwargs.get('limit'))
        env.cr.execute(query, qargs)
        ids = [x[0] for x in env.cr.fetchall()]
        res = []
        if ids:
            items = env['project.reference'].sudo().browse(ids)
            for item in items:
                res.append({
                    'id': item.id,
                    'name': item.name,
                    'website_url': item.website_url,
                    'image_url': item.image_url,
                })
        return json.dumps({
            'ok': True,
            'results': res,
        })
