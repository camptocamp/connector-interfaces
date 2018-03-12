import anthem


@anthem.log
def remove_submenus(ctx):
    xmlids = [
        "__setup__.website_menu_partners",
        "__setup__.website_menu_proposals",
        "__setup__.website_menu_references",
    ]
    for xmlid in xmlids:
        item = ctx.env.ref(xmlid, raise_if_not_found=False)
        if item:
            item.unlink()


@anthem.log
def post(ctx):
    remove_submenus(ctx)
