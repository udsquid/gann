"""
Sub-group commands for index operations.

Usage:
    index product <symbol>
    index range (start | end) <date> [<time>]
    index status
    index (search | searchf) <operator> <value>
        [(and | or) <operator> <value>]
"""


#
# project libraries
#
from history.models import *


#
# module classes
#
class IndexGroup():

    actions = ['product', 'range', 'status', 'search', 'searchf']

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
        print "*** not supported"
