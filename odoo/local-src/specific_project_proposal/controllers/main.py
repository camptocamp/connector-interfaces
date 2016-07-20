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
        user = request.env['res.users'].browse(request.uid)
        response = super(website_account, self).details(redirect, **post)
        response.qcontext.update({
            # XXX limit number of proposals to have max 4 proposals
            'proposals': user.proposal_ids,
        })
        return response
