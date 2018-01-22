##############################################################################
# For copyright and license notices, see __odoo__.py file in module root
# directory
##############################################################################
from odoo.osv import fields, osv


class res_partner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
        'expertise_ids': fields.many2many(
            'partner.project.expertise',
            'res_partner_rel',
            'partner_id',
            'project_expertise_id',
            'Expertise', help='Expertise'),
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
