##############################################################################
# For copyright and license notices, see __odoo__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class project(models.Model):
    _inherit = 'project.project'

    expertise_ids = fields.Many2many(
        'partner.project.expertise',
        'project_project_ids_rel',
        'project_id',
        'project_expertise_id',
        string='Expertise')
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
