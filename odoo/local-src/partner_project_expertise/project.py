# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class project(models.Model):
    _inherit = 'project.project'

    expertise_ids = fields.Many2many(
        'partner_project_expertise.expertise',
        'partner_project_expertise_expertise_ids_rel',
        'project_id',
        'partner_project_expertise_id',
        string='Expertise')
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
