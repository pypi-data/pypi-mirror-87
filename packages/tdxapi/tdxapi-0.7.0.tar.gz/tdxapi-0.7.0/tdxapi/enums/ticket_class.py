from enum import Enum


class TicketClass(Enum):
    """Describes the different classifications of tickets."""

    __tdx_type__ = "TeamDynamix.Api.Tickets.TicketClass"

    NONE = 0

    #: An "all tickets" classification for the purposes of filtering. Tickets should not
    #: be created or edited with this class.
    TICKET = 9

    #: An incident.
    INCIDENT = 32

    #: A major incident.
    MAJOR_INCIDENT = 77

    #: A problem.
    PROBLEM = 33

    #: A change.
    CHANGE = 34

    #: A release.
    RELEASE = 35

    #: A ticket template. Tickets should not be created or edited with this class.
    TICKET_TEMPLATE = 36

    #: A service request.
    SERVICE_REQUEST = 46
