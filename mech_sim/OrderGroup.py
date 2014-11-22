"""
Sub-group commands for order operations.

Usage:
    order strategy list
"""


#
# python libraries
#


#
# project libraries
#
from mech_sim.order.models import *
from lib.exception_decorator import print_except_only
from auto_complete import *


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
    def command_form(self):
        return [['order', 'strategy', 'list'],
                ]

    def complete_command(self, text, line, begin_index, end_index):
        return complete_command(text, line, self.command_form)

    def perform(self, arg):
        if arg['strategy']:
            if arg['list']:
                self.show_strategies()
        else:
            err_msg = "*** should not be here, arg: " + str(arg)
            raise ValueError(err_msg)

    def show_strategies(self):
        strategies = Strategy.objects.order_by('created_time')
        print 'Index | Name'
        print '-' * 60
        for i, s in enumerate(strategies):
            print "{:>5} | {}".format(i+1, s.name)
