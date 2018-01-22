# Copyright 2016 Goran Sunjka  (http://www.sunjka.de)
# Copyright 2017-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from odoo import models, fields


class ProjectPartnerExpertise(models.Model):

    _name = 'project.partner.expertise'
    _description = 'Partner and project expertise'

    name = fields.Char('Name', required=True, translate=True)
