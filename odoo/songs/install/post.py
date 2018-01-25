# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def remove_useless_menuitems(ctx):
    """ Remove useless website menu items """
    xmlids = (
        'website_slides.website_menu_slides',
        # TODO: remove this when we integrate blog features
        'website_blog.menu_news',
        'website.menu_contactus',
    )
    ids = []
    for xmlid in xmlids:
        item = ctx.env.ref(xmlid, raise_if_not_found=False)
        if item:
            ids.append(item.id)
    if ids:
        ctx.env['website.menu'].browse(ids).unlink()


@anthem.log
def setup_website_languages(ctx):
    """ Adding languages to website """
    website_langs = [ctx.env.ref('base.lang_en').id, ]
    for code in ('de_DE',):
        lang = ctx.env['res.lang'].search([('code', '=', code)])
        website_langs.append(lang.id)
    ws = ctx.env['website'].browse(1)
    ws.write({'language_ids': [(6, 0, website_langs), ]})


@anthem.log
def enable_html_compression(ctx):
    """ Enable html compression """
    ws = ctx.env['website'].search([])
    ws.write({'compress_html': True})


@anthem.log
def main(ctx):
    """ Main: creating demo data """
    remove_useless_menuitems(ctx)
    setup_website_languages(ctx)
    enable_html_compression(ctx)
