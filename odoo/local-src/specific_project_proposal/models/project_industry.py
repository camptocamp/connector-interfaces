# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from openerp import fields, models

class ProjectIndustry(models.Model):

    """Type of industry for projects"""

    _name = 'project.industry'
    _description = "Industry"

    name = fields.Char(required=True)
    description = fields.Text()
