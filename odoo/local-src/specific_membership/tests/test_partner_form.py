# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import openerp.tests.common as test_common
from openerp import exceptions
from openerp.addons.cms_form.tests.common import fake_request
from ..controllers.account import MyProfile


class TestMemberForm(test_common.TransactionCase):

    def setUp(self):
        super(TestMemberForm, self).setUp()
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

    def test_edit_form_access(self):
        controller = MyProfile()
        partner = self.partner2.sudo(self.user1)
        with self.assertRaises(exceptions.AccessError):
            controller._can_edit(partner)
        partner = self.partner1.sudo(self.user2)
        with self.assertRaises(exceptions.AccessError):
            controller._can_edit(partner)

    def test_update(self):
        data = {
            'name': 'Edward Norton',
        }
        request = fake_request(form_data=data, method='POST')
        form_model = self.env['cms.form.res.partner'].sudo(self.user1)
        form = form_model.form_init(request, main_object=self.partner1)
        form.form_create_or_update()
        self.assertEqual(self.partner1.name, data['name'])
