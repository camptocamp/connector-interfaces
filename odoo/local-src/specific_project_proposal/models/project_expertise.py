# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from openerp import fields, models

class ProjectExpertise(models.Model):

    """Expertise for projects"""

    _name = 'project.expertise'
    _description = "Expertise"

    name = fields.Char(required=True)
    description = fields.Text()
