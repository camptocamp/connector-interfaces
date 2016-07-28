# -*- coding: utf-8 -*-
# © 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, models, fields, exceptions
from openerp.tools.translate import _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    flux_membership = fields.Selection([
        ('free', 'Free Membership'),
        ('asso', 'Associate Membership')], default='free', required=True)

    @api.multi
    def create_membership_invoice(self, product_id=None, datas=None):
        prod_obj = self.env['product.product']
        acc_inv_obj = self.env['account.invoice']

        # product_id = product_id or datas.get('membership_product_id')
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
        acc_inv_id.invoice_validate()

        self.flux_membership = 'asso'
        return inv

    @api.multi
    def button_buy_membership(self):
        self.create_membership_invoice()

    @api.onchange('free_member')
    def change_flux_membership(self):
        self.flux_membership = 'free' if self.free_member else 'asso'
