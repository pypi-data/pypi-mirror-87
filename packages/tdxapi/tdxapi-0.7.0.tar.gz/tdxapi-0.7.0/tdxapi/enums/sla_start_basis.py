from enum import Enum


class SlaStartBasis(Enum):
    """Describes the SLA deadline start basis options to be applied to a ticket."""

    __tdx_type__ = "TeamDynamix.Api.Tickets.SlaStartBasis"

    #: Determine SLA deadlines from the current date and time.
    CURRENT_DATE_TIME = 0

    #: Determine SLA deadlines from the time the ticket was created.
    TICKET_CREATION_DATE_TIME = 1
