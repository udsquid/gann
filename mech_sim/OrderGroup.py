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
    order status

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
        return self._method

    @method.setter
    def method(self, value):
        if value not in ['random', 'best', 'worst', 'middle']:
            err_msg = "*** unsupported method: {}".format(value)
            raise ValueError(err_msg)
        self._method = value

    @property
    def product(self):
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
                ['order', 'status'],
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
            # gather startegy
            self._verify_strategy()
            strategy = self.strategy
            # gather date & time
            if arg['<date>'] and arg['<time>']:
                datetime_str = '{} {}'.format(arg['<date>'], arg['<time>'])
                start_time = parse_to_aware(datetime_str)
            else:
                if not self.first_match:
                    raise Exception("*** no date-time specified")
                start_time = to_local(self.first_match.time)
            # filter records
            if arg['long']:
                open_type = 'long'
            elif arg['short']:
                open_type = 'short'
            if not self.product:
                raise Exception("*** no product specified")
            records = self.product.filter(time__gte=start_time)
            open_time = records[0].time
            open_price = self.pick_open_price(records[0], open_type)
            # gather contract size
            size = arg['--size']
            # open a contract
            self.open_order(strategy,
                            open_type,
                            open_time,
                            open_price,
                            size)
        elif arg['status']:
            self.show_active_orders()
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
        Order.objects.create(strategy=strategy,
                             open_type=type_symbol,
                             open_time=open_time,
                             open_price=open_price,
                             size=size,
                             state='O')
        local_time = to_local(open_time)
        local_time = local_time.strftime(TIME_FORMAT)
        print "Opened a {} order at: {}, price: {}".format(open_type,
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
        else:
            raise ValueError("*** no method specified")

    def _verify_strategy(self):
        if not self.strategy:
            raise Exception("*** no strategy specified")

    def show_active_orders(self):
        self._verify_strategy()
        print '   Name:', self.strategy.name
        print ' Symbol:', self.strategy.symbol
        print ' Method:', self.method
        print 'Active orders:'
        orders = Order.objects.filter(strategy=self.strategy,
                                      state='O')
        if not orders:
            print 'None'
            return
        # show orders in table
        print '{} | {:>5} | {:^19} | {:>6} | {} |'.format(
            'Ticket', 'Type', 'Time', 'Price', 'Size')
        print '-' * 54
        for order in orders:
            temp = to_local(order.open_time)
            formatted_open_time = temp.strftime(TIME_FORMAT)
            print '{:>6} | {:>5} | {} | {:>6} | {:>4} |'.format(
                order.pk,
                order.get_open_type_display(),
                formatted_open_time,
                order.open_price,
                order.size)
