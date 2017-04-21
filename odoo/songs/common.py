# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from pkg_resources import Requirement
from pkg_resources import resource_stream
from anthem.lyrics.loaders import load_csv_stream

req = Requirement.parse('fluxdock')


def load_file_content(path):
    return resource_stream(req, path)


def load_csv(ctx, path, model, delimiter=','):
    content = resource_stream(req, path)
    load_csv_stream(ctx, model, content, delimiter=delimiter)
