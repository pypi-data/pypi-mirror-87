from enum import Enum


class UnmetConstraintSearchType(Enum):
    """A bit flag enumeration for indicating unmet constraints to filter on."""

    __tdx_type__ = "TeamDynamix.Api.Tickets.UnmetConstraintSearchType"

    #: Indicates that no filtering on unmet constraints should be performed.
    NONE = 0

    #: Indicates that filtering on an unmet "Respond By" constraint should be performed.
    RESPONSE = 1

    #: Indicates that filtering on an unmet "Resolve By" constraint should be performed.
    RESOLUTION = 2
