# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import openerp.tests.common as test_common


class TestMembership(test_common.TransactionCase):

    def setUp(self):
        super(TestMembership, self).setUp()
        self.product = self.env['product.product'].create(
            {
                'name': 'Membership product with variable period',
                'membership': True,
                'membership_date_from': '2015-01-01',
                'membership_date_to': '2015-12-31',
                'membership_type': 'variable',
                'membership_interval_qty': 1,
                'membership_interval_unit': 'weeks',
            })
        self.partner = self.env['res.partner'].create({'name': 'Test'})
        self.partner_account = self.partner.property_account_receivable_id.id

    def test_invoiced_membership(self):
        invoice_id = self.partner.create_membership_invoice()
        invoice = self.env['account.invoice'].search([('id', '=', invoice_id)])
        self.assertEqual(invoice.state, 'open')

    # def test_buy_membership_twice(self):

    # def test_check_membership_no_payment(self):
