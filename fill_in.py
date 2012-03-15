#!/usr/bin/python3

"""
Business card generator
Call me from command line
"""

RETURN_CODES = IO_ERR_TEMPLATE, IO_ERR_CSV = 0, 1


LOGFORMAT = "[%(levelname)-10s] %(message)s"
import logging
logging.basicConfig(level=logging.INFO, format=LOGFORMAT)
import sys
try:
    import argparse
except ImportError:
    logging.exception("""*** Unable to import *argparse*. \
Maybe install python-argpase. Exiting with status 2.***""")
    sys.exit(2)

from itertools import islice
#cf bug http://www.logilab.org/ticket/2481
# pylint: disable=W0402
from string import Template
import csv

# indexes:
FIRSTNAME, NAME, STREET, POSTCODE, CITY, TEL = tuple(range(6))

# punchline
PUNCHLINE = "Audit/Conseil IT, Formation, Développement"

#defaults
DEFAULT_TEMPLATE = "template/template.svg"
DEFAULT_PREFIX = "generated/business_cards"
DEFAULT_CSV = "data.csv"


def write_svg(row, template, out_prefix):
    """
    for every parsed csv row, spits a file
    """
    out_name = '%s.svg' % '_'.join((out_prefix, row[FIRSTNAME], row[NAME]))

    with open(out_name, 'w', encoding='utf-8') as out:
        replacements = {
            'Initiales': '.'.join(item[0].lower() for item in row[:STREET]),
            'NumDeTel': row[TEL],
            'NumRueVille': '{0} - {1} {2}'.format(*row[STREET:TEL]),
            'PrenomNOM': ' '.join((row[FIRSTNAME], row[NAME].upper())),
            'Punchline' : PUNCHLINE,
            }
        out.write(template.substitute(replacements))
        logging.info("Wrote file: %s", out_name)


def main(parser, values):
    """
    Give it a dict with information, does the job.
    There are defaults.
    Expected in the dict (but defaults are ok):
    * template_file: svg file name, file has $variables in it
    * csv_file: data in columns:
        FIRSTNAME, NAME, STREET, POSTCODE, CITY, TEL
    * output_prefix: we'll spit out files named like this
    """
    template_file = values.get('template', DEFAULT_TEMPLATE)
    csv_file = values.get('csv_file', DEFAULT_CSV)
    output_prefix = values.get('output_prefix', DEFAULT_PREFIX)

    try:
        with open(template_file, 'r', encoding='utf-8') as template_fd:
            template = Template(template_fd.read())
    except IOError as err:
        logging.error("Could'nt load template file '%s': %s\n", template_file, err)
        parser.print_help()
        return IO_ERR_TEMPLATE
    else:
        logging.info("Loaded template file '%s'.", template_file)

    try:
        with open(csv_file, 'r', encoding='utf-8') as csv_fd:
            reader = csv.reader(csv_fd)
            for row in islice(reader, 1, None):  # skip 1st (title) row
                logging.info("Got data for %s", " ".join(row[:2]))
                write_svg(row, template, output_prefix)
    except IOError as err:
        logging.error("Could'nt load csv file '%s': %s\n", csv_file, err)
        parser.print_help()
        return IO_ERR_CSV


def _analyse_cmd():
    """
    Parse CLI args
    """
    parser = argparse.ArgumentParser(description='Generates business cards.')
    parser.add_argument('--input', default=DEFAULT_CSV,
        help='default: data.csv')
    parser.add_argument('--output_prefix', default=DEFAULT_PREFIX)
    parser.add_argument('--template', default=DEFAULT_TEMPLATE)
    return parser, parser.parse_args(sys.argv[1:])


if __name__ == '__main__':
    parser, values = _analyse_cmd()
    sys.exit(main(parser, vars(values)))
