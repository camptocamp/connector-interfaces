# Copyright 2016 Goran Sunjka  (http://www.sunjka.de)
# Copyright 2017-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from odoo import models, fields


class ProjectProject(models.Model):
    _inherit = 'project.project'

    expertise_ids = fields.Many2many(
        comodel_name='project.partner.expertise',
        relation='project_expertise_ids_rel',
        column1='project_id',
        column2='project_expertise_id',
        string='Expertise'
    )
