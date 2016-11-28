# -*- coding: utf-8 -*-
# © 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import http
from openerp.addons.web.controllers.main import DataSet as DataSetBase


# This is a workaround to allow to use odoo js api for anonymous users.
# Since the original method `/web/dataset/call_kw` has `auth=user`
# we cannot use it because we have no session.
# Model's access rights seems well handled by ACLs
# but to stay secure I'm just enabling this only for some models.
# An OCA module is going to avoid this problem,
# will come from this PR https://github.com/OCA/web/pull/402


class DataSet(DataSetBase):
    @http.route([
        '/web/dataset/call_kw_pub',
        '/web/dataset/call_kw_pub/<path:path>'
    ], type='json', auth="public")
    def call_kw_pub(self, model, method, args, kwargs, path=None):
        if model not in ('partner.project.expertise', 'res.partner.category'):
            return http.request.not_found()
        return self._call_kw(model, method, args, kwargs)
