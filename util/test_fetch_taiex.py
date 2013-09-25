#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test functionalities of fetch_taiex.py.

Usage:
    test_fetch_taiex.py --unit-test
    test_fetch_taiex.py (-h | --help)
    test_fetch_taiex.py (-v | --version)

Options:
    -h, --help         Show this screen.
    -v, --version      Show version.
    --unit-test        Test basic functions of fetch_taiex.py.
"""

###
### python libraries
###
from docopt import docopt


###
### project libraries
###
from fetch_taiex import *


###
### unit test functions
###
def test_fetch_old():
    r1 = fetch_single1(date(2000, 1, 4))
    assert r1['09:00'] == '8448.84', \
        "index at '09:00' should be '8448.84', not '%s'" % r1['09:00']
    assert r1['09:01'] == '8644.91', \
        "index at '09:01' should be '8644.91', not '%s'" % r1['09:01']
    assert r1['09:02'] == '8683.23', \
        "index at '09:02' should be '8683.23', not '%s'" % r1['09:02']
    r2 = fetch_single1(date(2000, 1, 8))
    assert not r2, "indexes in '2000-01-08' should be empty"


###
### main procedure
###
if __name__ == '__main__':
    args = docopt(__doc__, version="test_fetch_taiex.py 1.0")
    if args['--unit-test']:
        print "Testing fetch from old site (every 1 minute).. "
        test_fetch_old()
        print "OK"
