import attr

from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class TicketStatusSearch(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Tickets.TicketStatusSearch"

    #: The search text to filter on. When set, results will be ordered by their text
    #: relevancy.
    search_text = attr.ib(default=None, metadata={"tdx_name": "SearchText"})

    #: The active status to filter on.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: The default status to filter on.
    is_default = attr.ib(default=None, metadata={"tdx_name": "IsDefault"})

    #: The status class to filter on.
    status_class = attr.ib(default=None, metadata={"tdx_name": "StatusClass"})

    #: The "Requires Goes Off Hold" status to filter on.
    requires_goes_off_hold = attr.ib(
        default=None, metadata={"tdx_name": "RequiresGoesOffHold"}
    )
