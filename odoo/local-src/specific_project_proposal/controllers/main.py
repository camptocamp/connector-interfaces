# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from openerp import http
from openerp.http import request

from openerp.addons.website_portal_profile.controllers.main import (
    website_account
)


class WebsiteAccountProposal(website_account):

    @http.route(['/my/account'], type='http', auth='user', website=True)
    def details(self, redirect=None, **post):
        response = super(website_account, self).details(redirect, **post)
        proposal_overview = request.env['project.proposal'].search(
            [('owner_id', '=', request.uid)],
            order='published DESC, start_date DESC'
        )
        response.qcontext.update({
            'proposals': proposal_overview,
        })
        return response
