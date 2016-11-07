# -*- coding: utf-8 -*-
# © 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models
from openerp import fields
from openerp import _


class ResUsers(models.Model):
    _inherit = 'res.users'

    is_associated = fields.Boolean(
        string='Is associated',
        related='partner_id.is_associated',
        readonly=True,
    )

    _sql_constraints = [
        (
            'login',
            'UNIQUE (login)',
            _('A user with this login already exists !')
        )
    ]
