#
# project libraries
#
from history.models import *


#
# module classes
#
class IndexGroup():
    """Sub-group commands handler for index searching."""

    def __init__(self):
        products = ProductInfo.objects.all()
        self.symbols = [p.symbol for p in products]

    def complete_command(self, text, line, begin_index, end_index):
        return [text]

    def perform(self, arg):
        print "*** not supported"
