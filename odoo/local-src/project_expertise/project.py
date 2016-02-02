# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class project(models.Model):
    _inherit = 'project.project'

    project_expertise_ids = fields.Many2many(
        'project_expertise.project_expertise',
        'project_project_expertise_ids_rel',
        'project_id',
        'project_expertise_id',
        string='Expertise')
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
