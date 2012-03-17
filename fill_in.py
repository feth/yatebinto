#!/usr/bin/python3

"""
Business card generator
Call me from command line

/* This program is free software. It comes without any warranty, to
 * the extent permitted by applicable law. You can redistribute it
 * and/or modify it under the terms of the Do What The Fuck You Want
 * To Public License, Version 2, as published by Sam Hocevar. See
 * http://sam.zoy.org/wtfpl/COPYING for more details. */
"""

RETURN_CODES = IO_ERR_TEMPLATE, IO_ERR_CSV, IO_ERR_COMMON_CSV, DATA_ERR = 1, 2, 3, 4


LOGFORMAT = "[%(levelname)-10s] %(message)s"
import logging
import sys
try:
    import argparse
except ImportError:
    logging.exception("""*** Unable to import *argparse*. \
Maybe install python-argpase. Exiting with status 2.***""")
    sys.exit(2)

#cf bug http://www.logilab.org/ticket/2481
# pylint: disable=W0402
# no, string is not deprecated!
from string import Template
# pylint: enable=W0402
import csv

# indexes:
FIRSTNAME, NAME, STREET, POSTCODE, CITY, TEL = tuple(range(6))

#defaults
DEFAULT_TEMPLATE = "template/template.svg"
DEFAULT_PREFIX = "generated/business_cards"
DEFAULT_CSV = "data.csv"
DEFAULT_COMMON_CSV = "common.csv"


class MissingData(Exception):
    """custom exception when we can't fill the template"""
    pass


def write_svg(row, template, out_prefix, header, common):
    """
    for every parsed csv row, spits a file
    """
    out_name = '%s.svg' % '_'.join((out_prefix, row[FIRSTNAME], row[NAME]))

    with open(out_name, 'w', encoding='utf-8') as out:
        replacements = common.copy()
        for index, item in enumerate(header):
            addition = row[index]
            if addition:
                #only override with non empty values
                replacements[item] = row[index]
        logging.debug("Replacements: %s", replacements)
        try:
            out.write(template.substitute(replacements))
        except KeyError as err:
            logging.error("Seems the template contains '%s', "
            "but we only have replacements for [%s]",
            err, ', '.join(replacements.keys()))
            raise MissingData()
        logging.info("Wrote file: %s", out_name)


def _strip_row(row):
    """
    strips every string in row (iterable). returns a list of strings
    """
    return [item.strip() for item in row]


def process(parser, values):
    """
    Give it a dict with information, does the job.
    There are defaults.
    Expected in the dict (but defaults are ok):
    * template_file: svg file name, file has $variables in it
    * csv_file: data in columns:
        FIRSTNAME, NAME, STREET, POSTCODE, CITY, TEL
    * output_prefix: we'll spit out files named like this
    """
    verbosity = sum(values.get('v'))
    if verbosity == 0:
        level = logging.WARNING
    elif verbosity == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG
    logging.basicConfig(level=level, format=LOGFORMAT)

    template_file = values.get('template', DEFAULT_TEMPLATE)
    csv_file = values.get('input', DEFAULT_CSV)
    common_csv_file = values.get('common_input')
    output_prefix = values.get('output_prefix', DEFAULT_PREFIX)

    #1/3 template
    try:
        with open(template_file, 'r', encoding='utf-8') as template_fd:
            template = Template(template_fd.read())
    except IOError as err:
        logging.error("Could'nt load template file '%s': %s\n",
            template_file, err)
        parser.print_help()
        return IO_ERR_TEMPLATE
    else:
        logging.info("Loaded template file '%s'.", template_file)

    #2/3 common values (optional)
    if common_csv_file is None:
        common = {}
    else:
        try:
            with open(common_csv_file, 'r', encoding='utf-8') as common_fd:
                reader = csv.reader(common_fd)
                for index, row in enumerate(reader):
                    row = _strip_row(row)
                    if index == 0:
                        keys = row
                    else:
                        values = row
        except IOError as err:
            logging.error("Could'nt load common csv file '%s': %s\n",
                csv_file, err)
            parser.print_help()
            return IO_ERR_COMMON_CSV
        else:
            logging.info("Loaded csv common file '%s'.", common_csv_file)
            common = dict(zip(keys, values))

    if common:
        logging.debug("common values: %s", common)

    #3/3 enumerated values
    try:
        with open(csv_file, 'r', encoding='utf-8') as csv_fd:
            reader = csv.reader(csv_fd)
            for index, row in enumerate(reader):
                row = _strip_row(row)
                if index == 0:
                    header = row
                    continue
                logging.info("Got data for %s", " ".join(row[:2]))
                write_svg(row, template, output_prefix, header, common)
    except IOError as err:
        logging.error("Could'nt load csv file '%s': %s\n", csv_file, err)
        parser.print_help()
        return IO_ERR_CSV
    except MissingData:
        return DATA_ERR


def _analyse_cmd():
    """
    Parse CLI args
    """
    parser = argparse.ArgumentParser(description='Generates business cards.')
    parser.add_argument('--common-input', default=None,
        help='default: None. First line must contain template variables..')
    parser.add_argument('--input', default=DEFAULT_CSV,
        help='''default: data.csv. First line must contain template variables.
        Can override --common_input.
        Leave field blank in csv to use common if available.''')
    parser.add_argument('--output_prefix', default=DEFAULT_PREFIX)
    parser.add_argument('--template', default=DEFAULT_TEMPLATE)
    #http://stackoverflow.com/questions/6076690/ ...
    # ... verbose-level-with-argparse-and-multiple-v-options
    parser.add_argument('-v', action='append_const', const=1,
        help='increase verbosity. Up to 3 times -v or -vvv',
        default=[])
    return parser, parser.parse_args(sys.argv[1:])


def main():
    """module entry point"""
    argparser, argvalues = _analyse_cmd()
    sys.exit(process(argparser, vars(argvalues)))

if __name__ == '__main__':
    main()
