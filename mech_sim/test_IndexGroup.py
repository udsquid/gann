#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# libraries
#
from datetime import datetime, time
from decimal import Decimal
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

    def test_set_range_end2_by_date_only(self):
        date_str = '2000-1-1'
        self.index_group.range_end2 = date_str
        expected = self._parse_date(date_str)
        self.assertEqual(self.index_group.range_end2, expected)

    def test_set_range_end2_by_date_and_time(self):
        datetime_str = '2014-10-22 01:07:43'
        self.index_group.range_end2 = datetime_str
        expected = self._parse_datetime(datetime_str)
        self.assertEqual(self.index_group.range_end2, expected)

    def test_set_range_end2_by_datetime_obj(self):
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

    def test_filter_taiex_by_single_op_1(self):
        self.index_group.set_product('TAIEX')
        self.index_group.range_start2 = '2000-2-18'
        self.index_group.range_start = self.index_group.range_start2
        cmd = 'index search < 8500'.split()[1:]
        opt = docopt(IndexGroup.__doc__, cmd)
        match = self.index_group.filter_history(opt)[0]
        exp_time = self._parse_datetime('2000-03-16 09:01:00')
        exp_price = Decimal('8472.54')
        self.assertEqual(exp_time, match.time)
        self.assertEqual(exp_price, match.price)

    def test_filter_taiex_by_single_op_2(self):
        self.index_group.set_product('TAIEX')
        self.index_group.range_start2 = '2001-2-21'
        self.index_group.range_start = self.index_group.range_start2
        cmd = 'index search > 6500'.split()[1:]
        opt = docopt(IndexGroup.__doc__, cmd)
        match = self.index_group.filter_history(opt)[0]
        exp_time = self._parse_datetime('2004-02-10 12:01:00')
        exp_price = Decimal('6501.84')
        self.assertEqual(exp_time, match.time)
        self.assertEqual(exp_price, match.price)

    def test_filter_taiex_by_two_ops(self):
        self.index_group.set_product('TAIEX')
        # search greater than upper
        self.index_group.range_start2 = '2004-2-10'
        self.index_group.range_start = self.index_group.range_start2
        cmd = 'index search > 7000 or < 6000'.split()[1:]
        opt = docopt(IndexGroup.__doc__, cmd)
        match = self.index_group.filter_history(opt)[0]
        exp_time = self._parse_datetime('2004-03-03 09:05:00')
        exp_price = Decimal('7003.88')
        self.assertEqual(exp_time, match.time)
        self.assertEqual(exp_price, match.price)
        # search less than lower
        self.index_group.range_start2 = '2004-3-9'
        self.index_group.range_start = self.index_group.range_start2
        cmd = 'index search > 7000 or < 6000'.split()[1:]
        opt = docopt(IndexGroup.__doc__, cmd)
        match = self.index_group.filter_history(opt)[0]
        exp_time = self._parse_datetime('2004-05-03 09:14:00')
        exp_price = Decimal('5994.07')
        self.assertEqual(exp_time, match.time)
        self.assertEqual(exp_price, match.price)


#
# main procedure
#
if __name__ == '__main__':
    unittest.main()
