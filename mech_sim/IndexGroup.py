"""
Sub-group commands for index operations.

Usage:
    index product <symbol>
    index range (start | end) <date> [<time>]
    index range reset
    index status
    index (search | searchf) <operator> <value>
        [((and | or) <operator> <value>)]
"""


#
# python libraries
#
from datetime import datetime, time, timedelta


#
# 3-party libraries
#
from django.db.models import Q
from django.utils import timezone
from django.utils.dateparse import date_re, datetime_re
from django.utils.dateparse import parse_date, parse_datetime
import pytz


#
# project libraries
#
from history.models import *


#
# module classes
#
class IndexGroup(object):

    actions = ['product', 'range', 'status', 'search', 'searchf']
    symbol = None
    range_start = None
    range_end = None
    time_format = "%Y-%m-%d %H:%M:%S"

    def __init__(self):
        products = ProductInfo.objects.all()
        self.symbols = [p.symbol for p in products]
        self._range_start2 = None
        self._range_end2 = None
        self._first_match = None

    @property
    def first_match(self):
        return self._first_match

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
            symbol = arg['<symbol>'].upper()
            self.set_product(symbol)
        elif arg['range']:
            if arg['reset']:
                self.reset_range()
            else:
                self.set_range(arg)
        elif arg['status']:
            self.show_status()
        elif arg['search']:
            self.do_search(arg)
        elif arg['searchf']:
            self.do_searchf(arg)
        else:
            print "*** not supported"

    def set_product(self, symbol):
        if symbol not in self.symbols:
            print "*** unknown symbol: %s" % symbol
            return

        self.symbol = symbol
        if self.symbol == 'TAIEX':
            self.product = Taiex.objects
        elif self.symbol == 'TX':
            self.product = Tx.objects

    def set_range(self, arg):
        time_ = self._parse_datetime_arg(arg)
        if not time_:
            print "*** invalid date-time format"
            return
        if arg['start']:
            self.range_start = time_
        elif arg['end']:
            self.range_end = time_
        self._check_range()

    def reset_range(self):
        self.range_start = None
        self.range_end = None

    @property
    def range_start2(self):
        return self._range_start2

    @range_start2.setter
    def range_start2(self, value):
        if value is None:
            self.range_start2 = None
        elif isinstance(value, (str, unicode)):
            naive_datetime = self._parse_datetime(value)
            if not naive_datetime:
                raise ValueError("*** invalid date-time format")
            self._range_start2 = self._to_aware(naive_datetime)
        elif isinstance(value, datetime):
            self._range_start2 = self._to_local(value)

    @property
    def range_end2(self):
        return self._range_end2

    @range_end2.setter
    def range_end2(self, value):
        if value is None:
            self.range_end2 = None
        elif isinstance(value, (str, unicode)):
            naive_datetime = self._parse_datetime(value)
            if not naive_datetime:
                raise ValueError("*** invalid date-time format")
            self._range_end2 = self._to_aware(naive_datetime)
        elif isinstance(value, datetime):
            self._range_end2 = self._to_local(value)

    def check_range(self):
        start = self.range_start2
        end = self.range_end2
        if not start or not end:
            return True
        elif start < end:
            return True
        else:
            return False

    def _parse_datetime(self, value):
        if date_re.match(value):
            date_obj = parse_date(value)
            return datetime.combine(date_obj, time.min)
        elif datetime_re.match(value):
            return parse_datetime(value)
        else:
            return None

    def _to_aware(self, naive):
        curr_tz = timezone.get_current_timezone_name()
        return pytz.timezone(curr_tz).localize(naive)

    def _to_local(self, datetime_obj):
        curr_tz = timezone.get_current_timezone()
        return datetime_obj.astimezone(curr_tz)

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
        if time_ is None:
            time_ = time.min
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
        self.time_format = "%Y-%m-%d %H:%M:%S"
        if value:
            print "{title:>{width}}: {value:{format}}".format(
                title=title,
                width=title_width,
                value=value,
                format=self.time_format)
        else:
            print "{title:>{width}}: {value}".format(
                title=title,
                width=title_width,
                value=None)

    def filter_history(self, arg):
        history = self.product.order_by('time')
        history = self._set_time_filters(history)
        if self.symbol in ['TX']:
            history = self._set_k_bar_filter(history, arg)
        else:
            history = self._set_price_filter(history, arg)
        return history

    def do_search(self, arg):
        if not self._check_symbol():
            return
        self._first_match = None

        # filter records
        history = self.product.order_by('time')
        history = self._set_time_filters(history)
        if self.symbol in ['TX']:
            history = self._set_k_bar_filter(history, arg)
        else:
            history = self._set_price_filter(history, arg)
        if history.count() == 0:
            print "Not found!"
            return

        self._first_match = history[0]
        # show first 5 records
        first_5 = history[:5]
        for rec in first_5:
            print rec

    def _set_time_filters(self, history):
        if self.range_start:
            history = history.filter(Q(time__gte=self.range_start))
        if self.range_end:
            history = history.filter(Q(time__lte=self.range_end))
        return history

    def _set_k_bar_filter(self, history, arg):
        if arg['and'] or arg['or']:
            op1, op2 = arg['<operator>']
            v1, v2 = arg['<value>']
            q1 = self._make_k_bar_Q_object(op1, v1)
            q2 = self._make_k_bar_Q_object(op2, v2)
            assert q1 and q2, "invalid Q object"
            if arg['and']:
                history = history.filter(q1, q2)
            elif arg['or']:
                history = history.filter(q1 | q2)
        else:
            op = arg['<operator>'][0]
            v = arg['<value>'][0]
            q = self._make_k_bar_Q_object(op, v)
            assert q, "invalid Q object"
            history = history.filter(q)
        return history

    def _make_k_bar_Q_object(self, op, value):
        if op == '<':
            return Q(low__lt=value)
        elif op == '<=':
            return Q(low__lte=value)
        elif op == '=':
            return Q(high__gte=value) & Q(low__lte=value)
        elif op == '>':
            return Q(high__gt=value)
        elif op == '>=':
            return Q(high__gte=value)
        else:
            print "*** unknown operator: %s" % op

    def _set_price_filter(self, history, arg):
        if arg['and'] or arg['or']:
            op1, op2 = arg['<operator>']
            v1, v2 = arg['<value>']
            q1 = self._make_price_Q_object(op1, v1)
            q2 = self._make_price_Q_object(op2, v2)
            if arg['and']:
                history = history.filter(q1, q2)
            elif arg['or']:
                history = history.filter(q1 | q2)
        else:
            op = arg['<operator>'][0]
            v = arg['<value>'][0]
            q = self._make_price_Q_object(op, v)
            history = history.filter(q)
        return history

    def _make_price_Q_object(self, op, value):
        if op == '<':
            return Q(price__lt=value)
        elif op == '<=':
            return Q(price__lte=value)
        elif op == '=':
            return Q(price=value)
        elif op == '>':
            return Q(price__gt=value)
        elif op == '>=':
            return Q(price__gte=value)
        else:
            print "*** unknown operator: %s" % op

    def do_searchf(self, arg):
        if not self._check_symbol():
            return
        self._first_match = None

        # filter records
        history = self.product.order_by('time')
        history = self._set_time_filters(history)
        if self.symbol in ['TX']:
            history = self._set_k_bar_filter(history, arg)
        else:
            history = self._set_price_filter(history, arg)
        if history.count() == 0:
            print "Not found!"
            return

        self._first_match = history[0]
        # push forward the range start
        _1_sec = timedelta(0, 1)
        new_start = self._first_match.time + _1_sec
        curr_tz = timezone.get_current_timezone()
        self.range_start = new_start.astimezone(curr_tz)
        # show first 5 records
        first_5 = history[:5]
        for rec in first_5:
            print rec

    def _check_symbol(self):
        if self.symbol:
            return True
        else:
            print "*** no symbol specified, " + \
                "please use 'index product <symbol>' first"
            return False
