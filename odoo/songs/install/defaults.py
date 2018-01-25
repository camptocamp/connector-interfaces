# import anthem
# from ..common import (
#     set_default_values,
# )

# TODO: move this stuff to DJ tool export

# DEFAULTS = (
#     ('res.users', 'digest_mode', True, ),
#     ('res.users', 'digest_frequency', 'weekly', ),
# )
# USER_TEMPLATE_DEFAULTS = (
#     # set defaults from here as this template user
#     # has `noupdate=1` hence we cannot force it via xml.
#     ('auth_signup.default_template_user', 'digest_mode', True, ),
#     ('auth_signup.default_template_user', 'digest_frequency', 'weekly', ),
# )
#
#
# @anthem.log
# def default_values(ctx):
#     company = ctx.env.ref('base.main_company')
#     set_default_values(ctx, company, DEFAULTS)
#
#     for xmlid, fname, value in USER_TEMPLATE_DEFAULTS:
#         ctx.env.ref(xmlid).write({fname: value})
#
#
# @anthem.log
# def main(ctx):
#     default_values(ctx)
