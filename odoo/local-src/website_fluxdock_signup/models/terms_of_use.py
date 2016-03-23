# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp import fields, api, models

class TermsOfUse(models.Model):
    _name = "terms.of.use"
    _description = 'Terms of use'

    name = fields.Char(related='website_id.name', string='Name', type='char')
    website_id = fields.Many2one('website', string="Website", required=True)
    terms_of_use = fields.Text(string='Terms of use', help='Terms of use', translate=True)
    privacy_policy = fields.Text(string='Privacy policy', help='Privacy policy', translate=True)

    _defaults = {
        'website_id': lambda self,cr,uid,context: self.pool.get('website').search(cr, uid, [], context=context)[0]
    }
