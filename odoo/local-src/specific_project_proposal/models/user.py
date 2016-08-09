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

    suggested_proposal_ids = fields.Many2many(
        compute='_get_suggested_proposals',
        comodel_name='project.proposal',
        string="Suggested proposals",
        help="Proposals that match with user expertises and industries."
             " (Blacklisted and own proposals are not part of this list)"
    )

    @api.depends('partner_id.category_id', 'partner_id.expertise_ids',
                 'proposal_blacklist_ids')
    def _get_suggested_proposals(self):
        """ Get list of suggestion of proposals

        Matching proposals based on expertises and industries.
        It doesn't includ self proposals and proposals marked as blacklisted
        by the user.
        """
        self.suggested_proposal_ids = self.env['project.proposal'].search(
            ['|', ('expertise_ids', 'in', self.partner_id.expertise_ids.ids),
                  ('industry_ids', 'in', self.partner_id.category_id.ids),
             ('id', 'not in', self.proposal_blacklist_ids.ids),
             ('owner_id', '!=', self.id),
             ]
        )
