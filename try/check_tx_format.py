#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Used to check the records format of Taiwan future indexes files.

Usage:
    check_tx_format.py -f <file>
    check_tx_format.py -d <directory>
"""

#
# python libraries
#
import fnmatch
import os
import re


#
# 3-party libraries
#
from docopt import docopt


#
# main procedure
#
fmt = r"""
    (?P<date>\d{4}(/\d{1,2}){2}),    # date
    (?P<time>\d{2}:\d{2}),           # time
    (?P<open>\d{,5}),                # open price
    (?P<high>\d{,5}),                # highest price
    (?P<low>\d{,5}),                 # lowest price
    (?P<close>\d{,5}),               # close price"""


def check_file(record_file):
    with open(record_file) as f:
        match_count = 0
        for r in f.readlines():
            assert re.match(fmt, r, re.VERBOSE), \
                "not match: %s" % r
            match_count += 1
        base_name = os.path.basename(record_file)
        print "%s: matched %d records" % (base_name, match_count)


option = docopt(__doc__)
if option['-f']:
    record_file = option['<file>']
    check_file(record_file)
elif option['-d']:
    record_dir = option['<directory>']
    for file in os.listdir(record_dir):
        if fnmatch.fnmatch(file, '*.txt'):
            record_file = os.path.join(record_dir, file)
            check_file(record_file)
