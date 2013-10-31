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
    --start=<start>    The start date to fetch data [default: 2000-01-01].
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
# --- common ---
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
    return u'查無資料' in data('body').text() or \
        '404 Not Found' in data.text()


def in_range(day, phase):
    assert phase in FETCH_CONFIG, \
        "invalid phase name [%s]" % phase
    lower = FETCH_CONFIG[phase]['lower']
    upper = FETCH_CONFIG[phase]['upper']
    return day >= lower and day <= upper


def fetch_single(day):
    if in_range(day, 'phase-1'):
        url = 'http://www.twse.com.tw/ch/trading/exchange/MI_5MINS_INDEX/MI_5MINS_INDEX_oldtsec.php'
        param = dict(input_date = convert_date(day))
        resp = requests.post(url, param)
    elif in_range(day, 'phase-2') or \
         in_range(day, 'phase-3') or \
         in_range(day, 'phase-4'):
        url = 'http://www.twse.com.tw/ch/trading/exchange/MI_5MINS_INDEX/genpage/Report{year}{month:02d}/A121{year}{month:02d}{day:02d}.php?chk_date={taiex_date}'.format(year=day.year, month=day.month, day=day.day, taiex_date=convert_date(day))
        resp = requests.get(url)
    return PyQuery(decode_page(resp.text))


def parse_times(day, data):
    if in_range(day, 'phase-1'):
        return data('tr > td.AS2').text().split()
    elif in_range(day, 'phase-2'):
        cfg = FETCH_CONFIG['phase-2']
        table = data(cfg['format']['table'])
        return table(cfg['format']['times']).text().split()
    elif in_range(day, 'phase-3'):
        cfg = FETCH_CONFIG['phase-3']
        table = data(cfg['format']['table'])
        return table(cfg['format']['times']).text().split()
    elif in_range(day, 'phase-4'):
        cfg = FETCH_CONFIG['phase-4']
        table = data(cfg['format']['table'])
        return table(cfg['format']['times']).text().split()


def parse_indexes(day, data):
    if in_range(day, 'phase-1'):
        _times = data('tr > td.AS2')
        _indexes = _times.next('td')
        return [i.replace(',', '') for i in _indexes.text().split()]
    elif in_range(day, 'phase-2'):
        cfg = FETCH_CONFIG['phase-2']
        table = data(cfg['format']['table'])
        _indexes = table(cfg['format']['indexes']).text().split()
        return [i.replace(',', '') for i in _indexes]
    elif in_range(day, 'phase-3'):
        cfg = FETCH_CONFIG['phase-3']
        table = data(cfg['format']['table'])
        _indexes = table(cfg['format']['indexes']).text().split()
        return [i.replace(',', '') for i in _indexes]
    elif in_range(day, 'phase-4'):
        cfg = FETCH_CONFIG['phase-4']
        table = data(cfg['format']['table'])
        _indexes = table(cfg['format']['indexes']).text().split()
        return [i.replace(',', '') for i in _indexes]


def parse(day, data):
    times = parse_times(day, data)
    indexes = parse_indexes(day, data)
    assert len(times) == len(indexes), \
        "number of times and indexes are not match"
    return dict(zip(times, indexes))


def save(day, data):
    if not data:
        return
    for time, index in data.iteritems():
        rec = MD.Taiex()
        naive = parse_datetime("%s %s" % (day, time))
        rec.time = pytz.timezone('Asia/Taipei').localize(naive)
        rec.price = index
        rec.save()


def fetch(start, end):
    for day in days_range(start, end):
        print "Fetching %s.. " % day,
        data = fetch_single(day)
        if is_holiday(data):
            print "holiday, skip!"
            continue
        indexes = parse(day, data)
        save(day, indexes)
        print ""


###
### main procedure
###
"""
The data history of TAIEX can be divided into following phases:
1. 2000-01-01 ~ 2004-10-14: on old site, every 1 minute
2. 2004-10-15 ~ 2005-12-31: on new site, every 1 minute (layout 1)
3. 2006-01-01 ~ 2011-01-15: on new site, every 1 minute (layout 2)
4. 2011-01-16 ~ now       : on new site, every 15 seconds
"""
FETCH_CONFIG = {
    'phase-1': {
        'lower': date(2000, 1, 1),
        'upper': date(2004, 10, 14),
    },
    'phase-2': {
        'lower': date(2004, 10, 15),
        'upper': date(2005, 12, 31),
        'format': {
            'table': 'table.board_trad',
            'times': 'tr[bgcolor="#FFFFFF"] > td:first-child',
            'indexes': 'tr[bgcolor="#FFFFFF"] > td:first-child + td',
        },
    },
    'phase-3': {
        'lower': date(2006, 1, 1),
        'upper': date(2011, 1, 15),
        'format': {
            'table': 'div#tbl-container',
            'times': 'tr[align="right"] > td:first-child',
            'indexes': 'tr[align="right"] > td:first-child + td',
        },
    },
    'phase-4': {
        'lower': date(2011, 01, 16),
        'upper': date.today(),
        'format': {
            'table': 'div#tbl-container',
            'times': 'tr[align="right"] > td:first-child',
            'indexes': 'tr[align="right"] > td:first-child + td',
        },
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
    fetch(start, end)
    print "done!"
