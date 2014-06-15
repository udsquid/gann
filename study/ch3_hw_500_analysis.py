"""
This analysis script can read records from file,
and output following Gann's analysis:
    # number of view points pass through
"""

###
### python library
###

from collections import Counter
from itertools import tee, izip
import re

###
### constants
###

START_PATTERN = """
    ;                 # start sign
    \s+               # inner spaces
    (?P<index>\d+)    # index
    \s*               # inner spaces
    ,                 # delimiter
    \s+               # inner spaces
    (?P<type>[+^])    # point type"""

POINT_PATTERN = """
    (?P<value>\d+)           # point value
    \)\)\)                   # end of lisp
    (?P<length>\d+)          # length
    \s*                      # inner spaces
    (
        ;                    # attributes start sign
        \s*                  # inner spaces
        (?P<mark>[\*\&]+)    # point markers
    )?                       # can be zero or one
"""

###
### helper functions
###

def print_header(text, width=30):
    print "=" * width
    print text.center(width)
    print "=" * width


def print_footer():
    print


def pairwise(iterable):
    """i -> (i0, i1), (i1, i2), (i2, i3), ..."""
    iter1, iter2 = tee(iterable)
    next(iter2)
    return izip(iter1, iter2)


###
### main procedure
###

def count_view_point_reach(record):
    count = 0
    for p in record['points']:
        assert p['attributes'], "no attributes in record: %s" % record
        if 'view' in p['attributes']:
            count += 1
        if 'end' in p['attributes']:
            break
    return count


def read_source():
    with open('chapter3-homework-500.el') as source:
        return source.readlines()


def parse_records(lines):
    """
    Parse source data into following format:
    {'index': DIGIT,
     'type': '^' | '+',
     'points': [{'value': DIGIT,
                 'length': DIGIT,
                 'attributes': '*' | '*&'}]}
    * 'value' is the point value on gann chart
    * 'length' is the distance from last high/low point
    * '^' is for angle, '+' is for cross
    * '*' is for end point, '*&' is for end point on view point
    """
    records = list()
    while lines:
        _index, _type = parse_start_line(lines)
        _points = parse_point_lines(lines)
        record = {'index': int(_index),
                  'type': _type,
                  'points': _points}
        records.append(record)
    return records


def parse_start_line(lines):
    line = lines.pop(0)
    line = line.strip()
    match_result = re.match(START_PATTERN, line, re.X)
    assert match_result, \
        "not a start line: %s" % line
    return match_result.groups()


def parse_point_lines(lines):
    points = list()
    while lines:
        line = lines.pop(0)
        line = line.strip()
        search_result = re.search(POINT_PATTERN, line, re.X)
        if not search_result:
            lines.insert(0, line)
            break
        groups = search_result.groupdict()
        # parse attributes
        attr_list = []
        if groups['mark']:
            if '*' in groups['mark']:
                attr_list.append('end')
            if '&' in groups['mark']:
                attr_list.append('view')
        else:
            attr_list.append('view')
        # push this point info
        point = {'value': int(groups['value']),
                 'length': int(groups['length']),
                 'attributes': attr_list}
        points.append(point)
    return points


def collect_view_point_reach(records):
    stat_angle = []
    stat_cross = []
    for r in records:
        c = count_view_point_reach(r)
        if r['type'] == '^':
            stat_angle.append(c)
        elif r['type'] == '+':
            stat_cross.append(c)
        else:
            err_msg = "unknown type '{type}' for index {index}".format(**r)
            assert False, err_msg
    return stat_angle, stat_cross


def print_reach_count(stat):
    reach_counter = Counter(stat)
    reach_min = min(reach_counter)
    reach_max = max(reach_counter)
    result = ''
    for number in range(reach_min, reach_max+1):
        count = reach_counter[number]
        result += "%d " % count
    print "    Reach count: %s" % result


def print_most_common(stat, number=3, indent=4):
    counter = Counter(stat)
    print "%sMost common: %s" % (" "*indent,
                                 counter.most_common(number))


def print_view_point_reach(records):
    stat_angle, stat_cross = collect_view_point_reach(records)
    print_header("View points reach")
    print "Angle:"
    print_reach_count(stat_angle)
    print_most_common(stat_angle)
    print "Cross:"
    print_reach_count(stat_cross)
    print_most_common(stat_cross)
    print_footer()


def print_amplitude_population():
    print_header("Amplitude population")
    with open('../data/taiex_high_low.txt') as source:
        lines = source.readlines()
        indexes = []
        for line in lines:
            day, index = line.split(',')
            index = int(index)
            indexes.append(index)
    assert len(indexes) == 487, "wrong number of indexes"
    pairs = pairwise(indexes)
    less_than_500_count = 0
    more_than_500_count = 0
    for v1, v2 in pairs:
        diff = abs(v1-v2)
        if diff < 500:
            less_than_500_count += 1
        else:
            more_than_500_count += 1
    print "Less than 500: %d" % less_than_500_count
    print "More than 500: %d" % more_than_500_count
    print_footer()


def print_continuous_angle_stat(records):
    print_header("Consecutive angle statistics")
    consecutive_counts = []
    angles = 0
    prev_is_angle = False
    for r in records:
        if r['type'] == '+' and prev_is_angle:
            consecutive_counts.append(angles)
            prev_is_angle = False
            angles = 0
            continue
        if r['type'] == '^':
            prev_is_angle = True
            angles += 1
            continue
    if prev_is_angle:
        consecutive_counts.append(angles)
    print "Consecutive counts: %s" % consecutive_counts
    histogram = Counter(consecutive_counts)
    print "Histogram: %s" % histogram.most_common()
    print_footer()


def print_view_points_length(record, n=None):
    """
    Print the length of view points, if 'n' is given
    then first nth view points will be printed out.
    """
    assert isinstance(n, int), "'n' must to be an integer"
    for index, point in enumerate(record['points']):
        if index == n:
            break
        # meet end point before nth point, stop
        if 'end' in point['attributes']:
            # if end point is on view point, print and stop
            if 'view' in point['attributes']:
                print "%4d" % point['length'],
            break
        print "%4d" % point['length'],
    print ""


def print_distance_population(records):
    print_header("Distance population")
    for record in records:
        print "{index:5d} {type}".format(**record),
        if record['type'] == '^':
            print_view_points_length(record, n=4)
        elif record['type'] == '+':
            print_view_points_length(record, n=2)
        else:
            assert False, "unsupported type: %s" % record['type']
    print_footer()


def main():
    lines = read_source()
    records = parse_records(lines)
    print_view_point_reach(records)
    print_amplitude_population()
    print_continuous_angle_stat(records)
    print_distance_population(records)
    print '-'*30
    print "Done!"


# what is my spec?
# -> can output series of Gann analysis
# -> each index should contain at least one point
if __name__ == '__main__':
    main()
