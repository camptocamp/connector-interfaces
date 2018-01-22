# Copyright 2016 Denis Leemann (Camptocamp SA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Fluxdock Project specific development',
    'version': '11.0.1.0.0',
    'category': '',
    'author': 'Camptocamp',
    'website': 'http://www.camptocamp.com/',
    'depends': [
        'base',
        'cms_delete_content',
        'cms_form',
        'cms_notification',
        'fluxdock_membership',
        'fluxdock_theme',
        'mail_digest',
        'project_expertise',
        'project',
    ],
    'demo': [
        'demo/project_proposal_demo.xml',
    ],
    'data': [
        # data
        'data/ir_cron.xml',
        'data/mail_message_subtype.xml',
        'data/proposal_data_menu.xml',
        'data/proposal_email_data.xml',
        # security
        'security/proposal/ir.model.access.csv',
        'security/proposal/proposal_record_rules.xml',
        'security/reference/ir.model.access.csv',
        'security/reference/reference_record_rules.xml',
        # backend
        'views/project_proposal.xml',
        'views/project_reference.xml',
        'views/menu.xml',
        # frontend
        'templates/assets.xml',
        'templates/reference/reference_detail.xml',
        # TODO: my home is going to be dropped
        # 'templates/reference/my_home.xml',
        'templates/reference/search_form.xml',
        'templates/reference/help_msgs.xml',
        'templates/proposal/search_form.xml',
        # TODO: my home is going to be dropped
        # 'templates/proposal/my_home.xml',
        'templates/notification/notify.xml',
        'templates/notification/notification_listing.xml',
    ],
}
