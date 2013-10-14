#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""TAIEX fetch tool.

Usage:
    fetch_taiex.py [--start=<start>] [--end=<end>]
    fetch_taiex.py -h | --help
    fetch_taiex.py -v | --version

Options:
    -h, --help         Show this screen.
    -v, --version      Show version.
    --start=<start>    The start date to fetch data [default: 2000-01-04].
    --end=<end>        The end date to fetch data, default is today.
"""

###
### python libraries
###
from datetime import date, datetime, timedelta
from docopt import docopt
from pyquery import PyQuery
from urllib import urlencode
import pytz
import re
import requests


###
### django libraries
###
from django.utils.dateparse import parse_datetime


###
### project libraries
###
from history import models as MD


###
### constants
###
ONE_DAY = timedelta(1)

# --- error codes ---
ERROR_INVALID_PARAMETER = 1


###
### helper functions
###
def normalize_date(d):
    pattern = '(?P<year>\d{4})[-/](?P<month>\d{1,2})[-/](?P<day>\d{1,2})'
    match = re.search(pattern, d)
    if not match:
        print "*** Error: date format [%s] is not valid" % d
        exit(ERROR_INVALID_PARAMETER)
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


def decode_page(content):
    return content.encode('raw_unicode_escape').decode('big5')


def is_holiday(data):
    return u'查無資料' in data('body').text()


def fetch_single1(day, cfg):
    # fetch
    url = 'http://www.twse.com.tw/ch/trading/exchange/MI_5MINS_INDEX/MI_5MINS_INDEX_oldtsec.php'
    param = dict(input_date = convert_date(day))
    resp = requests.post(url, param)
    # parse
    data = PyQuery(decode_page(resp.text))
    if is_holiday(data):
        return None
    _times = data('tr > td.AS2')
    _indexes = _times.next('td')
    times = _times.text().split()
    indexes = [i.replace(',', '') for i in _indexes.text().split()]
    assert len(times) == len(indexes), \
        "number of times and indexes are not match"
    return dict(zip(times, indexes))


def fetch_single2(day, cfg):
    # fetch
    url = 'http://www.twse.com.tw/ch/trading/exchange/MI_5MINS_INDEX/genpage/Report{year}{month:02d}/A121{year}{month:02d}{day:02d}.php?chk_date={taiex_date}'.format(year=day.year, month=day.month, day=day.day, taiex_date=convert_date(day))
    resp = requests.get(url)
    # parse
    data = PyQuery(decode_page(resp.text))
    if is_holiday(data):
        return None
    table = data(cfg['format']['table'])
    _times = table(cfg['format']['times']).text().split()
    _indexes = _times.next('td')
    times = [t.text for t in _times[1:]]
    indexes = [i.text.replace(',', '') for i in _indexes[1:]]
    assert len(times) == len(indexes), \
        "number of times and indexes are not match"
    return dict(zip(times, indexes))


def fetch_single3(day, cfg):
    # fetch
    url = 'http://www.twse.com.tw/ch/trading/exchange/MI_5MINS_INDEX/genpage/Report{year}{month:02d}/A121{year}{month:02d}{day:02d}.php?chk_date={taiex_date}'.format(year=day.year, month=day.month, day=day.day, taiex_date=convert_date(day))
    resp = requests.get(url)
    # parse
    data = PyQuery(decode_page(resp.text))
    if is_holiday(data):
        return None
    fmt1 = data('table.board_trad')
    fmt2 = data('div#tbl-container')
    if fmt1:
        _times = fmt1('tr[bgcolor="#FFFFFF"] > td:first-child').text().split()
        pass
    elif fmt2:
        pass
    else:
        assert False, "no suitable parser"
    _times = data('tr.basic2 > td:first-child')
    _indexes = _times.next('td')
    times = [t.text for t in _times[1:]]
    indexes = [i.text.replace(',', '') for i in _indexes[1:]]
    assert len(times) == len(indexes), \
        "number of times and indexes are not match"
    return dict(zip(times, indexes))


def save(data, day):
    if not data:
        return
    for time, index in data.iteritems():
        rec = MD.Taiex()
        naive = parse_datetime("%s %s" % (day, time))
        rec.time = pytz.timezone('Asia/Taipei').localize(naive)
        rec.price = index
        rec.save()


def fetch(start, end, cfg):
    LOWER = cfg['lower']
    UPPER = cfg['upper']
    ffunc = cfg['fetch']
    # adjust date boundaries
    if start > UPPER or end < LOWER:
        # not in this range
        return
    start = max(start, LOWER)
    end = min(end, UPPER)
    # start fetching daily data
    for day in days_range(start, end):
        print "Fetching %s.." % day
        data = ffunc(day, cfg)
        save(data, day)


###
### main procedure
###
"""
TAIEX data can be divided into following parts:
1. 2000-01-04 ~ 2004-10-14: on old site, every 1 minute
2. 2004-10-15 ~ 2005-12-31: on new site, every 1 minute (layout 1)
3. 2006-01-01 ~ 2011-01-15: on new site, every 1 minute (layout 2)
4. 2011-01-16 ~ now       : on new site, every 15 seconds
"""
FETCH_CONFIG = {
    'old': {
        'lower': date(2000, 1, 4),
        'upper': date(2004, 10, 14),
        'fetch': fetch_single1,
    },
    'new-1min-1': {
        'lower': date(2004, 10, 15),
        'upper': date(2005, 12, 31),
        'fetch': fetch_single2,
        'format': {
            'table': 'table.board_trad',
            'times': 'tr[bgcolor="#FFFFFF"] > td:first-child',
            'indexes': 'tr[bgcolor="#FFFFFF"] > td:first-child + td',
        },
    },
    'new-1min-2': {
        'lower': date(2006, 1, 1),
        'upper': date(2011, 1, 15),
        'fetch': fetch_single3,
    },
    'new-15sec': {
        'lower': None,
        'upper': None,
        'fetch': None,
    },
}

if __name__ == '__main__':
    args = docopt(__doc__, version="fetch_taiex 1.0")
    # setup date range
    start = normalize_date(args['--start'])
    if args['--end']:
        end = normalize_date(args['--end'])
    else:
        end = date.today()
    assert start <= end, "date range is not valid"
    # get daily data from specified range
    print "Fetching TAIEX from [%s] to [%s].. " % (start, end)
    fetch(start, end, FETCH_CONFIG['old'])
    fetch(start, end, FETCH_CONFIG['new-1min-1'])
    fetch(start, end, FETCH_CONFIG['new-1min-2'])
    print "done!"
