# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import os
from pkg_resources import resource_stream
import anthem
from anthem.lyrics.loaders import load_csv_stream
from ..common import req


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
def configure_admin_user(ctx):
    """ configure admin user """
    companies = ctx.env['res.company'].search([])
    admin = ctx.env.ref('base.user_root')
    # assign all companies
    admin.write(
        {'company_ids': [(6, 0, companies.ids)]}
    )
    ctx.env.ref('base.group_multi_company').write(
        {'users': [(4, admin.id)]}
    )


@anthem.log
def import_users(ctx):
    """ Import users """
    content = resource_stream(req, 'data/install/res.users.csv')
    load_csv_stream(ctx, 'res.users', content, delimiter=',')


@anthem.log
def main(ctx):
    """ Configuring products """
    admin_user_password(ctx)
    configure_admin_user(ctx)
    import_users(ctx)
