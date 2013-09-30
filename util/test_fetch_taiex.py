#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test functionalities of fetch_taiex.py.

Usage:
    test_fetch_taiex.py [--type=<type>]
    test_fetch_taiex.py -h | --help
    test_fetch_taiex.py -v | --version

Options:
    --type=<type>      Type of testing [default: unit-test].
    -h, --help         Show this screen.
    -v, --version      Show version.
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
### variables
###
test_result = dict( # p: pass; f:fail; n: not run; s: skip
    old = dict(regular = 'n', holiday = 'n'),
)


###
### unit test functions
###
def test_fetch_old_regular():
    try:
        print "\tFetching indexes in regular day.."
        result = fetch_single1(date(2000, 1, 4))
        check_list = [
            ('09:00', '8448.84'),
            ('09:01', '8644.91'),
            ('09:02', '8683.23')]
        for k, v in check_list:
            assert result[k] == v, \
                "index at '%s' should be '%s', not '%s'" % (k, v, result[k])
        return 'p'
    except Exception as e:
        print "** Error:", e
        return 'f'


def test_fetch_old_holiday():
    try:
        print "\tFetching indexes in holiday.."
        result = fetch_single1(date(2000, 1, 8))
        assert not result, "indexes in '2000-01-08' should be empty"
        return 'p'
    except Exception as e:
        print "** Error:", e
        return 'f'


def test_fetch_old():
    test_result['old']['regular'] = test_fetch_old_regular()
    test_result['old']['holiday'] = test_fetch_old_holiday()


###
### main procedure
###
if __name__ == '__main__':
    args = docopt(__doc__, version="test_fetch_taiex.py 1.0")
    print "Testing fetch from old site (every 1 minute).. "
    test_fetch_old()
    results = test_result['old'].values()
    print ""
    print "Pass: %d, Fail: %d, Skip: %d" % (results.count('p'),
                                            results.count('f'),
                                            results.count('s'))
    if results.count('p') == len(results):
        print "OK!"
    else:
        print "** Fail"
