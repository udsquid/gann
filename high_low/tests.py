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
    @classmethod
    def setUpClass(cls):
        build_db()


    def test_get_partial(self):
        data = json_get('/high_low/point/list/?id=2&count=3')
        self.assertEqual(len(data), 3)


    def test_get_length(self):
        data = json_get('/high_low/point/len/')
        self.assertEqual(data, 487)


    def test_filter_points(self):
        build_db()
        data = json_get('/high_low/point/filter/?amplitude=2700')
        pts = [d['price'] for d in data]
        expected = [12682, 2485, 6365, 3098, 7228, 4474, 10256, 5422, 10393, 3411, 9859]
        self.assertEqual(pts, expected)


###
### helper functions
###
def json_get(uri):
    client = Client()
    resp = client.get(uri)
    content = json.loads(resp.content)
    return content['data']


def json_post(uri):
    client = Client()
    resp = client.post(uri)
    content = json.loads(resp.content)


def add_point(time, price):
    uri = '/high_low/point/add/?time=%s&price=%s' % (time, price)
    json_post(uri)


def do_read(source):
    records = list()
    with open(source) as f:
        lines = f.readlines()
        for l in lines:
            time, price = l.replace(',', '').strip().split()
            records.append((time, price))
    return records


def build_db():
    records = do_read('data/taiex_high_low.txt')
    for time, price in records:
        t = time.replace('/', '-')
        p = int(price)
        add_point(t, p)
