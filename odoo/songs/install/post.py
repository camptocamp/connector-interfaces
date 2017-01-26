# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
import csv

from pkg_resources import resource_stream
from anthem.lyrics.records import create_or_update

from ..common import req
from ..common import load_file_content


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
        ctx, 'mail.template', 'specific_membership.set_password_email', values)


@anthem.log
def change_reset_pwd_email(ctx):
    """ Updating reset password email """
    content = resource_stream(req, 'data/mail_reset_password.html').read()
    values = {
        'name': 'Fluxdock Password Reset',
        'subject': 'Fluxdock password reset',
        'body_html': content,
        'email_from': 'noreply@fluxdock.io',
        'model_id': ctx.env.ref('base.model_res_users').id,
        'email_to': '${object.email|safe}',
        'lang': '${object.partner_id.lang}',
        'auto_delete': False,
    }
    create_or_update(
        ctx, 'mail.template',
        'specific_membership.reset_password_email', values)


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
def load_email_translations(ctx):
    """ Load email translations """
    # translation links original items with "res_id"
    # which is not a relation field but an integer.
    # So we cannot use an xmlid because it will fail like this:
    #
    # "'auth_signup.reset_password_email'
    #   does not seem to be an integer for field 'Record ID'"
    content = load_file_content('data/email.ir.translation.csv')
    for line in csv.DictReader(content, delimiter='|'):
        xmlid = line.pop('id')
        if not line['res_id']:
            continue
        # load HTML from file
        for key in ('src', 'source', 'value'):
            if line[key].startswith('path:'):
                line[key] = resource_stream(
                    req, line[key].split('path:')[-1]).read()
        # must fail if template not there
        template = ctx.env.ref(line['res_id'])
        line['res_id'] = template.id
        if template:
            # check untranslated
            to_translate = ctx.env['ir.translation'].search([
                ('module', '=', line['module']),
                ('res_id', '=', template.id),
                ('name', '=', line['name']),
                ('state', 'in', ('to_translate', False)),
            ])
            if to_translate:
                to_translate.unlink()
        # create or update here is not enough
        # if you delete the template from backend
        # you can get a stale entry for translation
        # so we must remove it 1st.
        existing = ctx.env.ref(xmlid, raise_if_not_found=0)
        if existing:
            existing.unlink()
        translation = create_or_update(
            ctx, 'ir.translation', xmlid, line)
        translation.write({
            # force state, since is not set to translated with values
            'state': 'translated'
        })


@anthem.log
def remove_useless_menuitems(ctx):
    """ Remove useless website menu items """
    xmlids = (
        'website_slides.website_menu_slides',
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
def update_emails(ctx):
    """ Update emails """
    change_signup_email(ctx)
    add_membership_upgrade_email(ctx)
    change_reset_pwd_email(ctx)
    load_email_translations(ctx)


@anthem.log
def setup_website_languages(ctx):
    """ Adding languages to website """
    website_langs = [ctx.env.ref('base.lang_en').id, ]
    for code in ('de_DE',):
        lang = ctx.env['res.lang'].search([('code', '=', code)])
        website_langs.append(lang.id)
    ws = ctx.env['website'].browse(1)
    ws.write(
        {'language_ids': [(6, 0, website_langs), ]})


@anthem.log
def enable_html_compression(ctx):
    """ Enable html compression """
    ws = ctx.env['website'].browse(1)
    ws.write({'compress_html': True})


@anthem.log
def main(ctx):
    """ Main: creating demo data """
    remove_useless_menuitems(ctx)
    update_emails(ctx)
    setup_website_languages(ctx)
    enable_html_compression(ctx)
