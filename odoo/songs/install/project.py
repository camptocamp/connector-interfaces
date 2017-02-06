# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
# from anthem.lyrics.records import create_or_update
from anthem.lyrics.records import add_xmlid
# from ..common import load_csv


def get_xmlid(record):

    def cleanup_string(val):
        return val.replace('-', '_').replace(' ', '')

    val = record.name
    prefix = 'sc.proj_expertise_'
    if not val.startswith(prefix):
        val = prefix + val
    return cleanup_string(val).lower()


@anthem.log
def add_expertise_xmlids(ctx):
    """ Add xmlid to existing expertises """
    records = ctx.env['partner.project.expertise'].search([])
    for record in records:
        add_xmlid(
            ctx, record,
            'sc.project_expertise' + record.name,
            noupdate=True
        )


@anthem.log
def main(ctx):
    """ Configuring project """
    add_expertise_xmlids(ctx)
