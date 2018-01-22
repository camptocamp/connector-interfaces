# Copyright 2016 Goran Sunjka  (http://www.sunjka.de)
# Copyright 2017-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    expertise_ids = fields.Many2many(
        comodel_name='project.partner.expertise',
        relation='res_project_partner_expertise_rel',
        column1='partner_id',
        column2='project_expertise_id',
        string='Expertises'
    )
