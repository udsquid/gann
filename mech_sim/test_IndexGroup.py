#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# libraries
#
from datetime import datetime, time
import unittest

from django.utils import timezone
from django.utils.dateparse import parse_datetime, parse_date
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

    def _parse_date(self, value):
        naive_date = parse_date(value)
        naive_datetime = datetime.combine(naive_date, time.min)
        curr_tz = timezone.get_current_timezone_name()
        return pytz.timezone(curr_tz).localize(naive_datetime)

    def _parse_datetime(self, value):
        naive_datetime = parse_datetime(value)
        curr_tz = timezone.get_current_timezone_name()
        return pytz.timezone(curr_tz).localize(naive_datetime)

    def test_range_reset(self):
        self.index_group.reset_range()
        self.assertIsNone(self.index_group.range_start)
        self.assertIsNone(self.index_group.range_end)

    def test_set_range_start2_by_date_only(self):
        date_str = '2000-1-1'
        self.index_group.range_start2 = date_str
        expected = self._parse_date(date_str)
        self.assertEqual(self.index_group.range_start2, expected)

    def test_set_range_start2_by_date_and_time(self):
        datetime_str = '2014-10-22 01:07:43'
        self.index_group.range_start2 = datetime_str
        expected = self._parse_datetime(datetime_str)
        self.assertEqual(self.index_group.range_start2, expected)

    def test_set_range_start2_by_datetime_obj(self):
        datetime_obj = datetime(2000, 1, 1, 0, 0, tzinfo=timezone.utc)
        self.index_group.range_start2 = datetime_obj
        expected = self._parse_datetime('2000-01-01 08:00:00')
        self.assertEqual(self.index_group.range_start2, expected)

    def test_set_invalid_range_format(self):
        datetime_str = '2014/10/22 01:07:43'
        self.assertRaises(ValueError,
                          self.index_group.range_start2,
                          datetime_str)
        self.assertRaises(ValueError,
                          self.index_group.range_end2,
                          datetime_str)

    def test_set_range_end2_by_str(self):
        datetime_str = '2014-10-22 01:07:43'
        self.index_group.range_end2 = datetime_str
        expected = self._parse_datetime(datetime_str)
        self.assertEqual(self.index_group.range_end2, expected)

    def test_set_range_end2_by_obj(self):
        datetime_obj = datetime(2000, 1, 1, 0, 0, tzinfo=timezone.utc)
        self.index_group.range_end2 = datetime_obj
        expected = self._parse_datetime('2000-01-01 08:00:00')
        self.assertEqual(self.index_group.range_end2, expected)

    def test_check_range(self):
        # test both end are empty
        result = self.index_group.check_range()
        self.assertTrue(result)
        # test no start
        self.index_group.range_end2 = '2107-06-10 12:00:00'
        result = self.index_group.check_range()
        self.assertTrue(result)
        # test no end
        self.index_group.range_start2 = '2007-06-10 12:00:00'
        result = self.index_group.check_range()
        self.assertTrue(result)
        # test good range
        self.index_group.range_start2 = '2007-06-10 12:00:00'
        self.index_group.range_end2 = '2207-06-10 23:59:59'
        result = self.index_group.check_range()
        self.assertTrue(result)
        # test bad range
        self.index_group.range_start2 = '2007-06-10 12:00:00'
        self.index_group.range_end2 = '2007-06-10 11:59:59'
        result = self.index_group.check_range()
        self.assertFalse(result)

    # def test_filter_taiex_by_(self):
    #     self.index_group.set_product('TAIEX')
    #     self.index_group.range_start2 = '2000-1-1'
    #     opt = docopt(IndexGroup.__doc__, 'index search < 8500')
    #     print opt
    #     self.index_group.filter_history(opt)


#
# main procedure
#
if __name__ == '__main__':
    unittest.main()
