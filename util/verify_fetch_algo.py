#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verify tool for fetch_taiex.py -- fetch_single2.

Usage:
    verify_fetch_algo.py verify html [--start=<start>] [--end=<end>] [--verbose]
    verify_fetch_algo.py count days [--start=<start>] [--end=<end>]
    verify_fetch_algo.py -h | --help
    verify_fetch_algo.py -v | --version

Options:
    -h, --help         Show this screen.
    -v, --version      Show version.
    --start=<start>    Fetch start date [default: 2000-01-01]
    --end=<end>        Fetch end date, default is today.
    --verbose          Product verbose output.
"""

###
### python libraries
###
import re


###
### project libraries
###
from fetch_taiex import *


###
### test functions
###
def verify_html(start, end, args):
    """Verify the HTML structures day by day are keep the same."""
    flag = start.replace(year=start.year-1, month=1, day=1)
    for day in days_range(start, end):
        # show progress by year
        if flag.year != day.year:
            print "[%s] Verifying HTML in %d.." % \
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 day.year)
            flag = day
        # verify time data in each trading day
        data = fetch_single(day)
        if is_holiday(data):
            continue
        times = parse_times(day, data)
        indexes = parse_indexes(day, data)
        if args['--verbose']:
            print "[%s %s] %s" % (day, times[0], indexes[0])
        if not re.match(r'0?9:00(:00)?', times[0]) or \
           not re.match(r'\d{4,5}\.\d{2}', indexes[0]):
            print "Verify success until %s" % day
            return
    print "OK!"


def count_days(start, end):
    total = (end - start).days + 1
    trade = holiday = 0
    flag = start.replace(year=start.year-1, month=1, day=1)
    for day in days_range(start, end):
        # show progress by year
        if flag.year != day.year:
            print "[%s] Counting days in %d.." % \
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 day.year)
            flag = day
        # count trading days and holidays
        data = fetch_single(day)
        if is_holiday(data):
            holiday += 1
        else:
            times = parse_times(day, data)
            if re.match(r'0?9:00(:00)?', times[0]):
                trade += 1
    # do sanity check
    assert total == (trade + holiday), \
        "days number are not match"
    # print result
    print "Total: %d, trade: %d, holiday: %d" % (total, trade, holiday)


###
### main procedure
###
if __name__ == '__main__':
    args = docopt(__doc__, version="fetch_taiex_single2.py 1.0")
    # setup date range
    start = normalize_date(args['--start'])
    if args['--end']:
        end = normalize_date(args['--end'])
    else:
        end = date.today()
    assert start <= end, "date range is not valid"
    # start verifying
    print "Verifying from [%s] to [%s].. " % (start, end)
    if args['verify']:
        verify_html(start, end, args)
    elif args['count']:
        if args['days']:
            count_days(start, end)
