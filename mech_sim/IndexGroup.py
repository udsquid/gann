"""
Sub-group commands for index operations.

Usage:
    index product <symbol>
    index range (start | end) <date> [<time>]
    index range reset
    index status
    index (search | searchf) <operator> <value>
        [(and | or) <operator> <value>]
"""


#
# python libraries
#
import datetime


#
# 3-party libraries
#
from django.utils import timezone
from django.utils.dateparse import parse_datetime
import pytz


#
# project libraries
#
from history.models import *


#
# module classes
#
class IndexGroup():

    actions = ['product', 'range', 'status', 'search', 'searchf']
    symbol = None
    range_start = None
    range_end = None

    def __init__(self):
        products = ProductInfo.objects.all()
        self.symbols = [p.symbol for p in products]

    def complete_command(self, text, line, begin_index, end_index):
        if self.has_complete_action(line):
            return [text]
        elif not text:
            return self.actions
        else:
            completions = []
            for act in self.actions:
                if act.startswith(text):
                    completions.append(act)
            return completions

    def has_complete_action(self, line):
        for act in self.actions:
            act += ' '
            if act in line:
                return True
        return False

    def perform(self, arg):
        if arg['product']:
            self.set_product(arg['<symbol>'])
        elif arg['range']:
            self.set_range(arg)
        elif arg['status']:
            self.show_status()
        elif arg['search']:
            print 'do search...'
        elif arg['searchf']:
            print 'do searchf...'
        else:
            print "*** not supported"

    def set_product(self, symbol):
        if symbol not in self.symbols:
            print "*** unknown symbol: %s" % symbol
            return
        self.symbol = symbol

    def set_range(self, arg):
        if arg['reset']:
            self.range_start = None
            self.range_end = None
            return

        time_ = self._parse_datetime_arg(arg)
        if not time_:
            print "*** invalid date-time format"
            return
        if arg['start']:
            self.range_start = time_
        elif arg['end']:
            self.range_end = time_
        self._check_range()

    def _check_range(self):
        start = self.range_start
        end = self.range_end
        if not start or not end:
            return
        if self.range_start >= self.range_end:
            print "!!! WARNING: empty range"

    def _parse_datetime_arg(self, arg):
        date_ = arg['<date>']
        time_ = arg['<time>']
        if time_ == None:
            time_ = datetime.time.min
        datetime_str = '{} {}'.format(date_, time_)
        naive_datetime = parse_datetime(datetime_str)
        if not naive_datetime:
            return None
        curr_tz = timezone.get_current_timezone_name()
        local_time = pytz.timezone(curr_tz).localize(naive_datetime)
        return local_time

    def show_status(self):
        # calculate status title length for printing
        status_title = dict(
            symbol='Symbol',
            start='Range start',
            end='Range end',
            result='Search result',
        )
        item_len = [len(v) for v in status_title.values()]
        min_width = max(item_len)
        # print status
        time_format = "%Y-%m-%d %H:%M:%S"
        print "{symbol:>{width}}: {value}".format(value=self.symbol,
                                                  width=min_width,
                                                  **status_title)
        self._print_time(status_title['start'],
                         self.range_start,
                         min_width)
        self._print_time(status_title['end'],
                         self.range_end,
                         min_width)

    def _print_time(self, title, value, title_width):
        time_format = "%Y-%m-%d %H:%M:%S"
        if value:
            print "{title:>{width}}: {value:{format}}".format(
                title=title,
                width=title_width,
                value=value,
                format=time_format)
        else:
            print "{title:>{width}}: {value}".format(
                title=title,
                width=title_width,
                value=None)

    def do_search(self, arg):
        if not self._check_symbol():
            return

    def do_searchf(self, arg):
        if not self._check_symbol():
            return

    def _check_symbol(self):
        if self.symbol:
            return True
        else:
            print "*** no symbol specified, " + \
                "please use 'index product <symbol>' first"
            return False
