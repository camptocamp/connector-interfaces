# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def update_existing_matches(ctx):
    proposals = ctx.env['project.proposal'].search(
        [('website_published', '=', True)]
    )
    # set as dirty and rely on cron to handle notifications
    proposals.set_notify_dirty(True)


@anthem.log
def main(ctx):
    update_existing_matches(ctx)
