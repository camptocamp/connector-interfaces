# coding=utf-8

import anthem
from ..common import (
    set_default_values,
)

DEFAULTS = (
    ('res.partner', 'notify_email', 'digest', ),
    ('res.partner', 'notify_frequency', 'weekly', ),
)
USER_TEMPLATE_DEFAULTS = (
    # set defaults from here as this template user
    # has `noupdate=1` hence we cannot force it via xml.
    ('auth_signup.default_template_user', 'notify_email', 'digest', ),
    ('auth_signup.default_template_user', 'notify_frequency', 'weekly', ),
)


@anthem.log
def default_values(ctx):
    company = ctx.env.ref('base.main_company')
    set_default_values(ctx, company, DEFAULTS)

    for xmlid, fname, value in USER_TEMPLATE_DEFAULTS:
        ctx.env.ref(xmlid).write({fname: value})
