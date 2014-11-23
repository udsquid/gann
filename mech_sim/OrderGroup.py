"""
Sub-group commands for order operations.

Usage:
    order strategy list
    order strategy new <name> <symbol>
    order strategy info <name>
"""


#
# python libraries
#
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


#
# project libraries
#
from auto_complete import *
from lib.exception_decorator import print_except_only
from lib.time_utils import to_local
from mech_sim.order.models import *


#
# module classes
#
class OrderGroup(object):

    def __init__(self):
        pass

    @property
    def actions(self):
        return ['strategy']

    @property
    def symbols(self):
        return ['TX']

    @property
    def command_forms(self):
        return [['order', 'strategy', 'list'],
                ['order', 'strategy', 'new', '<name>', '<symbol>'],
                ['order', 'strategy', 'info', '<name>'],
                ]

    def complete_command(self, text, line, begin_index, end_index):
        return complete_command(text, line, self.command_forms)

    @print_except_only
    def perform(self, arg):
        if arg['strategy']:
            if arg['list']:
                self.show_strategies()
            elif arg['new']:
                self.create_strategy_entry(arg['<name>'], arg['<symbol>'])
            elif arg['info']:
                self.show_strategy_detail(arg['<name>'])
        else:
            err_msg = "*** should not be here, arg: " + str(arg)
            raise ValueError(err_msg)

    def show_strategies(self):
        strategies = Strategy.objects.order_by('created_time')
        print 'Index | Name'
        print '-' * 60
        for i, s in enumerate(strategies):
            print "{:>5} | {}".format(i+1, s.name)

    def create_strategy_entry(self, name, symbol):
        upper_sym = symbol.upper()
        if upper_sym not in self.symbols:
            err_msg = "*** unknown symbol: %s" % symbol
            raise ValueError(err_msg)
        try:
            Strategy.objects.create(name=name, symbol=upper_sym)
        except IntegrityError as e:
            if 'UNIQUE constraint failed' not in str(e):
                raise e
            err_msg = "*** duplicate name: %s" % name
            raise ValueError(err_msg)

    def show_strategy_detail(self, name):
        s = self._get_strategy(name)
        created_time = to_local(s.created_time)
        _format = "%Y-%m-%d %H:%M:%S"
        print '   Name:', s.name
        print ' Symbol:', s.symbol
        print 'Created:', created_time.strftime(_format)

    def _get_strategy(self, name):
        try:
            return Strategy.objects.get(name=name)
        except ObjectDoesNotExist:
            err_msg = "*** strategy does not exist: %s" % name
            raise ValueError(err_msg)
