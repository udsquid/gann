"""
This analysis script can read records from file,
and output following Gann's analysis:
    # number of view points pass through
"""

###
### python library
###

from collections import Counter
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
    records = list()
    while lines:
        i, t = parse_start_line(lines)
        p = parse_point_lines(lines)
        record = {'index': int(i),
                  'type': t,
                  'points': p}
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


def print_header(text, width=30):
    print "=" * width
    print text.center(width)
    print "=" * width


def print_reach_count(stat):
    reach_counter = Counter(stat)
    reach_min = min(reach_counter)
    reach_max = max(reach_counter)
    result = ''
    for number in range(reach_min, reach_max+1):
        count = reach_counter[number]
        result += "%d " % count
    print "    Reach count: %s" % result


def print_most_common(stat):
    reach_counter = Counter(stat)
    print "    Most common: %s" % reach_counter.most_common(3)


def print_view_point_reach(stat_angle, stat_cross):
    print_header("View points reach")
    print "Angle:"
    print_reach_count(stat_angle)
    print_most_common(stat_angle)
    print "Cross:"
    print_reach_count(stat_cross)
    print_most_common(stat_cross)


def main():
    lines = read_source()
    records = parse_records(lines)
    stat_angle, stat_cross = collect_view_point_reach(records)
    print_view_point_reach(stat_angle, stat_cross)
    print '-'*30
    print "Done!"


# what is my spec?
# -> can output series of Gann analysis
# -> each index should contain at least one point
if __name__ == '__main__':
    main()
