# Copyright 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields, tools, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.modules import get_module_resource

import logging
import threading
import base64

_logger = logging.getLogger(__name__)

FLUX_MEMBERSHIP_OPTIONS = [
    ('free', _('Free Membership')),
]


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = [
        'res.partner',
        # `website.published.mixin` extension
        # from cms_form.models.website_mixin (like cms_edit_url field)
        # are not propagated to partner model.
        # Other features like `website_published` from std mixin are.
        # This is due to a bug in v8/9 whereas some inheritance on res.partner
        # model are broken at some point.
        # https://github.com/odoo/odoo/issues/9084#issuecomment-148373268
        # TODO: v11 should fix this -> check!
        'website.published.mixin',
    ]

    flux_membership = fields.Selection(
        string='Flux membership',
        selection=FLUX_MEMBERSHIP_OPTIONS,
        default='free',
        compute='_compute_flux_membership',
        required=True
    )
    # TODO: TMP field to fixup membership module removal
    # we some features like RR relying on this
    membership_state = fields.Char(default='free')
    is_free = fields.Boolean(
        string='Is free member',
        compute='_compute_is_free',
        readonly=True,
    )
    facebook = fields.Char(string='Facebook')
    twitter = fields.Char(string='Twitter')
    skype = fields.Char(string='Skype')
    agree_to_terms = fields.Boolean(
        'Agree to unity terms',
        help='Agree to terms'
    )
    profile_state = fields.Selection(
        string='Profile state',
        selection='_select_profile_state',
        required=True,
        default='step-1',
    )
    profile_completed = fields.Boolean(
        string='Profile completed',
        compute='_compute_profile_completed',
        readonly=True,
    )
    profile_completed_date = fields.Date(
        string='Profile completed date',
    )
    # TODO: v11 removed this field. Adding it to make detail view work
    fax = fields.Char(string='Fax')

    @api.multi
    @api.depends('image')
    def _compute_image_url(self):
        ws_model = self.env['website']
        for item in self:
            image_url = '/fluxdock_theme/static/img/member-placeholder.png'
            if item.image:
                image_url = ws_model.image_url(item, 'image')
            item.image_url = image_url

    @api.multi
    @api.depends('profile_state')
    def _compute_profile_completed(self):
        for item in self:
            item.profile_completed = \
                item.profile_state == self.PROFILE_STATE_LAST
            item.profile_completed_date = \
                item.profile_completed and fields.Date.today()

    PROFILE_STATE_LAST = 'step-3'

    @api.multi
    def update_profile_state(self, step=0, force_back=False):
        for item in self:
            state = ''
            if step:
                state = 'step-{}'.format(step)
            else:
                # just the next one
                if item.profile_state == 'step-1':
                    state = 'step-2'
                elif item.profile_state == 'step-2':
                    state = 'step-3'
            if not state or state < item.profile_state and not force_back:
                # you must explicitely force to get back to prev state
                continue
            item.profile_state = state

    def _select_profile_state(self):
        options = [
            ('step-1', 'S1 - Signup'),
            ('step-2', 'S2 - Update details'),
            ('step-3', 'S3 - Add references'),
        ]
        return options

    # TODO: cleanup membeship stuff
    # all the methods from here to the bottom must be reviewed

    @property
    def flux_membership_display(self):
        opts = dict(self.fields_get(
            ['flux_membership'])['flux_membership']['selection'])
        return opts.get(self.flux_membership, 'FIXME')

    @api.multi
    @api.depends('flux_membership')
    def _compute_is_free(self):
        for item in self:
            item.is_free = item.flux_membership == 'free'

    # CMS stuff
    cms_search_url = '/dock/partners'

    @api.multi
    def _compute_cms_edit_url(self):
        for item in self:
            item.cms_edit_url = '/my/account'

    @api.multi
    def _compute_website_url(self):
        for partner in self:
            partner.website_url = self.cms_search_url + '/' + slug(partner)

    @api.model
    def _get_default_image(self, partner_type, is_company, parent_id):
        """Bare copy/paste of original code: change default avatar only."""
        if (getattr(threading.currentThread(), 'testing', False) or
                self._context.get('install_mode')):
            return False

        colorize, img_path, image = False, False, False

        if partner_type in ['other'] and parent_id:
            parent_image = self.browse(parent_id).image
            image = parent_image and base64.b64decode(parent_image) or None

        if not image and partner_type == 'invoice':
            img_path = get_module_resource(
                'base', 'static/src/img', 'money.png')
        elif not image and partner_type == 'delivery':
            img_path = get_module_resource(
                'base', 'static/src/img', 'truck.png')
        elif not image and is_company:
            img_path = get_module_resource(
                'base', 'static/src/img', 'company_image.png')
        elif not image:
            img_path = get_module_resource(
                'fluxdock_theme', 'static/img', 'member-placeholder.png')
            colorize = True

        if img_path:
            with open(img_path, 'rb') as f:
                image = f.read()
        if image and colorize:
            try:
                image = tools.image_colorize(image)
            except ValueError as err:
                # PIL/Image.py", line 1344, in paste
                # self.im.paste(im, box, mask.im)
                # ValueError: bad transparency mask
                _logger.warn('_get_default_image ' + str(err))
                pass
        try:
            return tools.image_resize_image_big(base64.b64encode(image))
        except ValueError as err:
            # PIL/Image.py", line 1344, in paste
            # self.im.paste(im, box, mask.im)
            # ValueError: bad transparency mask
            _logger.warn('_get_default_image ' + str(err))
            return None

    @api.multi
    def redirect_after_publish(self):
        self.ensure_one()
        if self.website_published:
            return True

    @api.multi
    def do_after_publish(self):
        self.ensure_one()
        if self.website_published:
            # handle profile step upgrade
            self.sudo().update_profile_state(step=2)

    def get_membership_cost(self):
        product = self.env['product.product'].sudo().search([
            ('default_code', '=', 'associate')])
        total_price = product.list_price
        tax_amount = 0
        if product.taxes_id:
            tax_amount = product.list_price * (
                product.taxes_id[0].amount / 100)
            total_price += tax_amount
        return {
            'product': product,
            'product_price': product.list_price,
            'total_price': total_price,
            'tax_amount': tax_amount,
        }
