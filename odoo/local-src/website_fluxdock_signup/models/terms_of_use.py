# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class TermsOfUse(osv.Model):
    _name = 'terms.of.use'
    _inherit = 'res.config.settings'
    _description = 'Terms of use'

    _columns = {
        'website_id': fields.many2one('website', string="website", required=True),
        'terms_of_use': fields.text('Terms of use', help='Terms of use', translate=True),
        'privacy_policy': fields.text('Privacy policy', help='Privacy policy', translate=True),
    }

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
        'website_id': lambda self,cr,uid,c: self.pool.get('website').search(cr, uid, [], context=c)[0],
    }
