# -*- coding: utf-8 -*-
# © 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, models, fields, exceptions, _
from openerp.addons.website.models.website import slug

import logging

_logger = logging.getLogger(__file__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    flux_membership = fields.Selection(
        string='Flux membership',
        selection=[
            ('free', 'Free Membership'),
            ('asso', 'Associate Membership')
        ],
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
    @api.depends('profile_state')
    def _compute_profile_completed(self):
        for item in self:
            item.profile_completed = item.profile_state == 'step-3'

    @api.multi
    def update_profile_state(self):
        for item in self:
            if item.profile_state == 'step-1':
                item.profile_state = 'step-2'
            elif item.profile_state == 'step-2':
                item.profile_state = 'step-3'
                item.profile_completed_date = fields.Date.today()

    def _select_profile_state(self):
        options = [
            ('step-1', 'Signup'),
            ('step-2', 'Update details'),
            ('step-3', 'Add references'),
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
