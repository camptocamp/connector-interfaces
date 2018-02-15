# Copyright 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Fluxdock Membership specific development',
    'version': '11.0.1.0.0',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'category': 'Reports',
    'website': 'http://www.camptocamp.com',
    'images': [],
    "external_dependencies": {
        "python": [
            "validate_email",
        ],
    },
    'depends': [
        'auth_signup_verify_email',
        'auth_signup',
        'cms_form',
        'cms_status_message',
        'cms_account_form',
        'fluxdock_theme',
        'http_routing',
        'l10n_ch',
        'project_expertise',
        'website_partner',
        'website',
    ],
    'data': [
        # data
        'data/group_data.xml',
        'data/email_data.xml',
        # security
        'security/ir.model.access.csv',
        'security/partner_rules.xml',
        # backend views
        'views/partner_view.xml',
        # reports
        # FIXME 2018-01-24
        # ATM is not clear if we have to keep this report. If yes:
        # - fix templates according to
        # https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-11.0  # noqa
        # - reports have to be splitted out to fluxdock_reports
        # 'reports/assets.xml',
        # 'reports/layout.xml',
        # 'reports/invoice.xml',
        # templates
        'templates/assets.xml',
        'templates/signup.xml',
        'templates/help_msgs.xml',
        'templates/profile/widgets.xml',
        'templates/profile/upload.xml',
        'templates/membership/search_form.xml',
        # FIXME: something changed into publisher widget
        'templates/membership/member_detail.xml',
    ],
    'installable': True,
}
