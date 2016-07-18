# -*- coding: utf-8 -*-
# © 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def create_membership_invoice(self):
        # memb_line_obj = self.env['membership.line']
        product_id = self.env['product.product'].search(
            [('default_code', '=', 'asso_2016')])

        datas = {'membership_product_id': product_id.id, 'amount': 100}

        if self.free_member is True:
            self.free_member = False

        inv = super(ResPartner, self).create_membership_invoice(
            product_id=product_id,
            datas=datas)

        return inv

    @api.multi
    def buttonBuyMembership(self):
        self.create_membership_invoice()
