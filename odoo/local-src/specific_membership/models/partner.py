# -*- coding: utf-8 -*-
# © 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'


    flux_membership = fields.Selection([
        ('free', 'Free Membership'),
        ('asso', 'Associate Membership')],default='free')

    @api.multi
    def create_membership_invoice(self, product_id=None, datas=None):
        # memb_line_obj = self.env['membership.line']
        product_id = product_id or self.env['product.product'].search([
            ('default_code', '=', 'associate')])

        acc_inv_obj = self.env['account.invoice']

        datas = {'membership_product_id': product_id.id, 'amount': 100}

        if self.free_member is True:
            self.free_member = False

        inv = super(ResPartner, self).create_membership_invoice(
            product_id=product_id,
            datas=datas)

        acc_inv_id = acc_inv_obj.browse(inv)
        acc_inv_id.invoice_validate()

        self.flux_membership = 'asso'
        return inv

    @api.multi
    def buttonBuyMembership(self):
        self.create_membership_invoice()
