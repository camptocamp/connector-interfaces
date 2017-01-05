# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import http
from openerp.http import request


class WebsiteReference(http.Controller):
    """Controller for reference model."""

    @http.route([
        '/references/<model("project.reference"):reference>',
    ], type='http', auth='public', website=True)
    def reference_detail(self, reference, **kw):
        values = {
            'reference': reference
        }
        return request.website.render("specific_project.reference_detail",
                                      values)
