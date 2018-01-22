# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import odoo.tests.common as test_common
from odoo import exceptions


class TestPermission(test_common.TransactionCase):

    def setUp(self):
        super(TestPermission, self).setUp()
        user_model = self.env['res.users'].with_context(no_reset_password=1)
        self.user1 = user_model.create({
            'name': 'Member User 1 (test)',
            'login': 'testmember_user1',
            'email': 'testmember_user1@email.com',
            # make sure to have only portal group
            'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])]
        })
        self.partner1 = self.user1.partner_id
        self.user2 = user_model.create({
            'name': 'Member User 2 (test)',
            'login': 'testmember_user2',
            'email': 'testmember_user2@email.com',
            # make sure to have only portal group
            'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])]
        })
        self.partner2 = self.user2.partner_id
        self.user_noportal = user_model.create({
            'name': 'Member Noportal',
            'login': 'testmember_noportal',
            'email': 'testmember_noportal@email.com',
        })
        self.partner_noportal = self.user_noportal.partner_id

    def test_user_can_edit_own_partner(self):
        partner = self.partner1.sudo(self.user1)
        partner.write({'name': 'Foo'})
        self.assertEqual(self.partner1.name, 'Foo')
        partner = self.partner2.sudo(self.user2)
        partner.write({'name': 'Boo'})
        self.assertEqual(self.partner2.name, 'Boo')

    def test_user_cannot_edit_other_partners(self):
        partner = self.partner2.sudo(self.user1)
        with self.assertRaises(exceptions.AccessError):
            partner.write({'name': 'Foo'})
        partner = self.partner1.sudo(self.user2)
        with self.assertRaises(exceptions.AccessError):
            partner.write({'name': 'Boo'})

    def test_user_portal_rel(self):
        # on create
        self.assertEqual(self.partner1.user_id.id, self.user1.id)
        self.assertEqual(self.partner2.user_id.id, self.user2.id)
        self.assertNotEqual(
            self.partner_noportal.user_id.id, self.user_noportal.id)

        # on write
        self.user_noportal.write({
            'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])]
        })
        self.assertEqual(
            self.partner_noportal.user_id.id, self.user_noportal.id)
