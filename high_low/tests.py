###
### python libraries
###
import json


###
### django libraries
###
from django.test import TestCase
from django.test.client import Client


###
### project libraries
###
from high_low.models import Point


###
### Point test cases
###
class PointViewTests(TestCase):
    def test_get_partial(self):
        self.add_point('1990-02-12', 12682)
        self.add_point('1990-02-17', 11550)
        self.add_point('1990-02-21', 12321)
        self.add_point('1990-02-27', 10995)
        self.add_point('1990-03-01', 11720)
        data = self._json_get('/high_low/point/list/?id=2&count=3')
        self.assertEqual(len(data), 3)


    def test_get_length(self):
        self.add_point('1990-02-12', 12682)
        self.add_point('1990-02-17', 11550)
        self.add_point('1990-02-21', 12321)
        self.add_point('1990-02-27', 10995)
        self.add_point('1990-03-01', 11720)
        data = self._json_get('/high_low/point/len/')
        self.assertEqual(data, 5)


    def test_add_point(self):
        self.add_point('1995-09-30', 4986)
        self.add_point('1995-10-09', 5265)
        self.add_point('1995-11-18', 4530)
        data = self._json_get('/high_low/point/list/')
        self.assertEqual(data[0]['fields']['time'], '1995-09-30')
        self.assertEqual(data[0]['fields']['price'], 4986)
        self.assertEqual(data[1]['fields']['time'], '1995-10-09')
        self.assertEqual(data[1]['fields']['price'], 5265)
        self.assertEqual(data[2]['fields']['time'], '1995-11-18')
        self.assertEqual(data[2]['fields']['price'], 4530)


    def test_filter_points(self):
        data = self._json_get('/high_low/point/filter/?amplitude=2700')
        self.assertEqual(data[0]['fields']['price'], 12682)
        self.assertEqual(data[1]['fields']['price'], 2485)
        self.assertEqual(data[2]['fields']['price'], 6365)
        self.assertEqual(data[3]['fields']['price'], 3098)
        self.assertEqual(data[4]['fields']['price'], 7228)
        self.assertEqual(data[5]['fields']['price'], 4474)
        self.assertEqual(data[6]['fields']['price'], 10256)
        self.assertEqual(data[7]['fields']['price'], 5422)
        self.assertEqual(data[8]['fields']['price'], 10393)
        self.assertEqual(data[9]['fields']['price'], 3411)


    def add_point(self, time, price):
        uri = '/high_low/point/add/?time=%s&price=%d' % (time, price)
        self._json_post(uri)


    def _json_get(self, uri):
        client = Client()
        resp = client.get(uri)
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(content['success'], True)
        return content['data']


    def _json_post(self, uri):
        client = Client()
        resp = client.post(uri)
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(content['success'], True)
