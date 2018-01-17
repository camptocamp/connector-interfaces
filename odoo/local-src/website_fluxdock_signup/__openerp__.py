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
        # TODO 2016-10-21: dep needed to make the upgrade work.
        # Without this all the fields previously defined by this module
        # are not found and all related inherited views are broken.
        # Remove it (or the whole module)
        # after the 1st upgrade of `specific_membership`
        'specific_membership',
    ],
    'data': [
    ],
    'installable': False,
}
