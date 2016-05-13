#!/usr/bin/env python
# -*- coding: utf-8 -*-

from openerp import _, api, models, fields

class ProjectReferences(models.Model):
    """Project References"""
    _name = "project.references"

    name = fields.Char('Project name', size=256, help='Please enter name of the project')
