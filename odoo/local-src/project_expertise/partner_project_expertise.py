##############################################################################
# For copyright and license notices, see __odoo__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class PartnerProjectExpertise(models.Model):

    _name = 'partner.project.expertise'
    _description = 'Partner and project expertise'

    name = fields.Char('Name', required=True, translate=True)
    partner_id = fields.Many2one(
        'res.partner',
        'Partner',
        help='Enter Partner Name')
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
