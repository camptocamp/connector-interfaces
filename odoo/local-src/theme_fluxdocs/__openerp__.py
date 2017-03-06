{
    'name': 'Fluxdock Theme specific development',
    'description': 'Custom Theme for the fluxdock website.',
    'version': '1.0',
    'author': 'Pierre Sandrin',
    'data': [
        'templates/layout.xml',
        'templates/footer.xml',
        'templates/blog_news_list.xml',
        'templates/snippets.xml',
        'templates/options.xml',
        'templates/assets.xml',
        'templates/listing.xml',
        'templates/widgets.xml',
        'templates/mosaic.xml',
        'templates/status_msg.xml',
        'templates/search_form.xml',
        'pages/homepage.xml',
    ],
    'category': 'Theme/Creative',
    'depends': [
        'website',
        'website_blog',
        'website_portal',
        'cms_status_message',
        'cms_delete_content',
        'cms_form',
    ],
}
