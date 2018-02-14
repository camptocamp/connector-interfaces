# -*- coding: utf-8 -*-
# Copyright  Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
# -- This file has been generated --

# pylint: disable=C,E

import anthem
from ....common import load_csv


@anthem.log
def load_website(ctx):
    """ Import website from csv """
    path = 'data/install/generated/base/website/website.csv'
    model = ctx.env['website'].with_context(tracking_disable=True)
    load_csv(ctx, path, model)


@anthem.log
def load_website_de_DE(ctx):
    """ Import website from csv """
    path = 'data/install/generated/base/website/website.de_DE.csv'
    model = ctx.env['website'].with_context(
        lang='de_DE', tracking_disable=True)
    load_csv(ctx, path, model)


@anthem.log
def load_website_menu(ctx):
    """ Import website.menu from csv """
    path = 'data/install/generated/base/website/website.menu.csv'
    model = ctx.env['website.menu'].with_context(tracking_disable=True)
    header_exclude = ['parent_id/id']
    load_csv(ctx, path, model, header_exclude=header_exclude)
    if header_exclude:
        load_csv(ctx, path, model)


@anthem.log
def load_website_menu_de_DE(ctx):
    """ Import website.menu from csv """
    path = 'data/install/generated/base/website/website.menu.de_DE.csv'
    model = ctx.env['website.menu'].with_context(
        lang='de_DE', tracking_disable=True)
    load_csv(ctx, path, model)


@anthem.log
def load_ir_config_parameter(ctx):
    """ Import ir.config_parameter from csv """
    path = 'data/install/generated/base/website/ir.config_parameter.csv'
    model = ctx.env['ir.config_parameter'].with_context(tracking_disable=True)
    load_csv(ctx, path, model)


@anthem.log
def post(ctx):
    load_website(ctx)
    load_website_de_DE(ctx)
    load_website_menu(ctx)
    load_website_menu_de_DE(ctx)
    load_ir_config_parameter(ctx)
