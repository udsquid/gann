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
    phase1 = dict(regular = 'n', holiday = 'n'),
    phase2 = dict(regular = 'n', holiday = 'n'),
    phase3 = dict(regular = 'n', holiday = 'n'),
)


###
### unit test functions
###
def test_fetch_phase1_regular():
    try:
        print "\tTesting data in regular day.."
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
        print "** Error:", e.__class__, e
        return 'f'


def test_fetch_phase1_holiday():
    try:
        print "\tTesting data in holiday.."
        result = fetch_single1(date(2000, 1, 8))
        assert not result, "indexes in '2000-01-08' should be empty"
        return 'p'
    except Exception as e:
        print "** Error:", e.__class__, e
        return 'f'


def test_fetch_phase1():
    test_result['phase1']['regular'] = test_fetch_phase1_regular()
    test_result['phase1']['holiday'] = test_fetch_phase1_holiday()


def test_fetch_phase2_regular():
    try:
        print "\tTesting data in regular day.."
        result = fetch_single2(date(2004, 10, 15))
        check_list = [
            ('9:00', '5831.07'),
            ('9:01', '5817.81'),
            ('9:02', '5811.69')]
        for k, v in check_list:
            assert result[k] == v, \
                "index at '%s' should be '%s', not '%s'" % (k, v, result[k])
        return 'p'
    except Exception as e:
        print "** Error:", e.__class__, e
        return 'f'


def test_fetch_phase2_holiday():
    try:
        print "\tTesting data in holiday.."
        result = fetch_single2(date(2004, 10, 16))
        assert not result, "indexes in '2004-10-16' should be empty"
        return 'p'
    except Exception as e:
        print "** Error:", e.__class__, e
        return 'f'


def test_fetch_phase2():
    test_result['phase2']['regular'] = test_fetch_phase2_regular()
    test_result['phase2']['holiday'] = test_fetch_phase2_holiday()


def test_fetch_phase3_regular():
    try:
        print "\tTesting data in regular day.."
        result = fetch_single3(date(2006, 1, 2))
        check_list = [
            ('9:00', '6548.34'),
            ('9:01', '6457.61'),
            ('9:02', '6452.82')]
        for k, v in check_list:
            assert result[k] == v, \
                "index at '%s' should be '%s', not '%s'" % (k, v, result[k])
        return 'p'
    except Exception as e:
        print "** Error:", e.__class__, e
        print result
        return 'f'


def test_fetch_phase3_holiday():
    try:
        print "\tTesting data in holiday.."
        result = fetch_single3(date(2006, 1, 7))
        assert not result, "indexes in '2006-01-07' should be empty"
        return 'p'
    except Exception as e:
        print "** Error:", e.__class__, e
        return 'f'


def test_fetch_phase3():
    test_result['phase3']['regular'] = test_fetch_phase3_regular()
    test_result['phase3']['holiday'] = test_fetch_phase3_holiday()


def print_summary():
    results = test_result['phase1'].values() + \
              test_result['phase2'].values() + \
              test_result['phase3'].values()
    print ""
    print "Pass: %d, Fail: %d, Skip: %d" % (results.count('p'),
                                            results.count('f'),
                                            results.count('n'))
    if results.count('f'):
        print "** Fail"
    else:
        print "OK!"


###
### main procedure
###
if __name__ == '__main__':
    args = docopt(__doc__, version="test_fetch_taiex.py 1.0")
    print "Testing fetch data in phase 1.. "
    test_fetch_phase1()
    print "Testing fetch data in phase 2.. "
    test_fetch_phase2()
    print "Testing fetch data in phase 3.. "
    test_fetch_phase3()
    print_summary()
