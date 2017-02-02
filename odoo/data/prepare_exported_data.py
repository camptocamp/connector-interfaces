# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

"""
A script to convert exported csv data to scenario data.
"""

import csv
import os

FILE_IN = 'demo/_res.partner.category.csv'
FILE_OUT = 'demo/res.partner.category.csv'

PATH_BASE = os.path.dirname(__file__)
PATH_IN = os.path.join(PATH_BASE, FILE_IN)
PATH_OUT = os.path.join(PATH_BASE, FILE_OUT)
FIELDNAMES = ['id', 'name', ]
DELIMITER = ','


def cleanup_string(val):
    return val.replace('-', '_').replace(' ', '')


def toxmlid(val):
    prefix = 'sc.partner_categ_'
    if not val.startswith(prefix):
        val = prefix + val
    return cleanup_string(val).lower()


def prepare_rows(limit=0):
    rows_to_write = []
    with open(PATH_IN, 'r') as infile:
        for i, line in enumerate(csv.DictReader(infile, delimiter=DELIMITER)):
            if limit and i == limit:
                break
            # fix id
            line['id'] = toxmlid(line['name'])
            rows_to_write.append(line)
    return rows_to_write


def main():
    rows_to_write = prepare_rows()
    print('Processed %s lines.' % len(rows_to_write))
    fieldnames = FIELDNAMES
    path_out = PATH_OUT

    print('Input file %s', PATH_IN)
    print('Output file %s', path_out)

    with open(path_out, 'w') as outfile:
        writer = csv.DictWriter(
            outfile, fieldnames=fieldnames, delimiter=DELIMITER)
        writer.writeheader()
        writer.writerows(rows_to_write)

    print('OUT CSV ready.')


if __name__ == "__main__":
    main()
