# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def disable_old_login_template(ctx):
    # The template has been customized in the wrong way.
    # We are disabling it since theme_fluxdocs.layout_footer_copyright
    # is taking over it.
    # Since the original one has been customized TTW
    # xml inactivation is not take into account
    template = ctx.env.ref(
        'auth_signup.login', raise_if_not_found=0)
    if template:
        template.active = False


@anthem.log
def main(ctx):
    disable_old_login_template(ctx)
