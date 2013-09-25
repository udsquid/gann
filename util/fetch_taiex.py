#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""TAIEX fetch tool.

Usage:
    fetch_taiex.py [--start=<start>] [--end=<end>]
    fetch_taiex.py (-h | --help)
    fetch_taiex.py (-v | --version)

Options:
    -h, --help         Show this screen.
    -v, --version      Show version.
    --start=<start>    The start date to fetch data [default: 2000-01-04].
    --end=<end>        The end date to fetch data, default is today.
"""

###
### python libraries
###
from datetime import date, timedelta
from docopt import docopt
from pyquery import PyQuery
from urllib import urlencode
import re
import requests


###
### project libraries
###
from history import models as MD


###
### constants
###
ONE_DAY = timedelta(1)


###
### helper functions
###
def normalize_date(d):
    pattern = '(?P<year>\d{4})[-/](?P<month>\d{1,2})[-/](?P<day>\d{1,2})'
    match = re.search(pattern, d)
    if not match:
        print "*** Error: date format [%s] is not valid" % d
        exit(1)
    year, month, day = match.groups()
    return date(int(year), int(month), int(day))


def days_range(start, end):
    cur = start
    while cur <= end:
        yield cur
        cur += ONE_DAY


def convert_date(d):
    """Convert the given date to the TAIEX format."""
    return '%d/%#02d/%#02d' % (d.year-1911, d.month, d.day)


def fetch_single1(date):
    # fetch
    url = 'http://www.twse.com.tw/ch/trading/exchange/MI_5MINS_INDEX/MI_5MINS_INDEX_oldtsec.php'
    param = dict(input_date = convert_date(date))
    resp = requests.post(url, param)
    # parse
    data = PyQuery(resp.text.encode('raw_unicode_escape').decode('big5'))
    if u'查無資料' in data('body').text():
        # no data today
        return None
    _times = data('tr > td.AS2')
    _indexes = _times.next('td')
    times = _times.text().split()
    indexes = [i.replace(',', '') for i in _indexes.text().split()]
    assert len(times) == len(indexes), \
        "number of times and indexes are not match"
    return dict(zip(times, indexes))


def save(data, day):
    if not data:
        return
    for time, index in data.iteritems():
        rec = MD.Taiex()
        rec.time = '%s %s' % (day, time)
        rec.price = index
        if time == '09:00':
            print rec.time
            print rec.price


###
### main procedure
###
def fetch_old(start, end):
    # setup date boundaries
    LOWER = date(2000, 1, 4)
    UPPER = date(2004, 10, 14)
    if start > UPPER or end < LOWER:
        return
    start = max(start, LOWER)
    end = min(end, UPPER)
    # start fetching daily data
    for day in days_range(start, end):
        print "Fetching %s.." % day
        data = fetch_single1(day)
        save(data, day)


def fetch(start, end):
    """Fetch TAIEX data.

    TAIEX data can be divided into 3 parts:
    1. 2000-01-04 ~ 2004-10-14: on old site, every 1 minute
    2. 2004-10-15 ~ 2011-01-15: on new site, every 1 minute
    3. 2011-01-16 ~ now       : on new site, every 15 seconds
    """
    print "Fetching TAIEX from [%s] to [%s].. " % (start, end)
    fetch_old(start, end)
    # fetch_new_1min(start, end)
    print "done!"


if __name__ == '__main__':
    args = docopt(__doc__, version="fetch_taiex 1.0")
    # get daily data from specified region
    start = normalize_date(args['--start'])
    if args['--end']:
        end = normalize_date(args['--end'])
    else:
        end = date.today()
    assert start <= end, "date range is not valid"
    fetch(start, end)
