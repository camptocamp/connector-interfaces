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
    )

    @api.depends('partner_id.category_id', 'partner_id.expertise_ids',
                 'proposal_blacklist_ids')
    def _get_suggested_proposals(self):
        self.suggested_proposal_ids = self.env['project.proposal'].search(
            ['|', ('expertise_ids', 'in', self.partner_id.expertise_ids.ids),
                  ('industry_ids', 'in', self.partner_id.category_id.ids),
             ('id', 'not in', self.proposal_blacklist_ids.ids),
             ]
        )
