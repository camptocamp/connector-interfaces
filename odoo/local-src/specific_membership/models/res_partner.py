# -*- coding: utf-8 -*-
# © 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import openerp
from openerp import api, models, fields, exceptions, _
from openerp.addons.website.models.website import slug

import logging
import threading

_logger = logging.getLogger(__file__)

FLUX_MEMBERSHIP_OPTIONS = [
    ('free', _('Free Membership')),
    ('asso', _('Associate Membership')),
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
        'website.published.mixin',
    ]

    flux_membership = fields.Selection(
        string='Flux membership',
        selection=FLUX_MEMBERSHIP_OPTIONS,
        default='free',
        compute='_compute_flux_membership',
        required=True
    )
    is_associate = fields.Boolean(
        string='Is associate member',
        compute='_compute_is_associate',
        readonly=True,
    )
    is_free = fields.Boolean(
        string='Is free member',
        compute='_compute_is_free',
        readonly=True,
    )
    facebook = fields.Char(string='Facebook')
    twitter = fields.Char(string='Twitter')
    skype = fields.Char(string='Skype')
    # TODO: do we need this field? expertise_ids is a relation field.
    expertise = fields.Char(string='Expertise')
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

    @api.multi
    @api.depends('image')
    def _compute_image_url(self):
        ws_model = self.env['website']
        for item in self:
            image_url = '/theme_fluxdocs/static/img/member-placeholder.png'
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

    @api.multi
    @api.depends('membership_state')
    def _compute_flux_membership(self):
        for item in self:
            if (item.membership_state in ['paid', 'invoiced']):
                item.flux_membership = 'asso'
            else:
                item.flux_membership = 'free'

    @property
    def flux_membership_display(self):
        opts = dict(self.fields_get(
            allfields=['flux_membership'])['flux_membership']['selection'])
        return opts[self.flux_membership]

    @api.multi
    @api.depends('flux_membership')
    def _compute_is_associate(self):
        for item in self:
            item.is_associate = item.flux_membership == 'asso'

    @api.multi
    @api.depends('flux_membership')
    def _compute_is_free(self):
        for item in self:
            item.is_free = item.flux_membership == 'free'

    # CMS stuff
    cms_search_url = '/members'

    @api.multi
    def _compute_cms_edit_url(self):
        for item in self:
            item.cms_edit_url = '/my/account'

    @api.model
    def is_owner(self, uid):
        res = super(ResPartner, self).is_owner(uid)
        return res or self.user_id.id == uid

    @api.multi
    def create_membership_invoice(
            self, product_id=None, datas=None, email=True):
        """Override to update add fluxdock  goodies.

        Goodies:
        * update fluxdock status
        * generate invoice
        * send notifcation to partner w/ invoice attached
        """
        # `datas` is so wrong, yes,
        # but it's the original method's signature from membership module
        self.ensure_one()
        prod_obj = self.env['product.product']
        acc_inv_obj = self.env['account.invoice']
        if datas is None:
            datas = {}

        product_id = product_id or datas.get('membership_product_id')
        product = prod_obj.browse(product_id) or prod_obj.search(
            [('default_code', '=', 'associate')])
        if not product:
            raise exceptions.Warning(
                _('There is no associate default product'))

        datas = {'membership_product_id': product.id,
                 'amount': product.list_price}

        if self.free_member is True:
            self.free_member = False

        inv = super(ResPartner, self).create_membership_invoice(
            product_id=product,
            datas=datas)
        inv = acc_inv_obj.browse(inv)
        inv.signal_workflow('invoice_open')

        self.flux_membership = 'asso'

        if email:
            # handy flag for disable this (tests i.e.)
            template = self.env.ref(
                'specific_membership.mail_membership_upgrade')

            if template:
                template.send_mail(inv.id)
            else:
                _logger.warning(
                    "No email template found for "
                    "`specific_membership.mail_membership_upgrade`")

        # make original action happy and returns list of ids
        return inv.ids

    @api.multi
    def button_buy_membership(self):
        self.create_membership_invoice()

    @api.model
    def check_membership_payment(self):
        partners = self.search(
            [('membership_state', '=', 'invoiced')])
        acc_inv_obj = self.env['account.invoice']
        today = fields.Date.today()

        part_to_update = self.env['res.partner']

        for partner in partners:
            acc_inv = acc_inv_obj.search_count(
                [('partner_id', '=', partner.id),
                 ('date_due', '<', today),
                 ('state', '=', 'open')])
            if acc_inv:
                part_to_update |= partner

        part_to_update.write({'flux_membership': 'free'})

    @api.multi
    def _website_url(self, field_name, arg):
        res = {}
        for item in self:
            res[item.id] = "/members/%s" % slug(item)
        return res

    @api.model
    def _get_default_image(self, is_company, colorize=False):
        """Override to change default partner avatar."""
        if getattr(threading.currentThread(), 'testing', False) \
                or self.env.context.get('install_mode'):
            return False

        if self.env.context.get('partner_type') == 'delivery':
            img_path = openerp.modules.get_module_resource(
                'base', 'static/src/img', 'truck.png')
        elif self.env.context.get('partner_type') == 'invoice':
            img_path = openerp.modules.get_module_resource(
                'base', 'static/src/img', 'money.png')
        else:
            if is_company:
                img_path = openerp.modules.get_module_resource(
                    'base', 'static/src/img', 'company_image.png')
            else:
                img_path = openerp.modules.get_module_resource(
                    'theme_fluxdocs', 'static/img', 'member-placeholder.png')
        with open(img_path, 'rb') as f:
            image = f.read()

        return openerp.tools.image_resize_image_big(image.encode('base64'))

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
