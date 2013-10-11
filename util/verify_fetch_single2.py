#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verify tool for fetch_taiex.py -- fetch_single2.

Usage:
    verify_fetch_single2.py verify [--start=<start>] [--end=<end>]
    verify_fetch_single2.py count (total | trade | holiday)
    verify_fetch_single2.py -h | --help
    verify_fetch_single2.py -v | --version

Options:
    -h, --help         Show this screen.
    -v, --version      Show version.
    --start=<start>    Fetch start date [default: 2004-10-15]
    --end=<end>        Fetch end date [default: 2011-01-15]
"""

###
### project libraries
###
from fetch_taiex import *


###
### contants
###
ERROR_INVALID_ARGUMENT = 1


###
### helper functions
###
def setup_date_boundaries(start, end):
    LOWER = date(2004, 10, 15)
    UPPER = date(2011, 1, 15)
    if start > UPPER or end < LOWER:
        return None, None
    start = max(start, LOWER)
    end = min(end, UPPER)
    return start, end


###
### test functions
###
def verify_html(start, end):
    """Verify the HTML structure day by day are keep the same."""
    print "Verifying.. "
    for day in days_range(start, end):
        url = 'http://www.twse.com.tw/ch/trading/exchange/MI_5MINS_INDEX/genpage/Report{year}{month:02d}/A121{year}{month:02d}{day:02d}.php?chk_date={taiex_date}'.format(year=day.year, month=day.month, day=day.day, taiex_date=convert_date(day))
        resp = requests.get(url)
        data = PyQuery(decode_page(resp.text))


def count_total(start, end):
    return (end - start).days + 1


def count_trade(start, end):
    return 0


def count_holiday(start, end):
    return 0


###
### main procedure
###
if __name__ == '__main__':
    args = docopt(__doc__, version="fetch_taiex_single2.py 1.0")
    # setup the date range
    start = normalize_date(args['--start'])
    end = normalize_date(args['--end'])
    start, end = setup_date_boundaries(start, end)
    if not start or not end:
        print "*** Error: Date range is not correct!"
        exit(ERROR_INVALID_ARGUMENT)
    # start verifying
    if args['verify']:
        verify_html(start, end)
    elif args['count']:
        if args['total']:
            n = count_total(start, end)
            print "# of days: %d" % n
        elif args['trade']:
            n = count_trade(start, end)
            print "# of trading days: %d" % n
        elif args['holiday']:
            n = count_holiday(start, end)
            print "# of holidays: %d" % n
