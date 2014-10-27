"""
common datetime conversions
"""

import logging
import datetime
from calendar import timegm
import dateutil.parser


logger = logging.getLogger(__name__)

def total_seconds(td):
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6

ZERO = datetime.timedelta(0)
class UTC(datetime.tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO


def unixts_to_dt(timestamp):
    """convert utc unix timestamp to datetime"""
    return datetime.datetime.utcfromtimestamp(timestamp)

def dt_to_unixts(dt):
    """convert datetime to unix timestamp"""
    return timegm(dt.timetuple()) + (dt.microsecond / 10.0 ** 6)

def isodateformat(value):
    """Return the iso formatted year-month-day only"""
    return value.strftime('%Y-%m-%d')

def isoformat(value):
    return value.strftime('%Y-%m-%dT%H:%M:%S%z')

def datetime_from_string(v, default_value=None):
    """Try to parse the value to get a datetime object.

    Normalizes the result to UTC if it contains timezone
    information.
    If v is None or empty, return None or default_value

    :param v: date string value
    :param default_value: if the parse fails return this
    :returns: datetime
    """
    if isinstance(v, datetime.datetime):
        return v

    if v:
        try:
            aware_date = dateutil.parser.parse(v)
            if aware_date.tzinfo is not None:
                aware_date = aware_date - aware_date.utcoffset()
                aware_date = aware_date.replace(tzinfo = None)
            return aware_date
        except ValueError:
            pass
        except TypeError, te:
            logger.warn("Parsing date %s, %s", v, te)

    if default_value:
        return default_value

