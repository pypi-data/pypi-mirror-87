from enum import Enum


class AggregateFunction(Enum):
    """Aggregate functions that can be applied to a report column."""

    __tdx_type__ = "TeamDynamix.Api.Reporting.AggregateFunction"

    #: Indicates that no aggregation should be performed.
    NONE = 0

    #: Indicates that an average of referenced column values should be calculated.
    AVERAGE = 1

    #: Indicates that a count of referenced column values should be calculated.
    COUNT = 2

    #: Indicates that the maximum referenced column value should be calculated.
    MAXIMUM = 3

    #: Indicates that the minimum referenced column value should be calculated.
    MINIMUM = 4

    #: Indicates that a total of referenced column values should be calculated.
    SUM = 5
