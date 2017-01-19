# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
import os


@anthem.log
def setup_language(ctx):
    """ Installing language and configuring locale formatting """
    website_langs = [ctx.env.ref('base.lang_en').id, ]
    for code in ('de_DE',):
        ctx.env['base.language.install'].create({'lang': code}).lang_install()
        lang = ctx.env['res.lang'].search([('code', '=', code)])
        website_langs.append(lang.id)
    ctx.env['res.lang'].search([]).write({
        'grouping': [3, 0],
        'date_format': '%d/%m/%Y',
    })
    ws = ctx.env['website'].browse(1)
    ws.write(
        {'language_ids': [(6, 0, website_langs), ]})


@anthem.log
def setup_website_signup(ctx):
    """ Setting up system parameters to allow signup """
    ctx.env['ir.config_parameter'].set_param(
        'auth_signup.reset_password', True)
    ctx.env['ir.config_parameter'].set_param(
        'auth_signup.allow_uninvited', True)


@anthem.log
def setup_url_params(ctx):
    """ Setup url params """
    # make pdf report generation happy
    # see https://github.com/odoo/odoo/issues/1105
    # TMP fix: we need to move this stuff to environment files
    # PR for odoo project
    # https://github.com/camptocamp/docker-odoo-project/pull/20
    url = os.environ.get('DOMAIN_NAME', 'http://localhost:8069')
    ctx.env['ir.config_parameter'].set_param('web.base.url', url)
    ctx.env['ir.config_parameter'].set_param('web.base.url.freeze', 'True')
    ctx.env['ir.config_parameter'].set_param('report.url', url)


@anthem.log
def main(ctx):
    """ Main: creating demo data """
    setup_language(ctx)
    setup_website_signup(ctx)
    setup_url_params(ctx)
