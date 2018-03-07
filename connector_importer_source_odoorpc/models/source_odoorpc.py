# Author: Simone Orsi
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from ..utils import OdooRPCHandler
from odoo import models, fields, api
from odoo.tools.safe_eval import safe_eval
from collections import defaultdict


class OdooRPCSource(models.Model):
    _name = 'import.source.odoorpc'
    _inherit = 'import.source'
    _description = 'OdooRPC import source'
    _source_type = 'OdooRPC'
    _source_handler = OdooRPCHandler

    odoo_rpc_config_id = fields.Many2one(
        comodel_name='import.odoorpc.config',
        required=True,
    )
    odoo_source_model = fields.Char(help='res.users')
    odoo_source_domain = fields.Char(
        default='[]',
        help="[('company_id', '=', 1)]"
    )
    odoo_source_fields = fields.Char(
        help="Semicolumn-separated field names. "
             "Use column to state relation values to read. "
             "ie: name;parent_id;category_id:name` "
    )
    odoo_source_limit = fields.Integer()

    @api.multi
    def eval_domain(self):
        self.ensure_one()
        return safe_eval(self.odoo_source_domain or '[]')

    def _get_lines(self):
        """Retrieve lines to import.

        Based on the settings we can read main records
        and related records in the same place.

        For instance, if you want to read partners and partners' categories
        you can set this into `odoo_source_fields`:

            name;supplier;customer;category_id:name

        The result will be:

            [{
                'name': 'John Doe',
                'supplier': False,
                'customer': True,
                'category_id': 4,
                '_model': 'res.partner',
            }, {
                'name': 'Good boy',
                '_model': 'res.partner.category',
            }, ]

        Then if you use the importer `odoorpc.base.importer` as a base
        lines will be filtered out based on `_model` and `_apply_on`.
        """
        conn = self._rpc_connect_and_login()
        remote_model = conn.env[self.odoo_source_model]
        to_read, to_follow = self._rpc_fields_to_read(remote_model)
        # get main records
        records = remote_model.search_read(
            self.eval_domain(), to_read, limit=self.odoo_source_limit or None)
        # get what we should read on followed records
        to_follow_read = self._rpc_followed_to_read(records, to_follow)
        # read and yield followed
        for follow_rel in to_follow_read.keys():
            follow_ids = list(set(to_follow_read[follow_rel]['ids']))
            follow_fields = list(to_follow_read[follow_rel]['fields'])
            follow_model = conn.env[follow_rel]
            # trick: use browse+read as in tests we are mocking the env
            # w/ the test one so that calling read on an empty recordset
            # won't produce any result.
            followed_records = follow_model.browse(
                follow_ids).read(follow_fields)
            for followed in followed_records:
                followed['_model'] = follow_rel
                followed['_line_nr'] = followed['id']
                yield followed
        # yield main records
        for rec in records:
            rec['_model'] = self.odoo_source_model
            rec['_line_nr'] = rec['id']
            yield rec

    @api.multi
    def _rpc_connect_and_login(self):
        """Connect to remote Odoo, login and give back connection."""
        self.ensure_one()
        handler = self._source_handler(**self._rpc_connect_data())
        connection = handler.connect_and_login()
        return connection

    def _rpc_connect_data(self):
        """Retrieve data to connect to remote Odoo."""
        data = self.odoo_rpc_config_id.read(
            self._source_handler.required_attrs)[0]
        del data['id']
        data['odoo_port'] = int(data['odoo_port'])
        return data

    def _rpc_fields_to_read(self, remote_model):
        """"Collect fields to read and to follow.

        :param `remote_model`: browse remote model
        :return: tuple w (to_read, to_follow)
            `to_read` is a simple list of fields to read on the main model
            `to_follow` is a mapping `field name` -> list of fields to read
            on the related record.
        """

        to_read = []
        to_follow = defaultdict(dict)
        for fname in self.odoo_source_fields.strip().split(';'):
            fname, _, _to_follow = fname.partition(':')
            fname = fname.strip()
            to_read.append(fname)
            if _to_follow.strip():
                if _to_follow.strip() == '*':
                    # all fields
                    _fields = []
                else:
                    _fields = [
                        x.strip() for x in _to_follow.split(',') if x.strip()
                    ]
                to_follow[fname]['fields'] = _fields
        if to_follow:
            fields_info = remote_model.fields_get(
                allfields=list(to_follow.keys()),
                attributes=['relation', 'type'])
            for fname in to_follow.keys():
                to_follow[fname].update(fields_info[fname])
        return to_read, to_follow

    def _rpc_followed_to_read(self, records, to_follow):
        """Retrieve info on followed fields.

        :param records: main records
        :param to_follow: mapping main field: relate fields
        :return: mapping of fields and record ids to read by model

        To read all followed records at once, we collect all the ids
        of those records and build a mapping like:

            `res.partner.category`: {
                'ids': [1, 2, 3],
                'fields': ['name', 'parent_id', ],
            }
        """
        to_follow_read = {}
        for rec in records:
            for fname, info in to_follow.items():
                if info['relation'] not in to_follow_read:
                    to_follow_read[info['relation']] = {
                        'ids': [],
                        'fields': [],
                    }
                ids = rec[fname]
                # unfortunately we cannot use `load='_classic_write'`
                # with `search_read` so we cleanup values like (1, 'Foo')
                if info['type'] == 'many2one':
                    # handle them as x2m, we are just collecting ids to read
                    ids = [ids[0]]
                to_follow_read[info['relation']]['ids'].extend(ids)
                to_follow_read[info['relation']]['fields'].append(fname)
        return to_follow_read
