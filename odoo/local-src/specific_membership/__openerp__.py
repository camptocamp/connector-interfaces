# -*- coding: utf-8 -*-
# © 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Fluxdock Membership Specific Development',
    'version': '9.0.1.0.0',
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
        'base',
        'membership',
        'membership_variable_period',
        'auth_signup',
        'auth_signup_verify_email',
        'website',
        'website_portal',
        'website_mass_mailing',
        'website_terms_of_use',
        'website_portal_sale',
        'website_partner',
        'website_membership',
        'partner_project_expertise',
    ],
    'data': [
        'security/ir.model.access.csv',
        # views
        'views/partner_view.xml',
        # templates
        'templates/assets.xml',
        'templates/membership.xml',
        'templates/signup.xml',
        'templates/profile/reset.xml',
        # TODO: go trough these templates and check for stuff to move/merge
        'templates/profile/templates.xml',
        'templates/profile/members.xml',
        'templates/profile/upload.xml',
        # data
        'data/membership_data.xml',
        'data/group_data.xml',
        'data/email_data.xml',
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
}
