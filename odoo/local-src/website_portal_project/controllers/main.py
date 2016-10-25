# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import http
from openerp import SUPERUSER_ID
from openerp.addons.specific_membership.controllers.account\
    import WebsiteAccount as WebsiteAccountController
from openerp.http import request


class WebsiteAccount(WebsiteAccountController):

    def _account_extra_qcontext(self):
        _super = super(WebsiteAccount, self)
        res = _super._account_extra_qcontext()
        projects = request.env['project.project'].search([])
        res.update({'projects': projects})
        return res


class WebsitePortalProject(http.Controller):

    @http.route(
        ['/my/projects/<int:project_id>'],
        type='http',
        auth="user",
        website=True)
    def projects_followup(self, project_id=None):
        project = request.env['project.project'].browse(project_id)
        return request.website.render(
            "website_portal_project.projects_followup", {
                'project': project})

    @http.route(['/my/projects/new'], type='http', auth="user", website=True)
    def projects_new(self, project_id=None):
        project = request.env['project.project'].browse(project_id)
        return request.website.render(
            "website_portal_project.projects_new", {
                'project': project})


class WebsiteProjectProposal(http.Controller):

    @http.route(['/market'], type='http', auth="public", website=True)
    def proposals(self):
        proposal_obj = request.registry['project.proposal']
        proposals = proposal_obj.browse(
            request.cr,
            SUPERUSER_ID,
            request.context)
        values = {
            'proposals': proposals
        }
        return request.website.render("website_portal_project.market", values)
