{
    'name': 'Website Fluxdock Signup',
    'summary': '',
    'description': """
    Fluxdock sign up
        """,
    'author': 'Goran Sunjka',
    'website': 'https://www.sunjka.de/',
    'category': 'Website',
    'version': '1.0',
    'depends': [
        'auth_signup',
        'web',
        'website',
        'website_mass_mailing',
        'website_terms_of_use',
        'website_portal',
        'website_portal_profile',
        # 'website_portal_project'
    ],
    'data': [
        'views/templates.xml',
        'fluxdock_signup_data.xml'
    ],
    'installable': True,
}
