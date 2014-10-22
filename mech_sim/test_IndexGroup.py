#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# libraries
#
from datetime import datetime
import unittest

from django.utils import timezone
from django.utils.dateparse import parse_datetime
from docopt import docopt
import pytz


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

    def _parse_datetime(self, value):
        naive_datetime = parse_datetime(value)
        curr_tz = timezone.get_current_timezone_name()
        return pytz.timezone(curr_tz).localize(naive_datetime)

    def test_range_reset(self):
        self.index_group.reset_range()
        self.assertIsNone(self.index_group.range_start)
        self.assertIsNone(self.index_group.range_end)

    def test_set_range_start2_by_str(self):
        datetime_str = '2014-10-22 01:07:43'
        self.index_group.range_start2 = datetime_str
        expected = self._parse_datetime(datetime_str)
        self.assertEqual(self.index_group.range_start2, expected)

    def test_set_invalid_range_format(self):
        datetime_str = '2014/10/22 01:07:43'
        self.assertRaises(ValueError,
                          self.index_group.range_start2,
                          datetime_str)


#
# main procedure
#
if __name__ == '__main__':
    unittest.main()
