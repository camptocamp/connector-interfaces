# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
import os


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
def setup_url_params(ctx):
    """ Setup url params """
    # make pdf report generation happy
    # see https://github.com/odoo/odoo/issues/1105
    # TMP fix: we need to move this stuff to environment files
    # but currently you cannot use env vars in env files
    # because env vars are not loaded :(
    # PR for odoo project
    # https://github.com/camptocamp/docker-odoo-project/pull/20
    url = os.environ.get('DOMAIN_NAME', 'http://localhost:8069')
    ctx.env['ir.config_parameter'].set_param('web.base.url', url)
    ctx.env['ir.config_parameter'].set_param('web.base.url.freeze', 'True')
    ctx.env['ir.config_parameter'].set_param('report.url', url)


@anthem.log
def admin_user_password(ctx):
    if os.environ.get('RUNNING_ENV') in ('dev', ):
        ctx.log_line('RUNNING_ENV=dev => nothing to do here.')
        return
    if os.environ.get('RUNNING_ENV') in ('test', ):
        ctx.env.user.password_crypt = (
            '$pbkdf2-sha512$12000$sVYK4ZyzVioFYMyZU4pRag$BXgpuHm7B54rt6BMy6VCZ'
            'ydIIl0PGhH.dj986wQTaGw6dH3o5rDIK/SN5VUt.Om3HS4s9tj3pcCRQq1/.X07Kw'
        )
        ctx.log_line('Set admin user password.')


@anthem.log
def main(ctx):
    """ Main: creating demo data """
    setup_language(ctx)
    setup_website_signup(ctx)
    setup_url_params(ctx)
    admin_user_password(ctx)
