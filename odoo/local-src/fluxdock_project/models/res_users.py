# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    references_ids = fields.One2many(
        comodel_name='project.reference',
        inverse_name='create_uid'
    )
    proposal_ids = fields.One2many(
        comodel_name='project.proposal',
        inverse_name='create_uid',
    )
    proposal_blacklist_ids = fields.Many2many(
        comodel_name='project.proposal',
        string="Blacklisted proposals",
    )
    proposal_match_ids = fields.Many2many(
        compute='_get_proposal_matches',
        comodel_name='project.proposal',
        string="Suggested proposals",
        help="Proposals that match with user professions."
             " (Blacklisted and own proposals are not part of this list)"
    )

    def _proposal_search_domain(self):
        return [
            ('profession_ids', 'in', self.partner_id.profession_ids.ids),
            ('id', 'not in', self.proposal_blacklist_ids.ids),
            ('create_uid', '!=', self.id),
            # this should be handled by security rule
            # but let's be explicit :)
            ('website_published', '=', True)
        ]

    def _get_proposal_matches(self):
        """Get list of matching proposals by professions.

        Exclude self proposals and blacklisted proposals.
        """
        for rec in self:
            # Change environement to ensure to apply record rules
            # otherwise the search is done with admin
            prop_sudo = self.env['project.proposal'].sudo(rec)
            rec.proposal_match_ids = prop_sudo.search(
                rec._proposal_search_domain(),
                order='start_date DESC',
            )
