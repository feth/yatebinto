yatebinto
=========

Yet another templating engine but I needed this one

This is very suited for my SVG business cards.

Dependencies
------------

Python 3.2. Period.

Sample data
-----------

You can run fill_in.py from the source directory, after creating the expected 'generated' directory.

Like that::

        mkdir generated
        ./fill_in.py --input-common common.py

And then, look in generated (you can display svg files with inkscape or chromium or firefox!).


Usage and more
--------------

I think I put it nicely together in the help message, but if you still havec questions, please let me know.

::

        $ ./fill_in.py -h
        usage: fill_in.py [-h] [--common-input COMMON_INPUT] [--input INPUT]
                  [--output_prefix OUTPUT_PREFIX] [--template TEMPLATE] [-v]

        This program generates enveloppes for mailings, business cards or whatever.
        ---------------------------------------------------------------------------

        It reads
         - a template file (for instance an SVG)
            in which field names are prefixed with '$'.
         - a CSV data file
            for every line of which a file will be generated.
         - (optional) a CSV default data file
            default values for the fields may the be specified there.

        optional arguments:
          -h, --help            show this help message and exit
          --common-input COMMON_INPUT
                                default: None. First line must contain template
                                variables.
          --input INPUT         default: data.csv. First line must contain template
                                variables. Can override --common_input. Leave field
                                blank in csv to use common if available.
          --output_prefix OUTPUT_PREFIX
          --template TEMPLATE
          -v                    increase verbosity. Up to 3 times -v or -vvv

        Return codes:
            0: success
            1: error reading the template
            2: error reading csv individual data
            3: error reading csv common data
            4: error in data (missing data for a field for instance)

        Distribution and usage under WTFPL (see COPYING).

        See README.rst for more information.

