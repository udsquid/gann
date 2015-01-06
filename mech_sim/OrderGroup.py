"""
Sub-group commands for order operations.

Usage:
    order strategy list
    order strategy info <name>
    order strategy new <name> <symbol>
    order strategy load <name>
    order strategy rename <old-name> <new-name>
    order strategy delete <name>
    order method (random | best | worst | middle)
    order open (long | short) [--size=<n>] [(<date> <time>)]
    order close [(<date> <time>)] [--ticket=<id>]
    order delete <from>
    order status
    order summary

Options:
    --size=<n>    Contract size [default: 1]
"""


#
# python libraries
#
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
import random


#
# project libraries
#
from auto_complete import *
from history.models import *
from lib.exception_decorator import print_except_only
from lib.time_utils import parse_to_aware, to_local
from mech_sim.order.models import *


#
# module classes
#
class OrderGroup(object):

    _strategy = None
    _method = None
    _product = None
    _first_match = None

    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    @property
    def symbols(self):
        return ['TX']

    @property
    def strategy(self):
        if not self._strategy:
            raise Exception("*** no strategy specified")
        return self._strategy

    @strategy.setter
    def strategy(self, value):
        if not isinstance(value, Strategy):
            value_type = type(value)
            err_msg = "*** error strategy value: <{}>{}".format(value_type,
                                                                value)
        self._strategy = value

    @property
    def method(self):
        if not self._method:
            raise Exception("*** no method specified")
        return self._method

    @method.setter
    def method(self, value):
        if value not in ['random', 'best', 'worst', 'middle']:
            err_msg = "*** unsupported method: {}".format(value)
            raise ValueError(err_msg)
        self._method = value

    @property
    def product(self):
        if not self._product:
            raise Exception("*** no product specified")
        return self._product

    @product.setter
    def product(self, value):
        if not value:
            self._product = None
            return
        self._verify_symbol(value)
        upper_value = value.upper()
        if upper_value == 'TX':
            self._product = Tx.objects

    @property
    def digits(self):
        return 2

    @property
    def first_match(self):
        return self._first_match

    @first_match.setter
    def first_match(self, value):
        self._first_match = value

    @property
    def command_forms(self):
        return [['order', 'strategy', 'list'],
                ['order', 'strategy', 'info', '<name>'],
                ['order', 'strategy', 'new', '<name>', '<symbol>'],
                ['order', 'strategy', 'load', '<name>'],
                ['order', 'strategy', 'rename', '<old-name>', '<new-name>'],
                ['order', 'strategy', 'delete', '<name>'],
                ['order', 'method', ['random', 'best', 'worst', 'middle']],
                ['order', 'open', ['long', 'short'],
                          '--size=<n>', '<date> <time>'],
                ['order', 'close', '<date> <time>', '--ticket=<id>'],
                ['order', 'delete', '<from>'],
                ['order', 'status'],
                ['order', 'summary'],
                ]

    def complete_command(self, text, line, begin_index, end_index):
        return complete_command(text, line, self.command_forms)

    def _verify_symbol(self, symbol):
        upper_sym = symbol.upper()
        if upper_sym not in self.symbols:
            err_msg = "*** unknown symbol: {}".format(value)
            raise ValueError(err_msg)

    @print_except_only
    def perform(self, arg):
        if arg['strategy']:
            if arg['list']:
                self.show_strategies()
            elif arg['info']:
                name = arg['<name>']
                self.show_strategy_detail(name)
            elif arg['new']:
                name = arg['<name>']
                symbol = arg['<symbol>']
                self.create_strategy_entry(name, symbol)
            elif arg['load']:
                name = arg['<name>']
                self.load_strategy(name)
            elif arg['rename']:
                old_name = arg['<old-name>']
                new_name = arg['<new-name>']
                self.rename_strategy(old_name, new_name)
            elif arg['delete']:
                name = arg['<name>']
                self.delete_strategy(name)
        elif arg['method']:
            if arg['random']:
                self.method = 'random'
            elif arg['best']:
                self.method = 'best'
            elif arg['worst']:
                self.method = 'worst'
            elif arg['middle']:
                self.method = 'middle'
        elif arg['open']:
            strategy = self.strategy
            open_type, open_time, open_price = self._gather_open_info(arg)
            size = arg['--size']
            self.open_order(strategy,
                            open_type,
                            open_time,
                            open_price,
                            size)
        elif arg['close']:
            if arg['--ticket']:
                self._verify_ticket(arg['--ticket'])
                ticket = arg['--ticket']
            else:
                ticket = self.query_last_active_ticket(self.strategy)
            _time, _price = self._gather_close_info(ticket, arg)
            self.close_order(ticket, _time, _price)
        elif arg['delete']:
            from_ticket = arg['<from>']
            self.delete_order(from_ticket, self.strategy)
        elif arg['status']:
            self.show_active_orders()
        elif arg['summary']:
            self.show_order_summary()
        else:
            err_msg = "*** invalid perform arguments: " + str(arg)
            raise ValueError(err_msg)

    def show_strategies(self):
        strategies = Strategy.objects.order_by('created_time')
        print 'Index | Name'
        print '-' * 60
        for i, s in enumerate(strategies):
            print "{:>5} | {}".format(i+1, s.name)

    def show_strategy_detail(self, name):
        s = self._query_strategy(name)
        created_time = to_local(s.created_time)
        print '   Name:', s.name
        print ' Symbol:', s.symbol
        print 'Created:', created_time.strftime(TIME_FORMAT)

    def _query_strategy(self, name):
        try:
            return Strategy.objects.get(name=name)
        except ObjectDoesNotExist:
            err_msg = "*** strategy does not exist: {}".format(name)
            raise ValueError(err_msg)

    def create_strategy_entry(self, name, symbol):
        self._verify_symbol(symbol)
        try:
            upper_sym = symbol.upper()
            self.strategy = Strategy.objects.create(name=name,
                                                    symbol=upper_sym)
            self.product = upper_sym
        except IntegrityError as e:
            if 'UNIQUE constraint failed' not in str(e):
                raise e
            err_msg = "*** duplicate name: {}".format(name)
            raise ValueError(err_msg)

    def load_strategy(self, name):
        self.strategy = self._query_strategy(name)
        self.product = self.strategy.symbol

    def rename_strategy(self, old_name, new_name):
        s = self._query_strategy(old_name)
        s.name = new_name
        s.save()
        if self.strategy.name == old_name:
            self.strategy = s

    def delete_strategy(self, name):
        s = self._query_strategy(name)
        s.delete()
        if self.strategy.name == name:
            self.strategy = None
            self.product = None

    def _verify_open_type(self, open_type):
        if open_type not in ['long', 'short']:
            err_msg = "*** unsupported open type: {}".format(open_type)
            raise ValueError(err_msg)

    def open_order(self, strategy, open_type, open_time, open_price, size):
        self._verify_open_type(open_type)
        type_symbol = Order.get_open_type_symbol(open_type)
        new_order = Order.objects.create(strategy=strategy,
                                         open_type=type_symbol,
                                         open_time=open_time,
                                         open_price=open_price,
                                         size=size,
                                         state='O')
        local_time = to_local(open_time)
        local_time = local_time.strftime(TIME_FORMAT)
        print "Opened a {} order #{} at [{}], price is {}".format(
            open_type.upper(),
            new_order.pk,
            local_time,
            open_price)

    def pick_open_price(self, record, open_type):
        self._verify_open_type(open_type)

        # single point record, return it's price value directly
        if hasattr(record, 'price'):
            return record.price

        # k-bar like record, pick a price by specified method
        high = record.high
        low = record.low
        places = self.digits
        if self.method == 'random':
            lower = float(low)
            upper = float(high)
            open_price = random.uniform(lower, upper)
            if places == 0:
                return int(open_price)
            return round(open_price, places)
        elif self.method == 'best':
            if open_type == 'long': 
                return low
            elif open_type == 'short':
                return high
        elif self.method == 'worst':
            if open_type == 'long': 
                return high
            elif open_type == 'short':
                return low
        elif self.method == 'middle':
            lower = float(low)
            upper = float(high)
            open_price = (upper + lower) / 2.0
            if places == 0:
                return int(open_price)
            return round(open_price, places)

    def show_active_orders(self):
        print '   Name:', self.strategy.name
        print ' Symbol:', self.strategy.symbol
        print ' Method:', self.method
        print 'Active orders:'
        active_orders = Order.objects.filter(strategy=self.strategy,
                                             state='O')
        if not active_orders.exists():
            print '--- None ---'
            return
        # show orders in table
        print '{} | {:>5} | {:^19} | {:>6} | {} |'.format(
            'Ticket', 'Type', 'Time', 'Price', 'Size')
        print '-' * 54
        for order in active_orders:
            temp = to_local(order.open_time)
            formatted_open_time = temp.strftime(TIME_FORMAT)
            print '{:>6} | {:>5} | {} | {:>6} | {:>4} |'.format(
                order.pk,
                order.get_open_type_display(),
                formatted_open_time,
                order.open_price,
                order.size)

    def _make_start_time(self, arg):
        if arg['<date>'] and arg['<time>']:
            datetime_str = '{} {}'.format(arg['<date>'], arg['<time>'])
            return parse_to_aware(datetime_str)
        if self.first_match:
            return to_local(self.first_match.time)
        raise Exception("*** no date-time specified or match record")

    def _gather_open_info(self, arg):
        # gather open type
        if arg['long']:
            open_type = 'long'
        elif arg['short']:
            open_type = 'short'
        # gather open time & price
        start_time = self._make_start_time(arg)
        records = self.product.filter(time__gte=start_time)
        open_time = records[0].time
        open_price = self.pick_open_price(records[0], open_type)

        return open_type, open_time, open_price

    def _verify_ticket(self, ticket):
        try:
            Order.objects.get(pk=ticket, strategy=self.strategy)
        except ObjectDoesNotExist:
            err_fmt = "*** strategy {} does not have ticket: {}"
            err_msg = err_fmt.format(self.strategy.name, ticket)
            raise ValueError(err_msg)

    def query_last_active_ticket(self, strategy):
        active_orders = Order.objects.filter(strategy=strategy,
                                             state='O')
        if not active_orders.exists():
            err_fmt = "*** no active orders in strategy: {}"
            err_msg = err_fmt.format(strategy.name)
            raise Exception(err_msg)
        last_order = active_orders.order_by('pk').last()
        return last_order.pk

    def _gather_close_info(self, ticket, arg):
        order = Order.objects.get(pk=ticket)
        open_type = order.get_open_type_display().lower()
        start_time = self._make_start_time(arg)
        records = self.product.filter(time__gte=start_time)
        close_time = records[0].time
        close_price = self.pick_close_price(records[0], open_type)
        return close_time, close_price

    def pick_close_price(self, record, open_type):
        self._verify_open_type(open_type)

        # single point record, return it's price value directly
        if hasattr(record, 'price'):
            return record.price

        # k-bar like record, pick a price by specified method
        high = record.high
        low = record.low
        places = self.digits
        if self.method == 'random':
            lower = float(low)
            upper = float(high)
            close_price = random.uniform(lower, upper)
            if places == 0:
                return int(close_price)
            return round(close_price, places)
        elif self.method == 'best':
            if open_type == 'long': 
                return high
            elif open_type == 'short':
                return low
        elif self.method == 'worst':
            if open_type == 'long': 
                return low
            elif open_type == 'short':
                return high
        elif self.method == 'middle':
            lower = float(low)
            upper = float(high)
            close_price = (upper + lower) / 2.0
            if places == 0:
                return int(close_price)
            return round(close_price, places)

    def close_order(self, ticket, close_time, close_price):
        order = Order.objects.get(pk=ticket)
        if order.get_state_display() == 'Close':
            raise Exception("*** order had been closed before")
        if order.open_time > close_time:
            raise Exception("*** close time is before open time")
        order.close_time = close_time
        order.close_price = close_price
        order.state = 'C'
        order.save()

        local_time = to_local(close_time)
        local_time = local_time.strftime(TIME_FORMAT)
        print "Closed order #{} at [{}], price is {}".format(
            ticket, local_time, close_price)

    def delete_order(self, ticket, strategy):
        orders = Order.objects.filter(pk__gte=ticket,
                                      strategy=strategy)
        if not orders.exists():
            print "!!! WARNING: no matching orders, skip deletion"
            return
        delete_num = orders.count()
        confirm_msg = "{} order(s) will be deleted, " \
                      "are you sure? (y/n): ".format(delete_num)
        choice = raw_input(confirm_msg)
        if choice.lower() in ['y', 'yes']:
            orders.delete()
            print "{} order(s) has beed deleted".format(delete_num)
        else:
            print "cancel deletion"

    def show_order_summary(self):
        print "Strategy: {:<40} Symbol: {}".format(
            self.strategy.name,
            self.strategy.symbol)
        print "Win: {:>10}    Lose: {:>10}".format('', '')
