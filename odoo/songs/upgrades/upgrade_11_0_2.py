import anthem


SWITCH_KLASSES = (
    ('opt_dark_bg', 'bg-flux_dark'),
    ('opt_dark_grid_bg', 'bg-flux_dark_grid'),
)


@anthem.log
def replace_homepage_css_klasses(ctx):
    # CSS klasses have been updated: replace them in the homepage
    page = ctx.env.ref('fluxdock_theme.homepage')
    arch = page.arch
    for old, new in SWITCH_KLASSES:
        arch = arch.replace(old, new)
    page.arch = arch


@anthem.log
def pre(ctx):
    replace_homepage_css_klasses(ctx)
