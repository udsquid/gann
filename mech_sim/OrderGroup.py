"""
Sub-group commands for order operations.

Usage:
    order strategy list
    order strategy info <name>
    order strategy new <name> <symbol>
    order strategy load <name>
    order strategy rename <old-name> <new-name>
    order strategy delete <name>
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

    _strategy = None

    @property
    def symbols(self):
        return ['TX']

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, value):
        self._strategy = value

    @property
    def command_forms(self):
        return [['order', 'strategy', 'list'],
                ['order', 'strategy', 'info', '<name>'],
                ['order', 'strategy', 'new', '<name>', '<symbol>'],
                ['order', 'strategy', 'load', '<name>'],
                ['order', 'strategy', 'rename', '<old-name>', '<new-name>'],
                ['order', 'strategy', 'delete', '<name>'],
                ]

    def complete_command(self, text, line, begin_index, end_index):
        return complete_command(text, line, self.command_forms)

    @print_except_only
    def perform(self, arg):
        if arg['strategy']:
            if arg['list']:
                self.show_strategies()
            elif arg['info']:
                self.show_strategy_detail(arg['<name>'])
            elif arg['new']:
                self.create_strategy_entry(arg['<name>'], arg['<symbol>'])
            elif arg['load']:
                self.load_strategy(arg['<name>'])
            elif arg['rename']:
                self.rename_strategy(arg['<old-name>'], arg['<new-name>'])
            elif arg['delete']:
                self.delete_strategy(arg['<name>'])
        else:
            err_msg = "*** should not be here, arg: " + str(arg)
            raise ValueError(err_msg)

    def show_strategies(self):
        strategies = Strategy.objects.order_by('created_time')
        print 'Index | Name'
        print '-' * 60
        for i, s in enumerate(strategies):
            print "{:>5} | {}".format(i+1, s.name)

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

    def load_strategy(self, name):
        s = self._get_strategy(name)
        self.strategy = s.name

    def rename_strategy(self, old_name, new_name):
        s = self._get_strategy(old_name)
        s.name = new_name
        s.save()

    def delete_strategy(self, name):
        s = self._get_strategy(name)
        s.delete()
