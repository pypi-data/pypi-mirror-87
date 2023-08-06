"""Functions to automatically convert data using attr library."""

from dateutil import tz
from dateutil.parser import parse
from dateutil.utils import default_tzinfo


def to_datetime(value):
    """Convert TDX datetime string to Python DateTime."""
    if value is None or value[:4] == "0001":
        return None

    if isinstance(value, str):
        value = default_tzinfo(parse(value), tz.tzutc()).astimezone(tz.tzlocal())

    return value.replace(tzinfo=None)


def to_uid(value):
    """Check for TDX default UID value and return None instead."""
    empty_uid = "00000000-0000-0000-0000-000000000000"

    if value == empty_uid:
        return None

    if isinstance(value, list):
        return [v for v in value if v != empty_uid]

    return value
