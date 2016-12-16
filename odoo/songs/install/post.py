# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem

from pkg_resources import resource_stream
from anthem.lyrics.records import create_or_update

from ..common import req


@anthem.log
def change_signup_email(ctx):
    """ Updating signup email """
    # The goal of this method is to override the signup email wich has a
    # noupdate. Original template is as sample in
    # 'specific_membership/data/signup_data.xml'
    content = resource_stream(req, 'data/mail_signup.html').read()
    values = {
        'name': 'Fluxdock Signup',
        'subject': 'Fluxdock account confirmation',
        'body_html': content,
        'email_from': 'noreply@fluxdock.io',
        'model_id': ctx.env.ref('base.model_res_users').id,
        'email_to': '${object.email|safe}',
        'lang': '${object.partner_id.lang}',
        'auto_delete': False,
    }
    create_or_update(
        ctx, 'mail.template', 'auth_signup.set_password_email', values)


@anthem.log
def add_membership_upgrade_email(ctx):
    """ Add membership upgrade email """
    content = resource_stream(req, 'data/mail_membership_upgrade.html').read()
    values = {
        'name': 'Fluxdock membership upgrade',
        'subject': 'Fluxdock membership upgrade confirmed',
        'body_html': content,
        'email_from': 'noreply@fluxdock.io',
        'model_id': ctx.env.ref('account.model_account_invoice').id,
        'partner_to': '${object.partner_id.id}',
        'lang': '${object.partner_id.lang}',
        'report_template': ctx.env.ref('account.account_invoices').id,
        'report_name': (
            "Invoice_${(object.number or '')"
            ".replace('/','_')}_${object.state == 'draft' and 'draft' or ''}"
        ),
        'auto_delete': False,
    }
    create_or_update(
        ctx, 'mail.template',
        'specific_membership.mail_membership_upgrade', values)


@anthem.log
def remove_useless_menuitems(ctx):
    """ Remove useless website menu items """
    xmlids = (
        'website_slades.website_menu_slides',
        'website_blog.menu_news',
        'website_sale.menu_shop',
        'website.menu_contactus',
    )
    ids = []
    for xmlid in xmlids:
        item = ctx.env.ref(xmlid, raise_if_not_found=False)
        if item:
            ids.append(item.id)
    if ids:
        ctx.env['website.menu'].browse(ids).unlink()


@anthem.log
def main(ctx):
    """ Main: creating demo data """
    change_signup_email(ctx)
    add_membership_upgrade_email(ctx)
    remove_useless_menuitems(ctx)
