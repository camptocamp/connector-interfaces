# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from openerp import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    proposal_ids = fields.One2many(
        comodel_name='project.proposal',
        inverse_name='owner_id',
    )

    proposal_blacklist_ids = fields.Many2many(
        comodel_name='project.proposal',
        string="Blacklisted proposals",
    )

    proposal_match_ids = fields.Many2many(
        compute='_get_proposal_matches',
        comodel_name='project.proposal',
        string="Suggested proposals",
        help="Proposals that match with user expertises and industries."
             " (Blacklisted and own proposals are not part of this list)"
    )

    @api.depends('partner_id.category_id', 'partner_id.expertise_ids',
                 'proposal_blacklist_ids')
    def _get_proposal_matches(self):
        """ Get list of matches of proposals

        Matching proposals based on expertises and industries.
        It doesn't includ self proposals and proposals marked as blacklisted
        by the user.
        """
        for rec in self:
            partner = rec.partner_id
            rec.proposal_match_ids = self.env['project.proposal'].search(
                ['|', ('expertise_ids', 'in', partner.expertise_ids.ids),
                      ('industry_ids', 'in', partner.category_id.ids),
                 ('id', 'not in', rec.proposal_blacklist_ids.ids),
                 ('owner_id', '!=', rec.id),
                 ],
                order='website_published DESC, start_date DESC',
            )
