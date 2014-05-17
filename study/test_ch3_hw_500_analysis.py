###
### python libraries
###

from collections import Counter
import unittest

###
### project libraries
###

import ch3_hw_500_analysis as ANA

###
### test cases
###

class Ch3HwAnalysisTest(unittest.TestCase):
    def test_read_source(self):
        lines = ANA.read_source()
        self.assertEqual(len(lines), 1034)


    def test_parse_index_type(self):
        lines = ANA.read_source()
        records = ANA.parse_records(lines)
        types = [r['type'] for r in records]
        counter = Counter(types)
        self.assertEqual(counter['^'], 59)
        self.assertEqual(counter['+'], 135)


    def test_parse_point_numbers(self):
        lines = ANA.read_source()
        records = ANA.parse_records(lines)
        for r in records:
            _eval = len(r['points']) > 0
            err_msg = "index %d has no points record" % r['index']
            self.assertTrue(_eval, err_msg)


    def test_count_view_point_reach(self):
        lines = ANA.read_source()
        records = ANA.parse_records(lines)
        c = ANA.count_view_point_reach(records[0])
        self.assertEqual(c, 2)
        c = ANA.count_view_point_reach(records[1])
        self.assertEqual(c, 2)
        c = ANA.count_view_point_reach(records[2])
        self.assertEqual(c, 2)
        c = ANA.count_view_point_reach(records[3])
        self.assertEqual(c, 1)


###
### main procedure
###

if __name__ == '__main__':
    unittest.main()
