"""
This module provides utilities to parse and convert times.
"""

#
# python libraries
#
from datetime import datetime, time
from django.utils import timezone
import django.utils.dateparse as PARSER
import pytz


#
# module methods
#
def parse_datetime(value):
    """
    Parse datetime string to datetime object. Available format is
    following date_re and datetime_re in django.utils.dateparse module.
    Return 'None' if not match those formats.

    Examples:
        >>> d1 = parse_datetime('2014-11-23')
        >>> type(d1)
        <type 'datetime.datetime'>
        >>> print d1
        2014-11-23 00:00:00

        >>> dt1 = parse_datetime('2014-11-23 9:3')
        >>> print dt1
        2014-11-23 09:03:00

        >>> dt2 = parse_datetime('2014-11-23 09:03:00')
        >>> print dt2
        2014-11-23 09:03:00
    """
    if PARSER.date_re.match(value):
        date_obj = PARSER.parse_date(value)
        return datetime.combine(date_obj, time.min)
    elif PARSER.datetime_re.match(value):
        return PARSER.parse_datetime(value)
    else:
        return None


def to_aware(naive):
    curr_tz = timezone.get_current_timezone_name()
    return pytz.timezone(curr_tz).localize(naive)


def parse_to_aware(value):
    datetime_obj = parse_datetime(value)
    assert datetime_obj, "invalid datetime format: {}".format(value)
    return to_aware(datetime_obj)


def to_local(datetime_obj):
    curr_tz = timezone.get_current_timezone()
    return datetime_obj.astimezone(curr_tz)
