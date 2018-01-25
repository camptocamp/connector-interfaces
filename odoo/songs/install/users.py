# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import os
import anthem


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
    # enable multicompany
    ctx.env.ref('base.group_multi_company').write(
        {'users': [(4, admin.id)]}
    )
    # enable tech features
    ctx.env.ref('base.group_no_one').write(
        {'users': [(4, admin.id)]}
    )


@anthem.log
def main(ctx):
    admin_user_password(ctx)
    configure_admin_user(ctx)
