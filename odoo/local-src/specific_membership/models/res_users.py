# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
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
