import attr

from tdxapi.enums.sla_start_basis import SlaStartBasis
from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class SlaAssignmentOptions(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Tickets.SlaAssignmentOptions"

    #: The ID of the SLA to be assigned to the ticket.
    new_sla_id = attr.ib(default=None, metadata={"tdx_name": "NewSlaID"})

    #: The SLA deadline start basis. The default for this property will be the
    #: SlaStartBasis.CurrentDateTime option. Review the documentation for this property
    #: for all SLA start basis options.
    start_basis = attr.ib(
        default=None, converter=SlaStartBasis, metadata={"tdx_name": "StartBasis"}
    )

    #: Whether or not to cascade the SLA assignment to child tickets.
    should_cascade = attr.ib(default=None, metadata={"tdx_name": "ShouldCascade"})

    #: The email addresses to notify, associated with the SLA assignment feed entry.
    notify = attr.ib(default=attr.Factory(list), metadata={"tdx_name": "Notify"})

    #: The comments of the SLA assignment feed entry.
    comments = attr.ib(default=None, metadata={"tdx_name": "Comments"})
