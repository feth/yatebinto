yatebinto
=========

Yet another templating engine but I needed this one

This is very suited for my SVG business cards.

Sample data
-----------

You can run fill_in.py from the source directory, after creating the expected 'generated' directory.

Like that::

        mkdir generated
        ./fill_in.py --input-common common.py

And then, look in generated (you can display svg files with inkscape or chromium or firefox!).


Usage
------

usage: fill_in.py [-h] [--common-input COMMON_INPUT] [--input INPUT]
                  [--output_prefix OUTPUT_PREFIX] [--template TEMPLATE] [-v]

Generates business cards.

optional arguments:
  -h, --help            show this help message and exit
  --common-input COMMON_INPUT
                        default: None. First line must contain template
                        variables..
  --input INPUT         default: data.csv. First line must contain template
                        variables. Can override --common_input. Leave field
                        blank in csv to use common if available.
  --output_prefix OUTPUT_PREFIX
  --template TEMPLATE
  -v                    increase verbosity. Up to 3 times -v or -vvv
