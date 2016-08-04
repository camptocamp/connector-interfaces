# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from openerp import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    proposal_ids = fields.One2many(
        comodel_name='project.proposal',
        inverse_name='owner_id',
    )
