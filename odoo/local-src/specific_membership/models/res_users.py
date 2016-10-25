# -*- coding: utf-8 -*-
# © 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models
from openerp import _


class ResUsers(models.Model):
    _inherit = 'res.users'

    _sql_constraints = [
        (
            'login',
            'UNIQUE (login)',
            _('A user with this login already exists !')
        )
    ]
