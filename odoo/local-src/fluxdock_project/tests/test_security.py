# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import odoo.tests.common as test_common
# from odoo import exceptions
from .base import BaseTestCase


class TestReference(BaseTestCase, test_common.TransactionCase):

    @property
    def model(self):
        return self.env['project.reference'].with_context(no_profile_update=1)


class TestProposal(BaseTestCase, test_common.TransactionCase):

    @property
    def model(self):
        return self.env['project.proposal'].with_context(no_profile_update=1)
