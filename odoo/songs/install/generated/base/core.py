# -*- coding: utf-8 -*-
# Copyright  Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
# -- This file has been generated --

# pylint: disable=C,E

import anthem
from ....common import load_csv


@anthem.log
def load_res_lang(ctx):
    """ Import res.lang from csv """
    path = 'data/install/generated/base/core/res.lang.csv'
    model = ctx.env['res.lang'].with_context(tracking_disable=True)
    load_csv(ctx, path, model)


@anthem.log
def load_res_company(ctx):
    """ Import res.company from csv """
    path = 'data/install/generated/base/core/res.company.csv'
    model = ctx.env['res.company'].with_context(tracking_disable=True)
    header_exclude = ['parent_id/id']
    load_csv(ctx, path, model, header_exclude=header_exclude)
    if header_exclude:
        load_csv(ctx, path, model)


@anthem.log
def load_res_groups(ctx):
    """ Import res.groups from csv """
    path = 'data/install/generated/base/core/res.groups.csv'
    model = ctx.env['res.groups'].with_context(tracking_disable=True)
    header_exclude = ['implied_ids/id']
    load_csv(ctx, path, model, header_exclude=header_exclude)
    if header_exclude:
        load_csv(ctx, path, model)


@anthem.log
def load_ir_default(ctx):
    """ Import ir.default from csv """
    path = 'data/install/generated/base/core/ir.default.csv'
    model = ctx.env['ir.default'].with_context(
        tracking_disable=True, xmlid_value_reference=True)
    load_csv(ctx, path, model)


@anthem.log
def pre(ctx):
    load_res_lang(ctx)


@anthem.log
def post(ctx):
    load_res_company(ctx)
    load_res_groups(ctx)
    load_ir_default(ctx)
