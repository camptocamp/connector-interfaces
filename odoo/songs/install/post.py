# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
import csv

from pkg_resources import resource_stream
from anthem.lyrics.records import create_or_update
from anthem.lyrics.records import add_xmlid

from ..common import req
from ..common import load_file_content


def create_or_update_email_template(ctx, xmlid, values):
    template = ctx.env.ref(xmlid, raise_if_not_found=0)

    # TODO: move email templates to qweb using
    # https://github.com/OCA/social/blob/9.0/email_template_qweb
    # HERE we are forced to delete existing templates
    # to make sure they get updated when needed

    # if template:
    #     template.write(values)
    # else:
    #     template = ctx.env['mail.template'].create(values)
    #     add_xmlid(template, xmlid)

    if template:
        template.unlink()
    template = ctx.env['mail.template'].create(values)
    add_xmlid(ctx, template, xmlid, noupdate=False)
    return template


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
    xmlid = 'specific_membership.set_password_email'
    # `anthem.lyrics.create_or_update`
    # will not update if existing and modified TTW :S
    create_or_update_email_template(ctx, xmlid, values)


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
    xmlid = 'specific_membership.reset_password_email'
    # `anthem.lyrics.create_or_update`
    # will not update if existing and modified TTW :S
    create_or_update_email_template(ctx, xmlid, values)


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
    xmlid = 'specific_membership.mail_membership_upgrade'
    # `anthem.lyrics.create_or_update`
    # will not update if existing and modified TTW :S
    create_or_update_email_template(ctx, xmlid, values)


@anthem.log
def override_default_notification_template(ctx):
    content = resource_stream(req, 'data/mail_default_template.html').read()
    # took from original one
    subject = """${object.subject or (object.record_name
    and 'Re: %s' % object.record_name)
    or (object.parent_id and object.parent_id.subject
    and 'Re: %s' % object.parent_id.subject)
    or (object.parent_id and object.parent_id.record_name
    and 'Re: %s' % object.parent_id.record_name)}"""
    values = {
        'body_html': content,
        'email_from': 'noreply@fluxdock.io',
        'name': 'Fluxdock Notification Email',
        'subject': subject,
        'model_id': ctx.env.ref('mail.model_mail_message').id,
        'auto_delete': True,
        'lang': """${object.mapped('partner_ids').lang
        if object.mapped('partner_ids') else object.user_id.lang}""",
    }
    xmlid = 'mail.mail_template_data_notification_email_default'
    create_or_update_email_template(ctx, xmlid, values)


@anthem.log
def add_matches_notification_template(ctx):
    content = resource_stream(req, 'data/mail_matches_template.html').read()
    # took from original one
    subject = """${object.subject or (object.record_name
    and 'Re: %s' % object.record_name)
    or (object.parent_id and object.parent_id.subject
    and 'Re: %s' % object.parent_id.subject)
    or (object.parent_id and object.parent_id.record_name
    and 'Re: %s' % object.parent_id.record_name)}"""
    values = {
        'body_html': content,
        'email_from': 'noreply@fluxdock.io',
        'name': 'Fluxdock Matches Notification Email',
        'subject': subject,
        'model_id': ctx.env.ref('mail.model_mail_message').id,
        'auto_delete': True,
        'lang': """${object.mapped('partner_ids').mapped('lang')[0]
         if object.mapped('partner_ids') else object.user_id.lang}""",
    }
    xmlid = 'specific_project_proposal.mail_matches_notification'
    create_or_update_email_template(ctx, xmlid, values)


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
    override_default_notification_template(ctx)
    add_matches_notification_template(ctx)
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
