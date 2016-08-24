# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp.osv import fields, osv


class res_partner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
        'expertise_ids': fields.many2many(
            'partner.project.expertise',
            'res_partner_rel',
            'partner_id',
            'partner_project_expertise_id',
            'Expertise', help='Expertise'),
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
