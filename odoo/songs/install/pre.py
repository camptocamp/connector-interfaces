# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def setup_language(ctx):
    """ Installing language and configuring locale formatting """
    for code in ('de_DE',):
        ctx.env['base.language.install'].create({'lang': code}).lang_install()
    ctx.env['res.lang'].search([]).write({
        'grouping': [3, 0],
        'date_format': '%d/%m/%Y',
    })


@anthem.log
def setup_website_signup(ctx):
    """ Setting up system parameters to allow signup """
    ctx.env['ir.config_parameter'].set_param(
        'auth_signup.reset_password', True)
    ctx.env['ir.config_parameter'].set_param(
        'auth_signup.allow_uninvited', True)


@anthem.log
def main(ctx):
    """ Main: creating demo data """
    setup_language(ctx)
    setup_website_signup(ctx)
