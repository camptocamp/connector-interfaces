{
    'name': 'Website Portal Profile',
    'author': 'Goran Sunjka',
    'category': 'Website',
    'summary': '',
    'version': '1.1',
    'description': """
    Enhanced Portal Profile
        """,
    'website': 'https://www.sunjka.de/',
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
