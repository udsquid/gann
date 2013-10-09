#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verify tool for util/fetch_taiex.py-fetch_single2.

Usage:
    fetch_taiex_single2.py [--start=<start>] [--end=<end>]
    fetch_taiex_single2.py -h | --help
    fetch_taiex_single2.py -v | --version

Options:
    -h, --help         Show this screen.
    -v, --version      Show version.
    --start=<start>    Fetch start date [default: 2004-10-15]
    --end=<end>        Fetch end date [default: 2011-01-15]
"""

###
### project libraries
###
from util.fetch_taiex import *


###
### main procedure
###
if __name__ == '__main__':
    args = docopt(__doc__, version="fetch_taiex_single2.py 1.0")
