#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# libraries
#
import unittest

from docopt import docopt


#
# module under test
#
import IndexGroup


#
# test case
#
class TestIndexGroup(unittest.TestCase):
    def setUp(self):
        self.index_group = IndexGroup.IndexGroup()

    def test_range_reset(self):
        self.index_group.reset_range()
        self.assertIsNone(self.index_group.range_start)
        self.assertIsNone(self.index_group.range_end)

#
# main procedure
#
if __name__ == '__main__':
    unittest.main()
