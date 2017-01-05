# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import openerp.tests.common as test_common


class TestVisibility(test_common.TransactionCase):

    def setUp(self):
        super(TestVisibility, self).setUp()
        self.user1 = self.env['res.users'].create({
            'name': 'User1',
            'login': 'user_test_visibility_1',
            'email': 'user1@email.com',
        })
        self.user2 = self.env['res.users'].create({
            'name': 'User2',
            'login': 'user_test_visibility_2',
            'email': 'user2@email.com',
        })

        self.Proposal = self.env['project.proposal']

        # Count demo data
        self.seen_usr1 = self.Proposal.sudo(self.user1).search([])
        self.seen_usr2 = self.Proposal.sudo(self.user2).search([])

        self.prop1usr1 = self.Proposal.sudo(self.user1).create({
            'name': "Project 1 Owner 1",
            'website_published': True,
        })
        self.prop2usr1 = self.Proposal.sudo(self.user1).create({
            'name': "Project 2 Owner 1",
            'website_published': True,
        })
        self.prop1usr2 = self.Proposal.sudo(self.user2).create({
            'name': "Project 1 Owner 2",
            'website_published': True,
        })
        self.prop2usr2 = self.Proposal.sudo(self.user2).create({
            'name': "Project 2 Owner 2",
            'website_published': False,
        })

    def test_deactivate(self):
        seen_by_user1 = self.Proposal.sudo(self.user1).search([])
        seen_by_user2 = self.Proposal.sudo(self.user2).search([])

        self.assertEquals(len(seen_by_user1), 3 + len(self.seen_usr1))
        self.assertEquals(len(seen_by_user2), 4 + len(self.seen_usr2))

        visible = self.prop1usr1 | self.prop2usr1 | self.prop1usr2
        self.assertEquals(seen_by_user1, visible | self.seen_usr1)
        visible |= self.prop2usr2
        self.assertEquals(seen_by_user2, visible | self.seen_usr2)

        self.prop1usr1.toggle_published()
        self.prop2usr1.toggle_published()
        self.prop2usr2.toggle_published()

        seen_by_user1 = self.Proposal.sudo(self.user1).search([])
        seen_by_user2 = self.Proposal.sudo(self.user2).search([])
        self.assertEquals(len(seen_by_user1), 4 + len(self.seen_usr1))
        self.assertEquals(len(seen_by_user2), 2 + len(self.seen_usr2))

        # this time user one sees everything
        visible = visible
        self.assertEquals(seen_by_user1, visible | self.seen_usr1)
        visible = self.prop1usr2 | self.prop2usr2
        self.assertEquals(seen_by_user2, visible | self.seen_usr2)
