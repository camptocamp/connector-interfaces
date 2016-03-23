# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp import fields, api, models

class TermsOfUse(models.Model):
    _name = "terms.of.use"
    _description = 'Terms of use'

    name = fields.Char(string='Name', size=64, help='Terms of use name')
    website_id = fields.Many2one(string="Website", required=True)
    terms_of_use = fields.Text(string='Terms of use', help='Terms of use', translate=True)
    privacy_policy = fields.Text(string='Privacy policy', help='Privacy policy', translate=True)

    def on_change_website_id(self, cr, uid, ids, website_id, context=None):
        if not website_id:
            return {'value': {}}
        website_data = self.pool.get('website').read(cr, uid, [website_id], [], context=context)[0]
        values = {'website_name': website_data['name']}
        for fname, v in website_data.items():
            if fname in self._columns:
                values[fname] = v[0] if v and self._columns[fname]._type == 'many2one' else v
        return {'value' : values}

    _defaults = {
        'website_id': lambda self,cr,uid,context: self.pool.get('website').search(cr, uid, [], context=context)[0]
    }
