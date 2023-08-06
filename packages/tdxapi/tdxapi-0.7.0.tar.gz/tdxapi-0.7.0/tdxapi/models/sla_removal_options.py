import attr

from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class SlaRemovalOptions(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Tickets.SlaRemovalOptions"

    #: Whether or not to cascade the SLA removal to child tickets.
    should_cascade = attr.ib(default=None, metadata={"tdx_name": "ShouldCascade"})

    #: The email addresses to notify, associated with the SLA removal feed entry.
    notify = attr.ib(default=attr.Factory(list), metadata={"tdx_name": "Notify"})

    #: The comments of the SLA removal feed entry.
    comments = attr.ib(default=None, metadata={"tdx_name": "Comments"})
