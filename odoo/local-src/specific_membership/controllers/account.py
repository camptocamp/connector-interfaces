# -*- coding: utf-8 -*-
# © 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import http, _
from openerp.http import request
from openerp import SUPERUSER_ID
from openerp.addons.website_portal.controllers.main import website_account
from openerp.addons.base.ir.ir_mail_server import MailDeliveryException
import json
import base64
import logging
import datetime
_logger = logging.getLogger(__name__)
try:
    from validate_email import validate_email
except ImportError:
    _logger.debug("Cannot import `validate_email`.")


class WebsiteAccount(website_account):

    @http.route(['/my', '/my/home'], type='http', auth="public", website=True)
    def account(self, **kw):
        response = super(WebsiteAccount, self).account(**kw)
        response.qcontext.update(self._account_extra_qcontext())
        return response

    def _account_extra_qcontext(self):
        partner = request.env['res.users'].browse(request.uid).partner_id
        yesterday = (
            datetime.datetime.now() - datetime.timedelta(days=1)
        ).strftime('%Y-%m-%d')
        show_profile_progress = not partner.profile_completed or \
            (partner.profile_completed and not
                partner.profile_completed_date <= yesterday)
        return {
            'partner': partner,
            'show_profile_progress': show_profile_progress
        }

    @http.route(['/my/account'], type='http', auth="user", website=True)
    def details(self, redirect=None, **post):
        vals = {}
        user = request.env['res.users'].browse(request.uid)
        partner = user.partner_id
        if redirect:
            redirect = redirect
        else:
            redirect = ('/my/home')

        # handle this here since the call to super klass
        # saves the new email already
        if post and post.get('email'):
            vals['email_updated'] = self._handle_email_update(user, post)

        response = super(WebsiteAccount, self).details(redirect, **post)

        # FIXME: Workaround for problem with saving of fields website.
        # If required fields are not set, website will be taken out of
        # response dictionary in order to avoid server errors.
        if 'website' in response.qcontext:
            del response.qcontext['website']

        industry_ids = []
        expertise_ids = []

        if request.httprequest.method == 'POST':
            # form really submitted by user
            country_id = post['country_id']
            if country_id and country_id.isdigit():
                vals.update({'country_id': int(country_id)})
            if post['post_categories']:
                industry_ids = post['post_categories'].split(',')
                industry_ids = [int(rec_id) for rec_id in industry_ids]
                vals['category_id'] = [(6, None, industry_ids)]
            if post['post_expertises']:
                expertise_ids = post['post_expertises'].split(',')
                expertise_ids = [int(rec_id) for rec_id in expertise_ids]
                vals['expertise_ids'] = [(6, None, expertise_ids)]
            if post['uimage']:
                vals['image'] = base64.encodestring(post['uimage'].read())
            response.qcontext.update(vals)

            if 'error' not in response.qcontext:
                vals['website'] = post['website_url']

                # finally publish the partner
                if not partner.website_published:
                    vals['website_published'] = True

                # handle profile step upgrade
                partner.update_profile_state()
                partner.sudo().write(vals)

                if request.website:
                    msg = _('Profile details updated.')
                    request.website.add_status_message(msg)

        if industry_ids:
            Industry = request.env['res.partner.category']
            industries = Industry.browse(industry_ids)
        else:
            industries = partner.category_id
        industries = [dict(id=category.id, name=category.display_name)
                      for category in industries]
        industries = json.dumps(industries)

        if expertise_ids:
            Expertise = request.env['partner.project.expertise']
            expertises = Expertise.browse(expertise_ids)
        else:
            expertises = partner.expertise_ids
        expertises = json.dumps(expertises.read(['name']))

        response.qcontext.update(categories=industries, expertises=expertises)
        return response

    def _handle_email_update(self, user, post):
        """Validate email update and handle login update."""
        if user.email != post.get('email'):
            email = post['email']
            valid = validate_email(email)
            if email and valid and user.id != SUPERUSER_ID:
                exists = user.sudo().search_count(
                    ['|', ('login', '=', email), ('email', '=', email)]
                )
                # prevent email save and display friendly message
                post.pop('email')
                if exists and request.website:
                    title = _('Warning')
                    msg = _(
                        'Email address `%s` already taken. '
                        'Please check inside your company. '
                    ) % email
                    # NOTE: `add_status_message`
                    # is defined into `theme_fluxdocs` ATM
                    request.website.add_status_message(
                        msg, mtype='warning', mtitle=title)
                    return False
                try:
                    # update login on user
                    # this MUST happen BEFORE `reset_password` call
                    # otherwise it will not find the user to reset!
                    user.sudo().write(
                        {'login': email, 'email': email, }
                    )
                    # send reset password link to verify email
                    user.sudo().reset_password(email)
                    can_change = True
                except MailDeliveryException:
                    # do not update email / login
                    # if for any reason we cannot send email
                    can_change = False
                if can_change and request.website:
                    title = _('Important')
                    msg = _(
                        'Your login username has changed to: `%s`. '
                        'An email has been sent to verify it. '
                        'You will be asked to reset your password.'
                    ) % email
                    # NOTE: `add_status_message`
                    # is defined into `theme_fluxdocs` ATM
                    request.website.add_status_message(
                        msg, mtype='warning', mtitle=title)
                return True
        return False

    def details_form_validate(self, data):
        """ Overwrite checks """
        error = {}
        error_message = []

        # prevent stupid fail when appending only '?debug' to URL
        data.pop('debug', None)

        mandatory_fields = ["name", "street2", "zipcode", "city", "country_id",
                            "phone", "email"]
        optional_fields = ["state_id", "vat", "street"]
        additional_fields = ['uimage', 'website_url', 'twitter', 'facebook',
                             'skype', 'website_short_description',
                             'post_expertises', 'post_categories']

        missing = False
        # Validation
        for field_name in mandatory_fields:
            if not data.get(field_name):
                error[field_name] = 'missing'
                missing = True

        # error message for empty required fields
        if missing:
            error_message.append(_('Some required fields are empty.'))

        # email validation
        if data.get('email') and not validate_email(data.get('email')):
            error["email"] = 'error'
            error_message.append(
                _('Invalid Email! Please enter a valid email address.'))

        # vat validation
        if data.get("vat") and hasattr(request.env["res.partner"],
                                       "check_vat"):
            if request.website.company_id.vat_check_vies:
                # force full VIES online check
                check_func = request.env["res.partner"].vies_vat_check
            else:
                # quick and partial off-line checksum validation
                check_func = request.env["res.partner"].simple_vat_check
            vat_country, vat_number = request.env["res.partner"]._split_vat(
                data.get("vat"))
            if not check_func(vat_country, vat_number):  # simple_vat_check
                error["vat"] = 'error'

        valid_fields = mandatory_fields + optional_fields + additional_fields
        unknown = [
            k for k in data.iterkeys()
            if k not in valid_fields
        ]
        if unknown:
            error['common'] = 'Unknown field'
            error_message.append("Unknown field '%s'" % ','.join(unknown))

        return error, error_message

    @http.route(
        ['/my/get_expertises'],
        type='http',
        auth="public",
        methods=['GET'],
        website=True)
    def expertise_read(self, q='', l=25, **post):
        data = request.env['partner.project.expertise'].search_read(
            domain=[('name', '=ilike', (q or '') + "%")],
            fields=['id', 'name'],
            limit=int(l),
        )
        return json.dumps(data)

    @http.route(
        ['/my/get_categories'],
        type='http',
        auth="public",
        methods=['GET'],
        website=True)
    def categories_read(self, q='', l=25, **post):
        data = request.env['res.partner.category'].search_read(
            domain=[('name', '=ilike', (q or '') + "%")],
            fields=['id', 'display_name'],
            limit=int(l),
        )
        return json.dumps(data)

    @http.route(
        ['/my/profile_success'],
        type='http',
        auth='user',
        website=True)
    def profile_success(self, *args, **kw):
        return request.render('specific_membership.profile_success', {})
