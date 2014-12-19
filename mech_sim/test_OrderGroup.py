#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# libraries
#
import unittest


#
# module under test
#
from history.models import Tx
from lib.time_utils import parse_to_aware
import OrderGroup


#
# test case
#
class TestOrderGroup(unittest.TestCase):
    def setUp(self):
        self.order_group = OrderGroup.OrderGroup()

    def _query_tx(self, datetime_str):
        time = parse_to_aware(datetime_str)
        records = Tx.objects.filter(time__gte=time)
        return records[0]

    def test_pass_invalid_order_type(self):
        record = self._query_tx('2002-06-26 11:13:00')
        self.assertRaises(ValueError,
                          self.order_group.pick_open_price,
                          record,
                          'middle')

    def test_pick_open_price_by_random(self):
        self.order_group.method = 'random'
        record = self._query_tx('2002-06-26 11:13:00')
        price = self.order_group.pick_open_price(record, 'long')
        self.assertGreaterEqual(price, record.low)
        self.assertLessEqual(price, record.high)

    def test_pick_open_price_by_best(self):
        self.order_group.method = 'best'
        record = self._query_tx('2002-06-26 11:13:00')
        long_price = self.order_group.pick_open_price(record, 'long')
        self.assertEqual(long_price, 5135)
        short_price = self.order_group.pick_open_price(record, 'short')
        self.assertEqual(short_price, 5148)

    def test_pick_open_price_by_worst(self):
        self.order_group.method = 'worst'
        record = self._query_tx('2002-06-26 11:13:00')
        long_price = self.order_group.pick_open_price(record, 'long')
        self.assertEqual(long_price, 5148)
        short_price = self.order_group.pick_open_price(record, 'short')
        self.assertEqual(short_price, 5135)

    def test_pick_open_price_by_middle(self):
        self.order_group.method = 'middle'
        record = self._query_tx('2002-06-26 11:13:00')
        long_price = self.order_group.pick_open_price(record, 'long')
        self.assertEqual(long_price, 5141.5)
