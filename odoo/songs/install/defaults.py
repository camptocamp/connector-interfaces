# coding=utf-8

import anthem
from ..common import (
    set_default_values,
)

DEFAULTS = (
    ('res.partner', 'notify_email', 'digest', ),
    ('res.partner', 'notify_frequency', 'weekly', ),
)


@anthem.log
def default_values(ctx):
    company = ctx.env.ref('base.main_company')
    set_default_values(ctx, company, DEFAULTS)
