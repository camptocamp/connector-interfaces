# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from ..common import load_csv


@anthem.log
def load_users(ctx):
    model = ctx.env['res.users'].with_context({
        'no_reset_password': True,
        'tracking_disable': True,
    })
    load_csv(
        ctx, 'data/sample/res.users.csv',
        model, delimiter=',')

    # update partners
    users = ctx.env['res.users']
    users |= ctx.env.ref('__sample__.res_user_one')
    users |= ctx.env.ref('__sample__.res_user_two')
    users.mapped('partner_id').write({'website_published': True})
    ctx.env.ref(
        '__sample__.res_user_three').partner_id.website_published = False


@anthem.log
def main(ctx):
    """ Installing sample data """
    load_users(ctx)
