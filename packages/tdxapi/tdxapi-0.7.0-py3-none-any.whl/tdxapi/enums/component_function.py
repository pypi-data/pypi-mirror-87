from enum import Enum


class ComponentFunction(Enum):
    """Component extraction functions that can be applied to a report column."""

    __tdx_type__ = "TeamDynamix.Api.Reporting.ComponentFunction"

    #: Indicates that no component function should be applied.
    NONE = 0

    #: Indicates that the year should be extracted from a date/time value.
    YEAR = 1

    #: Indicates that the month and year should be extracted from a date/time value.
    MONTH_YEAR = 2

    #: Indicates that the week and year should be extracted from a date/time value.
    WEEK_YEAR = 3
