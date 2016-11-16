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
        # use `email=False` to fix:
        #
        # 2016-11-16 16:30:07,369 85 INFO odoodb_test
        # openerp.addons.mail.models.mail_template:
        # Failed to render template <Template memory:7f5d0d39e050> using values
        # {'format_tz': <function <lambda> at 0x7f5d072d7b18>,
        #  'ctx': {'safe': False}, 'user': res.users(1,),
        # 'object': res.users(8,)}
        # Traceback (most recent call last):
        #   File "/opt/odoo/src/addons/mail/models/mail_template.py", line 364, in render_template  # noqa
        #     render_result = template.render(variables)
        #   File "/usr/local/lib/python2.7/dist-packages/jinja2/environment.py", line 969, in render  # noqa
        #     return self.environment.handle_exception(exc_info, True)
        #   File "/usr/local/lib/python2.7/dist-packages/jinja2/environment.py", line 742, in handle_exception  # noqa
        #     reraise(exc_type, exc_value, tb)
        #   File "<template>", line 1, in top-level template code
        #   File "/usr/local/lib/python2.7/dist-packages/jinja2/sandbox.py", line 330, in getattr  # noqa
        #     value = getattr(obj, attribute)
        #   File "/opt/odoo/src/openerp/fields.py", line 835, in __get__
        #     return record._cache[self]
        #   File "/opt/odoo/src/openerp/models.py", line 6132, in __getitem__
        #     return value.get() if isinstance(value, SpecialValue) else value
        #   File "/opt/odoo/src/openerp/fields.py", line 39, in get
        #     raise self.exception
        invoice = self.partner.create_membership_invoice(email=False)
        invoice = self.env['account.invoice'].search([('id', '=', invoice.id)])
        self.assertEqual(invoice.state, 'open')

    # def test_buy_membership_twice(self):

    # def test_check_membership_no_payment(self):
