"""
Sub-group commands for index operations.

Usage:
    index product <symbol>
    index range (start | end) <date> [<time>]
    index range forward
    index range reset
    index status
    index (search | searchf) <operator> <value>
        [((and | or) <operator> <value>)]
"""


#
# python libraries
#
from datetime import datetime, time, timedelta
import re


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
from lib.exception_decorator import print_except_only
from auto_complete import *


#
# module classes
#
class IndexGroup(object):

    actions = ['product', 'range', 'status', 'search', 'searchf']
    symbol = None

    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self):
        products = ProductInfo.objects.all()
        self.symbols = [p.symbol for p in products]
        self._range_start = None
        self._range_end = None
        self._first_match = None

    @property
    def first_match(self):
        return self._first_match

    @property
    def command_form(self):
        return [['index', 'product', '<symbol>'],
                ['index', 'range', ['start', 'end'], '<date>', '[<time>]'],
                ['index', 'range', 'forward'],
                ['index', 'range', 'reset'],
                ['index', 'status'],
                ['index', ['search', 'searchf'], '<operator>', '<value>',
                          ['and', 'or'], '<operator>', '<value>'],
                ]

    def complete_command(self, text, line, begin_index, end_index):
        return complete_command(text, line, self.command_form)

    def perform(self, arg):
        if arg['product']:
            symbol = arg['<symbol>'].upper()
            self.set_product(symbol)
        elif arg['range']:
            if arg['forward']:
                self.forward_range_start()
                new_start = self.range_start.strftime(TIME_FORMAT)
                print "Range start has been forwarded to [{}]".format(
                    new_start)
            elif arg['reset']:
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

    @print_except_only
    def set_range(self, arg):
        assert arg['<date>'], "no date specified"
        if arg['<time>']:
            datetime_str = '{<date>} {<time>}'.format(**arg)
        else:
            datetime_str = arg['<date>']
        if arg['start']:
            self.range_start = datetime_str
        elif arg['end']:
            self.range_end = datetime_str
        if not self.check_range():
            print "!!! WARNING: empty range"

    def check_range(self):
        start = self.range_start
        end = self.range_end
        if not start or not end:
            return True
        elif start < end:
            return True
        else:
            return False

    def reset_range(self):
        self.range_start = None
        self.range_end = None

    @property
    def range_start(self):
        return self._range_start

    @range_start.setter
    def range_start(self, value):
        if value is None:
            self._range_start = None
        elif isinstance(value, (str, unicode)):
            naive_datetime = self._parse_datetime(value)
            if not naive_datetime:
                raise ValueError("*** invalid date-time format")
            self._range_start = self._to_aware(naive_datetime)
        elif isinstance(value, datetime):
            self._range_start = self._to_local(value)

    @property
    def range_end(self):
        return self._range_end

    @range_end.setter
    def range_end(self, value):
        if value is None:
            self._range_end = None
        elif isinstance(value, (str, unicode)):
            naive_datetime = self._parse_datetime(value)
            if not naive_datetime:
                raise ValueError("*** invalid date-time format")
            self._range_end = self._to_aware(naive_datetime)
        elif isinstance(value, datetime):
            self._range_end = self._to_local(value)

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

    def show_status(self):
        # calculate status title length for printing
        status_title = dict(
            symbol='Symbol',
            start='Range start',
            end='Range end',
            match='First match',
        )
        item_len = [len(v) for v in status_title.values()]
        width = max(item_len)
        # print status
        print "{symbol:{width}}: {value}".format(value=self.symbol,
                                                 width=width,
                                                 **status_title)
        range_format = '%Y-%m-%d %H:%M:%S'
        if self.range_start:
            print "{start:{width}}: {value:{format}}".format(
                value=self.range_start,
                width=width,
                format=range_format,
                **status_title)
        else:
            print "{start:{width}}: {value}".format(
                value=self.range_start,
                width=width,
                **status_title)
        if self.range_end:
            print "{end:{width}}: {value:{format}}".format(
                value=self.range_end,
                width=width,
                format=range_format,
                **status_title)
        else:
            print "{end:{width}}: {value}".format(
                value=self.range_end,
                width=width,
                **status_title)
        print "{match:{width}}: {value}".format(value=self.first_match,
                                                width=width,
                                                **status_title)

    @print_except_only
    def do_search(self, arg):
        if not self._check_symbol():
            return

        self._first_match = None
        history = self.filter_history(arg)
        if history.count() == 0:
            print "Not found!"
            return
        self._first_match = history[0]
        # show first 5 records
        first_5 = history[:5]
        for rec in first_5:
            print rec

    def filter_history(self, arg):
        history = self.product.order_by('time')
        history = self._set_time_filters(history)
        if self.symbol in ['TX']:
            history = self._set_k_bar_filter(history, arg)
        else:
            history = self._set_price_filter(history, arg)
        return history

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
            if arg['and']:
                history = history.filter(q1, q2)
            elif arg['or']:
                history = history.filter(q1 | q2)
        else:
            op = arg['<operator>'][0]
            v = arg['<value>'][0]
            q = self._make_k_bar_Q_object(op, v)
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
            raise ValueError("*** unknown operator: %s" % op)

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
            raise ValueError("*** unknown operator: %s" % op)

    @print_except_only
    def do_searchf(self, arg):
        if not self._check_symbol():
            return

        self._first_match = None
        history = self.filter_history(arg)
        if history.count() == 0:
            print "Not found!"
            return
        self._first_match = history[0]
        self.forward_range_start()
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

    def forward_range_start(self):
        if not self.first_match:
            raise Exception("*** no first match record")

        one_sec = timedelta(0, 1)
        self.range_start = self.first_match.time + one_sec
