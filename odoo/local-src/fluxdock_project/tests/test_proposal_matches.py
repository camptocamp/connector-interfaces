# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import odoo.tests.common as test_common


class TestMatches(test_common.TransactionCase):

    def setUp(self):
        super(TestMatches, self).setUp()
        Profession = self.env['project.partner.profession']
        self.prof1 = Profession.create({'name': 'Origami'})
        self.prof2 = Profession.create({'name': 'Dart throwing'})
        self.prof3 = Profession.create({'name': 'Caps stacking up'})

        user_model = self.env['res.users'].with_context(
            tracking_disable=True, no_reset_password=True)
        self.user1 = user_model.create({
            'name': 'User 1 (test)',
            'login': 'user_test_matches_1',
            'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])]
        })
        self.user1.partner_id.profession_ids = self.prof1 | self.prof2

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

    def test_match_profession(self):
        self.prop.profession_ids = self.prof1
        matches = self.user1.proposal_match_ids
        self.assertIn(self.prop, matches)

    def test_match_multiple_professions(self):
        self.prop.profession_ids = self.prof1 | self.prof2
        matches = self.user1.proposal_match_ids
        self.assertIn(self.prop, matches)

    def test_no_match_profession(self):
        self.prop.profession_ids = self.prof3
        matches = self.user1.proposal_match_ids
        self.assertNotIn(self.prop, matches)

    def test_matching_partners(self):
        self.prop.profession_ids = self.prof1
        self.assertIn(self.user1.partner_id, self.prop.matching_partner_ids)
