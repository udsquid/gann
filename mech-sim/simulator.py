#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This mechanism simulator which provides following functional groups that
can help us to analyze our newly designed trading mechanisms:
    - product information system
    - index query system
    - trading report system

Usage:
    simulator.py -i | --interactive
    simulator.py -h | --help
    simulator.py -v | --version

Options:
    -i, --interactive    Interactive mode.
    -h, --help           Show this screen.
    -v, --version        Show version number.
"""

#
# python libraries
#
import cmd


#
# 3-party libraries
#
from docopt import docopt


#
# project libraries
#
from lib.docopt_decorator import docopt_cmd
import IndexGroup as IG
import ProductGroup as PG


#
# main procedure
#
class MainInteractive(cmd.Cmd):
    intro = "Welcome to mechanism simulator!" + \
            "\n" + \
            "(type help for a list of commands)" + \
            "\n"
    prompt = "mech-sim$ "

    product_group = PG.ProductGroup()
    index_group = IG.IndexGroup()

    def emptyline(self):
        """Override with no action to avoid repeat last command,
        that is so noisy!"""

        pass

    def do_quit(self, arg):
        """Quits out of interactive mode."""

        print("Good Bye!")
        exit()

    def complete_product(self, text, line, begin_index, end_index):
        return self.product_group.complete_command(
            text, line, begin_index, end_index)

    @docopt_cmd(PG.ProductGroup)
    def do_product(self, arg):
        """Usage:
        product list
        product info <symbol>
        """

        self.product_group.perform(arg)

    def complete_index(self, text, line, begin_index, end_index):
        return self.index_group.complete_command(
            text, line, begin_index, end_index)

    @docopt_cmd(IG.IndexGroup)
    def do_index(self, arg):
        self.index_group.perform(arg)

option = docopt(__doc__, version='Mechanism Simulator 1.0')
if option['--interactive']:
    cli = MainInteractive()
    cli.cmdloop()
