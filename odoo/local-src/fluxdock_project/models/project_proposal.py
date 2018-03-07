# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import _, api, exceptions, fields, models
from odoo.addons.http_routing.models.ir_http import slug

from datetime import datetime, timedelta
import logging
logger = logging.getLogger('[project_proposal]')


class ProjectProposal(models.Model):
    """Future project to find partners and collaborators. """

    _name = 'project.proposal'
    _description = "Project proposal"
    _inherit = [
        'mail.thread',
        'website.published.mixin',
    ]
    _order = 'website_published DESC, create_date DESC'

    # we use this for website template add action
    cms_create_url = '/dock/proposals/add'
    cms_after_delete_url = '/my/dock'
    cms_search_url = '/dock/proposals'

    @api.multi
    def _compute_cms_edit_url(self):
        for item in self:
            item.cms_edit_url = item.website_url + '/edit'

    @api.multi
    def _compute_website_url(self):
        for item in self:
            item.website_url = self.cms_search_url + '/' + slug(item)

    name = fields.Char(
        string="Proposal Name",
        required=True
    )
    display_name = fields.Char(
        string="Display name",
        readonly=True,
        related='name'
    )
    create_uid = fields.Many2one(
        'res.users',
        'Owner',
        select=True,
        readonly=True,
    )
    # TODO: still needed?
    color_owner_id = fields.Integer(
        string="Color index of owner",
        compute='_get_color_owner_id',
        readonly=True,
        store=False,
    )  # Color of owner
    location = fields.Char()
    country_id = fields.Many2one(comodel_name='res.country', string="Country")
    # TODO 2016-12-05:
    # why are we not using website.seo.mixin to get this field????
    website_short_description = fields.Text(
        string="Teaser text",
        help=("Write a short description of the Project.")
    )
    website_description = fields.Text(
        string="Description",
        help=("Describe the project you have in mind.")
    )
    start_date = fields.Date(string="Start date")
    stop_date = fields.Date(string="End date")
    duration = fields.Integer()
    profession_ids = fields.Many2many(
        comodel_name="project.partner.profession",
        string="Professions",
        help="Which professions do you need for your project?",
    )

    is_new = fields.Boolean(
        compute='_is_new'
    )
    # contact fields
    contact_name = fields.Char(
        help='Contact person for this project.'
    )
    contact_email = fields.Char()
    contact_phone = fields.Char()

    matching_partner_ids = fields.Many2many(
        string="Matching partners",
        comodel_name="res.partner",
        compute="_compute_matching_partner_ids",
    )
    # flag used to determine if the proposal needs notification
    notify_dirty = fields.Boolean(default=False)
    enable_matches_notification = fields.Boolean(default=True)

    @api.depends('create_uid')
    def _get_color_owner_id(self):
        for rec in self:
            rec.color_owner_id = rec.create_uid.id

    @api.multi
    def toggle_published(self):
        """ Inverse the value of the field ``published`` on the records in
        ``self``.
        """
        for record in self:
            record.website_published = not record.website_published

    @api.multi
    def _is_new(self):
        for rec in self:
            create_date = fields.Datetime.from_string(rec.create_date)
            rec.is_new = (datetime.now() - create_date).days < 15

    @api.multi
    def blacklist(self):
        self.env.user.proposal_blacklist_ids |= self

    @api.multi
    def unblacklist(self):
        self.env.user.proposal_blacklist_ids -= self

    @api.onchange('start_date', 'stop_date')
    def onchange_dates(self):
        if not self.start_date or not self.stop_date:
            return
        start = fields.Datetime.from_string(self.start_date)
        stop = fields.Datetime.from_string(self.stop_date)
        self.duration = (stop - start).days

    @api.onchange('duration')
    def onchange_duration(self):
        if not self.start_date or not self.duration:
            return
        start = fields.Datetime.from_string(self.start_date)
        end = start + timedelta(days=self.duration)
        self.stop_date = end

    @api.constrains('start_date', 'stop_date')
    def _check_date_order(self):
        for rec in self:
            if (rec.start_date and rec.stop_date and
                    rec.stop_date < rec.start_date):
                raise exceptions.UserError(
                    _('End Date cannot be set before Start Date.'))

    @api.multi
    @api.depends('profession_ids')
    def _compute_matching_partner_ids(self):
        """Get matching partners by profession."""
        partner_sudo = self.env['res.partner'].sudo()
        for item in self:
            # TODO 2018-02-1: as of v11 refactoring and membership cleanup
            # we are getting a perm issue here in tests.
            # Should be ok to sudo here as we need to compute
            # all possible matches. Nevertheless: let's double check this
            # when we have time.
            item_sudo = item.sudo()
            if isinstance(item.id, models.NewId):
                # bad fields behavior in form:
                # when removing a tag here you get a new object :/
                continue
            item.matching_partner_ids = partner_sudo.search([
                '|',
                ('profession_ids', 'in', item_sudo.profession_ids.ids),
                ('user_id.proposal_blacklist_ids', 'not in', [item_sudo.id, ]),
                ('id', '!=', item_sudo.create_uid.partner_id.id),
            ])

    @property
    def _matches_subtype(self):
        return self.env.ref(
            'fluxdock_project.mt_proposal_matches'
        )

    @api.model
    def create(self, vals):
        """Override to mark as `dirty` when needed."""
        res = super(ProjectProposal, self).create(vals)
        # notify only published objects
        if not res.website_published:
            return res
        if not self.env.context.get('notify_disable') \
                and res._matches_to_be_notified():
            res.set_notify_dirty(True)
        return res

    @api.multi
    def write(self, vals):
        """Override to mark as `dirty` when needed."""
        res = super(ProjectProposal, self).write(vals)
        if not self.env.context.get('notify_disable'):
            for item in self:
                # notify only published objects
                if (not item.website_published or
                        not item.enable_matches_notification):
                    continue
                # yes, we write once more but we don't want tracking here
                # and we need proposal to be saved to fetch updated matches
                if item._matches_to_be_notified():
                    item.set_notify_dirty(True)
        return res

    @api.multi
    def _notified_partners(self, partner_ids):
        """Return partners' id that have been notified for current object."""
        # TODO: is this enough? We are relying on existing messages
        # but if you delete them, partners can be notified twice
        self.ensure_one()
        domain = [
            ('partner_ids', 'in', partner_ids),
            ('model', '=', self._name),
            ('res_id', '=', self.id),
            ('subtype_id', '=', self._matches_subtype.id),
        ]
        return self.env['mail.message'].search(domain).mapped('partner_ids')

    @api.model
    def _matches_to_be_notified(self):
        """Return matches to be notified."""
        to_be_notified = []
        matching_partner_ids = self.matching_partner_ids.ids
        if matching_partner_ids:
            notified = self._notified_partners(matching_partner_ids)
            to_be_notified = set(matching_partner_ids).difference(notified.ids)
        return list(to_be_notified)

    # TODO: this part could be made generic
    # and put in an extra module to be reusable

    def set_notify_dirty(self, value):
        self.with_context(
            **self._notify_restricted_context()).write({'notify_dirty': value})

    def _notify_restricted_context(self):
        return {
            'notify_only_recipients': True,
            'tracking_disable': True,
            'notify_disable': True,
        }

    @api.multi
    def button_test_notify_match(self):
        self.ensure_one()
        self.cron_notify_matches(domain=[('id', '=', self.id)])
        self.env['mail.digest'].process()

    @api.model
    def cron_notify_matches(self, domain=None):
        """Create messages to notify matches."""
        # 1. search for proposals that have matches (dirty)
        # 2. get only matching partners that did not received yet notifications
        # matching: model, res_id, subtype_id
        # 3. mark proposal as not dirty
        if domain is None:
            domain = [
                ('website_published', '=', True),
                ('notify_dirty', '=', True),
                ('enable_matches_notification', '=', True),
            ]
        proposals = self.search(domain)
        proposals._create_match_messages()
        proposals.set_notify_dirty(False)

    def _match_message_body(self, proposal, lang):
        template = self.env.ref(
            'fluxdock_project.message_proposal_match')
        return template.with_context(lang=lang).render({'proposal': proposal})

    @api.multi
    def _match_message_defaults(self):
        self.ensure_one()
        return {
            'model': self._name,
            'res_id': self.id,
            'no_auto_thread': True,
            'subject': _('Proposal match'),
            'subtype_id': self._matches_subtype.id,
        }

    @api.multi
    def _create_match_messages(self):
        msg_model = self.env['mail.message'].sudo(
        ).with_context(**self._notify_restricted_context())
        for item in self:
            to_be_notified = item._matches_to_be_notified()
            if not to_be_notified or not item.website_published:
                continue
            values = item._match_message_defaults()
            # mail.message do not have translations
            # hence we must render message by partner lang.
            # We group them here and we create 1 message per lang.
            grouped = {}
            domain = [
                ('id', 'in', to_be_notified),
                ('notification_type', '=', 'email'),
            ]
            partner_langs = self.env['res.partner'].search_read(
                domain, ['lang', ])
            for rec in partner_langs:
                grouped.setdefault(rec['lang'], []).append(rec['id'])
            for lang, pids in grouped.items():
                values['body'] = self._match_message_body(item, lang)
                values['partner_ids'] = [
                    (4, _id) for _id in pids
                ]
                msg_model.create(values)
            logger.info(
                'Created match messages for prop: %d, partners: %s',
                item.id,
                ', '.join([str(x) for x in to_be_notified])
            )
