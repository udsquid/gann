#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Read records from TX files and push them into Django database.

Usage:
    push_tx_to_db.py -d <path>
    push_tx_to_db.py -f <file>

Options:
    -h, --help    Show this screen.
    -d            TX data path.
    -f            TX data file.
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
from django.utils.dateparse import parse_datetime
from docopt import docopt
import pytz


#
# project libraries
#
import history.models as MD


#
# main procedure
#
def search_record_files(path):
    record_files = []
    for _file in os.listdir(path):
        if fnmatch.fnmatch(_file, '*.txt'):
            full_path = os.path.join(path, _file)
            record_files.append(full_path)
    return record_files


def convert_time(date, time):
    date = date.replace('/', '-')
    time_str = '%s %s' % (date, time)
    naive_time = parse_datetime(time_str)
    aware_time = pytz.timezone('Asia/Taipei').localize(naive_time)
    return aware_time


def parse_as_model(raw_record):
    fmt = r"""
        (?P<date>\d{4}(/\d{1,2}){2}),    # date
        (?P<time>\d{2}:\d{2}),           # time
        (?P<open>\d{,5}),                # open price
        (?P<high>\d{,5}),                # highest price
        (?P<low>\d{,5}),                 # lowest price
        (?P<close>\d{,5}),               # close price
        """
    match_result = re.match(fmt, raw_record, re.VERBOSE)
    rec_info = match_result.groupdict()
    new_rec = MD.Tx()
    new_rec.time = convert_time(rec_info['date'],
                                rec_info['time'])
    new_rec.open = rec_info['open']
    new_rec.high = rec_info['high']
    new_rec.low = rec_info['low']
    new_rec.close = rec_info['close']
    return new_rec


def push_records(record_file):
    print "Processing [%s].. " % record_file
    with open(record_file) as f:
        for line in f.readlines():
            rec = parse_as_model(line)
            rec.save()


option = docopt(__doc__)
if option['-d']:
    data_path = option['<path>']
    record_files = search_record_files(data_path)
    for f in record_files:
        push_records(f)
elif option['-f']:
    data_file = option['<file>']
    push_records(data_file)
