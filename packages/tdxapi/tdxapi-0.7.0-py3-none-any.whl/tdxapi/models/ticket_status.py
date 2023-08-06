import attr

from tdxapi.enums.status_class import StatusClass
from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class TicketStatus(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Tickets.TicketStatus"

    #: The ID of the ticket status.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The ID of the ticketing application associated with the ticket status.
    app_id = attr.ib(default=None, metadata={"tdx_name": "AppID"})

    #: The name of the ticketing application associated with the ticket status.
    app_name = attr.ib(default=None, metadata={"tdx_name": "AppName"})

    #: The name of the ticket status.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The description of the ticket status.
    description = attr.ib(default=None, metadata={"tdx_name": "Description"})

    #: The order of the ticket status when displayed in a list.
    order = attr.ib(default=None, metadata={"tdx_name": "Order"})

    #: The status class associated with the ticket status.
    status_class = attr.ib(
        default=StatusClass.NONE,
        converter=StatusClass,
        metadata={"tdx_name": "StatusClass"},
    )

    #: The active status of the ticket status.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: The default status of the ticket status.
    is_default = attr.ib(default=None, metadata={"tdx_name": "IsDefault"})
