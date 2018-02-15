# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from ..common import load_csv


# TODO: review this when we introduce the 2 profiles company/user
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
    free_member = ctx.env.ref('__sample__.res_user_freemember')
    asso_member = ctx.env.ref('__sample__.res_user_associatemember')
    free_member.partner_id.free_member = True
    free_member.partner_id.website_published = True
    asso_member.partner_id.free_member = True
    asso_member.partner_id.website_published = True
    # asso_member.partner_id.create_membership_invoice(email=False)


@anthem.log
def main(ctx):
    """ Installing sample data """
    load_users(ctx)
