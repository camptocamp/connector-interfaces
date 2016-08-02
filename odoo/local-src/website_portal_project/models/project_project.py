# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import models, fields


class ProjectProject(models.Model):
    _name = "project.project"
    _inherit = ['project.project']

    referenz_titel = fields.Char('Referenzprojekt Titel', size=64)
    zeitpunkt_implementierung = fields.Date(
        'Zeitpunkt der Implementierung')
    ort = fields.Char('Ort', size=64, help='Ort')
    referenz_bild = fields.Char(
        'Referenzprojekt Bild',
        size=64,
        help='Referenzprojekt Bild')
    referenz_kurzbeschreibung = fields.Char(
        'Referenzprojekt Kurzbeschreibung',
        size=64,
        help='Referenzprojekt Kurzbeschreibung')
    video_url = fields.Char('Video URL', size=64, help='Video URL')
    referenz_partner = fields.Char(
        'Referenzprojekt Partner',
        size=64,
        help='Referenzprojekt Partner')
