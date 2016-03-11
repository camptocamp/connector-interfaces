{
    'name': 'Website Fluxdock Signup',
    'author': 'Goran Sunjka',
    'category': 'Website',
    'summary': '',
    'version': '1.0',
    'description': """
    Fluxdock sign up
        """,
    'website': 'https://www.sunjka.de/',
    'depends': [
        'auth_signup',
        'partner_area',
        'website',
        'website_mass_mailing',
        'website_portal',
        'website_portal_profile',
        'website_portal_project'
    ],
    'data': [
        'views/templates.xml',
        'fluxdock_signup_data.xml'
    ],
    'installable': True,
}
