# -*- coding: utf-8 -*-
{
    'name': "website_terms_of_use",
    'summary': """
        Adds two fields for terms of use and privacy policy to
        Website Admin menu""",

    'description': """
        Adds two fields for terms of use and privacy policy to
        Website Admin menu. You can add terms of use and privacy
        policy per website and these fields are displayed during
        the signup process.
    """,
    'author': "Goran Sunjka",
    'website': "http://www.sunjka.de",
    'category': 'Website',
    'version': '0.1',
    'depends': [
        'auth_signup',
        'base',
        'website',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/signup_views.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
}
