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
        points = json_get('/high_low/point/filter/?amplitude=2700')
        actual = [p['price'] for p in points]
        expected = [12682, 2485, 6365, 3098, 7228, 4474, 10256, 5422, 10393, 3411, 9859]
        self.assertEqual(actual, expected)


    def test_filter_points2(self):
        points = json_get('/high_low/point/filter/?amplitude=450')
        actual = [p['price'] for p in points]
        expected = [12682, 11550, 12321, 10995, 11720, 10887, 12065, 10145, 11282, 9405, 10011, 8652, 9838, 8252, 9062, 8125, 8689, 5822, 8007, 5758, 6606, 4450, 5286, 4522, 5825, 3788, 4391, 3021, 3812, 2485, 3575, 3016, 5027, 3986, 5267, 3773, 4533, 3142, 5255, 4446, 5715, 5202, 6365, 5681, 6240, 5556, 6137, 4781, 5282, 4775, 5247, 4250, 4925, 4032, 5459, 4253, 4772, 3306, 3797, 3098, 5091, 3740, 6719, 5649, 6424, 5125, 7020, 6539, 7228, 5916, 6904, 6153, 7180, 6167, 6696, 5199, 5690, 4474, 5265, 4530, 5209, 4672, 6237, 5695, 6624, 5943, 8599, 7830, 8758, 8251, 8750, 7893, 9889, 9345, 10167, 9501, 10256, 7274, 7901, 7040, 8137, 7418, 7907, 7400, 8532, 7375, 9378, 8630, 9337, 7073, 8116, 6219, 7218, 6384, 7249, 6643, 7488, 5988, 6577, 5422, 7706, 7209, 8710, 7068, 7830, 6771, 8414, 7415, 7959, 7261, 8152, 7558, 10393, 8250, 10328, 8780, 9477, 8281, 9167, 8386, 9209, 7988, 8643, 7670, 8305, 5904, 6425, 5074, 6035, 5381, 6164, 4760, 5526, 4555, 6103, 5653, 6198, 5471, 5981, 4008, 4715, 3411, 5651, 5090, 5926, 5375, 6049, 5492, 6484, 4808, 5460, 4506, 5030, 3845, 4867, 4413, 5141, 4044, 6182, 5718, 7135, 6020, 6916, 5450, 6137, 5255, 6135, 5597, 6267, 5565, 6481, 5618, 6797, 6344, 7476, 6268, 6789, 6232, 7999, 7306, 9807, 8727, 9219, 7987, 9783, 9275, 9859, 8207, 8804, 7664, 8532, 7818, 8546, 7384, 8658, 7900, 9049, 8419, 9309]
        self.assertEqual(actual, expected)


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
