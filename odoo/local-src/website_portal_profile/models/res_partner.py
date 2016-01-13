# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# from openerp.osv import orm, fields, osv
from openerp import fields, models


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    werbeversprechen = fields.Char(string='Werbeversprechen')
    facebook = fields.Char(string='Facebook')
    twitter = fields.Char(string='Twitter')
    expertise = fields.Char(string='Expertise')
    agree_to_terms = fields.Boolean('Agree to unity terms', help='Agree to terms')
