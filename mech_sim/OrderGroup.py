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
