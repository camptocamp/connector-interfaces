# -*- coding: utf-8 -*-
# Copyright  Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
# -- This file has been generated --

# pylint: disable=C,E

import anthem
from ....common import load_csv


@anthem.log
def load_res_users(ctx):
    """ Import res.users from csv """
    path = 'data/sample/generated/custom/fluxdock/res.users.csv'
    model = ctx.env['res.users'].with_context(
        no_reset_password=True, tracking_disable=True)
    load_csv(ctx, path, model)


@anthem.log
def load_project_partner_profession(ctx):
    """ Import project.partner.profession from csv """
    path = ('data/sample/generated/custom/'
            'fluxdock/project.partner.profession.csv')
    model = ctx.env['project.partner.profession'].with_context(
        tracking_disable=True)
    load_csv(ctx, path, model)


@anthem.log
def load_project_proposal(ctx):
    """ Import project.proposal from csv """
    path = 'data/sample/generated/custom/fluxdock/project.proposal.csv'
    model = ctx.env['project.proposal'].with_context(tracking_disable=True)
    load_csv(ctx, path, model)


@anthem.log
def load_project_reference(ctx):
    """ Import project.reference from csv """
    path = 'data/sample/generated/custom/fluxdock/project.reference.csv'
    model = ctx.env['project.reference'].with_context(tracking_disable=True)
    load_csv(ctx, path, model)


@anthem.log
def post(ctx):
    load_res_users(ctx)
    load_project_partner_profession(ctx)
    load_project_proposal(ctx)
    load_project_reference(ctx)
