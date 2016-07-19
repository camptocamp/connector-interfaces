# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import openerp.tests.common as test_common


class TestVisibility(test_common.TransactionCase):

    def test_deactivate(self):
        seen_by_user1 = self.Proposal.sudo(self.user1).search([])
        seen_by_user2 = self.Proposal.sudo(self.user2).search([])

        self.assertEquals(len(seen_by_user1), 3)
        self.assertEquals(len(seen_by_user2), 4)

        visible = self.prop1usr1 | self.prop2usr1 | self.prop1usr2
        self.assertEquals(seen_by_user1, visible)
        visible |= self.prop2usr2
        self.assertEquals(seen_by_user2, visible)

        self.prop1usr1.toggle_published()
        self.prop2usr1.toggle_published()
        self.prop2usr2.toggle_published()

        seen_by_user1 = self.Proposal.sudo(self.user1).search([])
        seen_by_user2 = self.Proposal.sudo(self.user2).search([])
        self.assertEquals(len(seen_by_user1), 4)
        self.assertEquals(len(seen_by_user2), 2)

        # this time user one sees everything
        visible = visible
        self.assertEquals(seen_by_user1, visible)
        visible = self.prop1usr2 | self.prop2usr2
        self.assertEquals(seen_by_user2, visible)

    def setUp(self):
        super(TestVisibility, self).setUp()
        self.user1 = self.env['res.users'].create({
            'name': 'User1',
            'login': 'usr1',
        })
        self.user2 = self.env['res.users'].create({
            'name': 'User2',
            'login': 'usr2',
        })

        self.Proposal = self.env['project.proposal']
        self.prop1usr1 = self.Proposal.create({
            'name': "Project 1 Owner 1",
            'owner_id': self.user1.id,
            'published': True,
        })
        self.prop2usr1 = self.Proposal.create({
            'name': "Project 2 Owner 1",
            'owner_id': self.user1.id,
            'published': True,
        })
        self.prop1usr2 = self.Proposal.create({
            'name': "Project 1 Owner 2",
            'owner_id': self.user2.id,
            'published': True,
        })
        self.prop2usr2 = self.Proposal.create({
            'name': "Project 2 Owner 2",
            'owner_id': self.user2.id,
            'published': False,
        })
