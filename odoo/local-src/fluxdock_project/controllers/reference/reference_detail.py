# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import http
from odoo.http import request


class ReferenceDetail(http.Controller):
    """Controller for reference model."""

    @http.route([
        '/dock/references/<model("project.reference"):reference>',
    ], type='http', auth='public', website=True)
    def reference_detail(self, reference, **kw):
        return request.render("fluxdock_project.reference_detail", {
            'proposal': reference,
            'main_object': reference,
        })
