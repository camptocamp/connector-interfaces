# -*- coding: utf-8 -*-
# © 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, models, fields, exceptions, _


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
    is_associated = fields.Boolean(
        string='Is associated',
        compute='_compute_is_associated',
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
    def _compute_is_associated(self):
        for item in self:
            item.is_associated = item.flux_membership == 'asso'

    @api.multi
    def create_membership_invoice(self, product_id=None, datas=None):
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
        acc_inv_id = acc_inv_obj.browse(inv)
        acc_inv_id.signal_workflow('invoice_open')

        self.flux_membership = 'asso'
        return inv

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
