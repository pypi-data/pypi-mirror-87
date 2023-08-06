from enum import Enum


class ColumnDataType(Enum):
    """Types of data that a column can contain."""

    __tdx_type__ = "TeamDynamix.Api.Reporting.ColumnDataType"

    #: Indicates that the column's values are of no specific type.
    GENERIC_DATA = 0

    #: Indicates that the column's values are strings.
    STRING = 1

    #: Indicates that the column's values are whole numbers.
    INTEGER = 2

    #: Indicates that the column's values are decimal numbers with potentially a
    #: fractional component.
    DECIMAL = 3

    #: Indicates that the column's values are currency values with potentially a
    #: fractional component.
    CURRENCY = 4

    #: Indicates that the column's values are decimal percentage values (where 1.0
    #: represents 100%).
    PERCENTAGE = 5

    #: Indicates that the column's values are date-only values.
    DATE = 6

    #: Indicates that the column's values are date and time values.
    DATE_AND_TIME = 7

    #: Indicates that the column's values are true/false Boolean values.
    BOOLEAN = 8

    #: Indicates that the column's values are timespans represented as a number of
    #: hours.
    TIME_SPAN = 9

    #: Indicates that the column's values are names of project health choices.
    PROJECT_HEALTH = 10

    #: Indicates that the column's values are sanitized HTML strings.
    HTML = 11
