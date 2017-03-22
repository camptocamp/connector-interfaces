# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import openerp.tests.common as test_common


class TestMatches(test_common.TransactionCase):

    def setUp(self):
        super(TestMatches, self).setUp()
        self.cat1 = self.env.ref('base.res_partner_category_4')
        self.cat2 = self.env.ref('base.res_partner_category_5')
        self.cat3 = self.env.ref('base.res_partner_category_6')
        Expertise = self.env['partner.project.expertise']
        self.exp1 = Expertise.create({'name': 'Origami'})
        self.exp2 = Expertise.create({'name': 'Dart throwing'})
        self.exp3 = Expertise.create({'name': 'Caps stacking up'})

        user_model = self.env['res.users'].with_context(no_reset_password=1)
        self.user1 = user_model.create({
            'name': 'User 1 (test)',
            'login': 'user_test_matches_1',
            'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])]
        })
        self.user1.partner_id.category_id = self.cat1 | self.cat2
        self.user1.partner_id.expertise_ids = self.exp1 | self.exp2

        self.user2 = user_model.create({
            'name': 'User 2 (test)',
            'login': 'user_test_matches_2',
            'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])]
        })

        self.prop = self.env['project.proposal'].create({
            'name': "Project 1",
            'create_uid': self.user2.id,
            'website_published': True,
        })

    def test_match_expertise(self):
        self.prop.expertise_ids = self.exp1
        matches = self.user1.proposal_match_ids
        self.assertIn(self.prop, matches)

    def test_match_multiple_expertises(self):
        self.prop.expertise_ids = self.exp1 | self.exp2
        matches = self.user1.proposal_match_ids
        self.assertIn(self.prop, matches)

    def test_no_match_expertise(self):
        self.prop.expertise_ids = self.exp3
        matches = self.user1.proposal_match_ids
        self.assertNotIn(self.prop, matches)

    def test_match_industry(self):
        self.prop.industry_ids = self.cat1
        matches = self.user1.proposal_match_ids
        self.assertIn(self.prop, matches)

    def test_match_multiple_industries(self):
        self.prop.industry_ids = self.cat1 | self.cat2
        matches = self.user1.proposal_match_ids
        self.assertIn(self.prop, matches)

    def test_no_match_industry(self):
        self.prop.industry_ids = self.cat3
        matches = self.user1.proposal_match_ids
        self.assertNotIn(self.prop, matches)

    def test_match_both(self):
        self.prop.expertise_ids = self.exp1
        self.prop.industry_ids = self.cat1
        matches = self.user1.proposal_match_ids
        self.assertIn(self.prop, matches)

    def test_match_both_full(self):
        self.prop.expertise_ids = self.exp1 | self.exp2
        self.prop.industry_ids = self.cat1 | self.cat2
        matches = self.user1.proposal_match_ids
        self.assertIn(self.prop, matches)

    def test_matching_partners(self):
        self.prop.expertise_ids = self.exp1
        self.assertIn(self.user1.partner_id, self.prop.matching_partner_ids)
