# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class OverrideMyHome(CustomerPortal):

    @http.route()
    def home(self, **kw):
        return request.redirect('/my/dock', code=301)


class MyDock(http.Controller):

    my_dock_template = 'fluxdock_project.my_dock'

    @http.route([
        '/my/dock',
    ], type='http', auth='user', website=True)
    def my_dock(self, **kw):
        return request.render(self.my_dock_template, {})
