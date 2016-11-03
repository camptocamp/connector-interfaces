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
    }
    create_or_update(
        ctx, 'mail.template', 'auth_signup.set_password_email', values)





@anthem.log
def main(ctx):
    """ Main: creating demo data """
    change_signup_email(ctx)
