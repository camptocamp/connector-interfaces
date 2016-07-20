#!/usr/bin/env python
# -*- coding: utf-8 -*-

from openerp import _, api, models, fields

class ProjectProposal(models.Model):
    """Project Proposals"""
    _name = "project.proposal"

    name = fields.Char('Project name', size=256, help='Please enter name of the project')
    description = fields.Char('Description', size=256, help='Please enter a description')
    publish_date = fields.Date('Published at', help='Date when project was published')
    start_date = fields.Date('Start date', help='Start date')
    end_date = fields.Date('End date', help='End date')
    project_owner = fields.Char('Project owner', size=64, help='Owner')
    expertise = fields.Char('Expertise', size=64, help='Expertise')
    status = fields.Char('Project status', size=64, help='Status')
    attachments = fields.Char('Attachments', size=64, help='Please add attachments')
