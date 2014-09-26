"""
Sub-group commands for product operations.

Usage:
    product list
    product info <symbol>
"""


#
# 3-party libraries
#
from django.utils import timezone


#
# project libraries
#
from history.models import *


#
# module classes
#
class ProductGroup():

    actions = ['list', 'info']

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
            if act in line:
                return True
        return False

    def perform(self, arg):
        if arg['list']:
            self.show_symbols()
        elif arg['info']:
            self.show_product_info(arg['<symbol>'])
        else:
            print "*** not supported"

    def show_symbols(self):
        for index, name in enumerate(self.symbols):
            print "%d. %s" % (index+1, name)

    def show_product_info(self, symbol):
        if symbol not in self.symbols:
            print "*** unknown symbol: %s" % symbol
        # calculate info title length for printing
        info_title = dict(
            symbol='Symbol',
            name='Full name',
            tick='Tick value',
            begin='Begin time',
            end='End time',
            )
        item_len = [len(v) for v in info_title.values()]
        min_width = max(item_len)
        # print info
        product = ProductInfo.objects.get(symbol=symbol)
        print "{symbol:>{width}}: {value}".format(value=product.symbol,
                                                  width=min_width,
                                                  **info_title)
        print "{name:>{width}}: {value}".format(value=product.full_name,
                                                width=min_width,
                                                **info_title)
        print "{tick:>{width}}: {value}".format(value=product.tick_value,
                                                width=min_width,
                                                **info_title)
        if symbol == 'TAIEX':
            self._print_time_range(Taiex, info_title, min_width)
        elif symbol == 'TX':
            self._print_time_range(Tx, info_title, min_width)

    def _print_time_range(self, product, title_dict, title_width):
        data = product.objects.all().order_by('time')
        count = data.count()
        begin = data[0].time
        end = data[count-1].time
        self._print_time(title_dict['begin'], begin, title_width)
        self._print_time(title_dict['end'], end, title_width)

    def _print_time(self, title, value, title_width):
        curr_tz = timezone.get_current_timezone()
        value = value.astimezone(curr_tz)
        time_format = "%Y-%m-%d %H:%M:%S"
        print "{title:>{width}}: {value:{format}}".format(
            title=title,
            width=title_width,
            value=value,
            format=time_format)
