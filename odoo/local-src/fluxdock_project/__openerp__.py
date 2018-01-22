# -*- coding: utf-8 -*-
# © 2016 Denis Leemann (Camptocamp SA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
     'name': 'Fluxdock Project specific development',
     'version': '9.0.1.0.0',
     'category': '',
     'author': 'Camptocamp',
     'maintainer': 'Camptocamp',
     'website': 'http://www.camptocamp.com/',
     'depends': [
          'cms_delete_content',
          'cms_form',
          'cms_notification',
          'fluxdock_theme',
          'mail_digest',
          'partner_project_expertise',
          'project',
          'fluxdock_membership',
     ],
     'data': [
          # demo
          'demo/ir_cron.xml',
          'data/project_proposal_demo.xml',
          'data/mail_message_subtype.xml',
          'data/proposal_data_menu.xml',
          'data/proposal_email_data.xml',
          # security
          'security/proposal.acl.csv',
          'security/reference.acl.csv',
          'security/proposal_record_rules.xml',
          'security/reference_record_rules.xml',
          # backend
          'views/project_proposal.xml',
          'views/project_reference.xml',
          'views/menu.xml',
          # frontend
          'templates/assets.xml',
          'templates/reference/reference_detail.xml',
          'templates/reference/my_home.xml',
          'templates/reference/search_form.xml',
          'templates/reference/help_msgs.xml',
          'templates/proposal/search_form.xml',
          'templates/proposal/my_home.xml',
          'templates/notification/notify.xml',
          'templates/notification/notification_listing.xml',
     ],
}
