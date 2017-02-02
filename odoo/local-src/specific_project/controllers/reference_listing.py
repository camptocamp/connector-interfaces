# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import http
from openerp.addons.cms_form.controllers import SearchFormControllerMixin


class ReferenceListing(http.Controller, SearchFormControllerMixin):

    template = 'specific_project.reference_search_form_wrapper'

    @http.route([
        '/references',
        '/references/page/<int:page>',
    ], type='http', auth="public", website=True)
    def market(self, **kw):
        model = 'project.reference'
        return self.make_response(model, **kw)
