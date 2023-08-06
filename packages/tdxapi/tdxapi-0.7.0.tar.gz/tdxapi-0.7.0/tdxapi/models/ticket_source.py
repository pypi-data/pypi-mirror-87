import attr

from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class TicketSource(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Tickets.TicketSource"

    #: The ID of the ticket source.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The name of the ticket source.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The description of the ticket source.
    description = attr.ib(default=None, metadata={"tdx_name": "Description"})

    #: The active status of the ticket source.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})
