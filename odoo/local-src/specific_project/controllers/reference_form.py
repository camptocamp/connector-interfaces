# -*- coding: utf-8 -*-

from openerp import http
from openerp.addons.cms_form.controllers.main import FormControllerMixin


class ReferenceFormController(http.Controller, FormControllerMixin):
    """Reference form controller."""

    @http.route([
        '/references/add',
        '/references/<model("project.reference"):reference>/edit',
    ], type='http', auth='user', website=True)
    def cms_form(self, reference=None, **kw):
        """Handle a `form` route.
        """
        model = 'project.reference'
        return self.make_response(
            model, model_id=reference and reference.id, **kw)
