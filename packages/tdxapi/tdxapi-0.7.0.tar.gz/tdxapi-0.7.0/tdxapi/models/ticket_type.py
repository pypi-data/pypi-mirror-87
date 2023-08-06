import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_uid


@attr.s(kw_only=True)
class TicketType(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Tickets.TicketType"

    #: The ID of the ticket type.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The ID of the ticketing application associated with the type.
    app_id = attr.ib(default=None, metadata={"tdx_name": "AppID"})

    #: The name of the ticketing application associated with the type.
    app_name = attr.ib(default=None, metadata={"tdx_name": "AppName"})

    #: The name of the ticket type.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The description of the ticket type.
    description = attr.ib(default=None, metadata={"tdx_name": "Description"})

    #: The ID of the category associated with the ticket type.
    category_id = attr.ib(default=None, metadata={"tdx_name": "CategoryID"})

    #: The name of the category associated with the ticket type.
    category_name = attr.ib(default=None, metadata={"tdx_name": "CategoryName"})

    #: The full name of the type, which includes the type category.
    full_name = attr.ib(default=None, metadata={"tdx_name": "FullName"})

    #: The active status of the ticket type.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: The UID of the reviewing user associated with the ticket type.
    reviewer_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ReviewerUid"}
    )

    #: The full name of the reviewing user associated with the ticket type.
    reviewer_full_name = attr.ib(
        default=None, metadata={"tdx_name": "ReviewerFullName"}
    )

    #: The email address of the reviewing user associated with the ticket type.
    reviewer_email = attr.ib(default=None, metadata={"tdx_name": "ReviewerEmail"})

    #: The ID of the reviewing group associated with the ticket task.
    reviewing_group_id = attr.ib(
        default=None, metadata={"tdx_name": "ReviewingGroupID"}
    )

    #: The name of the reviewing group associated with the ticket task.
    reviewing_group_name = attr.ib(
        default=None, metadata={"tdx_name": "ReviewingGroupName"}
    )

    #: Whether the reviewing resource(s) (and other addresses, if specified) should be
    #: notified of any new tickets that are created with this type (or later changed to
    #: this type).
    notify_reviewer = attr.ib(default=None, metadata={"tdx_name": "NotifyReviewer"})

    #: The other email addresses to notify of incoming tickets when reviewer
    #: notification is enabled.
    other_notification_email_addresses = attr.ib(
        default=None, metadata={"tdx_name": "OtherNotificationEmailAddresses"}
    )

    #: The ID of the default SLA to use when tickets are created with this type.
    default_sla_id = attr.ib(default=None, metadata={"tdx_name": "DefaultSLAID"})

    #: The name of the default SLA to use when tickets are created with this type.
    default_sla_name = attr.ib(default=None, metadata={"tdx_name": "DefaultSLAName"})

    #: The active status of the default SLA to use when tickets are created with this
    #: type.
    default_sla_is_active = attr.ib(
        default=None, metadata={"tdx_name": "DefaultSLAIsActive"}
    )

    #: The ID of the workspace associated with the ticket type.
    workspace_id = attr.ib(default=None, metadata={"tdx_name": "WorkspaceID"})

    #: The name of the workspace associated with the ticket type.
    workspace_name = attr.ib(default=None, metadata={"tdx_name": "WorkspaceName"})
