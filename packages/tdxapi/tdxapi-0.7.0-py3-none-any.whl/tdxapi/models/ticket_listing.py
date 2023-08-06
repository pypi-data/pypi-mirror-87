import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime, to_uid


@attr.s(kw_only=True)
class TicketListing(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Tickets.TicketListing"

    #: The id of the ticket.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The title.
    title = attr.ib(default=None, metadata={"tdx_name": "Title"})

    #: The id of the application to which this ticket belongs.
    app_id = attr.ib(default=None, metadata={"tdx_name": "AppID"})

    #: The name of the application to which this ticket belongs.
    app_name = attr.ib(default=None, metadata={"tdx_name": "AppName"})

    #: The id of the ticket's classification.
    classification_id = attr.ib(default=None, metadata={"tdx_name": "ClassificationID"})

    #: The name of the ticket's classification.
    classification_name = attr.ib(
        default=None, metadata={"tdx_name": "ClassificationName"}
    )

    #: The status id.
    status_id = attr.ib(default=None, metadata={"tdx_name": "StatusID"})

    #: The status name.
    status_name = attr.ib(default=None, metadata={"tdx_name": "StatusName"})

    #: The account/department id.
    account_id = attr.ib(default=None, metadata={"tdx_name": "AccountID"})

    #: The account/department name.
    account_name = attr.ib(default=None, metadata={"tdx_name": "AccountName"})

    #: The type category id.
    type_category_id = attr.ib(default=None, metadata={"tdx_name": "TypeCategoryID"})

    #: The type category name.
    type_category_name = attr.ib(
        default=None, metadata={"tdx_name": "TypeCategoryName"}
    )

    #: The ticket type id.
    type_id = attr.ib(default=None, metadata={"tdx_name": "TypeID"})

    #: The ticket type name.
    type_name = attr.ib(default=None, metadata={"tdx_name": "TypeName"})

    #: The uid of the creator.
    created_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "CreatedUid"}
    )

    #: The created date.
    created_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CreatedDate"}
    )

    #: The full name of the creator.
    created_full_name = attr.ib(default=None, metadata={"tdx_name": "CreatedFullName"})

    #: The uid of the last person to modify the ticket.
    modified_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ModifiedUid"}
    )

    #: The last modified date.
    modified_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "ModifiedDate"}
    )

    #: The full name of the last person to modify the ticket.
    modified_full_name = attr.ib(
        default=None, metadata={"tdx_name": "ModifiedFullName"}
    )

    #: The uid of the requestor.
    contact_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ContactUid"}
    )

    #: The full name of the requestor.
    contact_full_name = attr.ib(default=None, metadata={"tdx_name": "ContactFullName"})

    #: The start date currently set on the ticket.
    start_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "StartDate"}
    )

    #: The end date currently set on the ticket.
    end_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "EndDate"}
    )

    #: The "respond by" sla deadline for the ticket.
    respond_by_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "RespondByDate"}
    )

    #: The "resolve by" sla deadline for the ticket.
    resolve_by_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "ResolveByDate"}
    )

    #: The date the ticket will go off hold.
    goes_off_hold_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "GoesOffHoldDate"}
    )

    #: A value indicating whether the ticket is archived.
    is_archived = attr.ib(default=None, metadata={"tdx_name": "IsArchived"})

    #: The priority identifier.
    priority_id = attr.ib(default=None, metadata={"tdx_name": "PriorityID"})

    #: The name of the priority.
    priority_name = attr.ib(default=None, metadata={"tdx_name": "PriorityName"})

    #: The location identifier.
    location_id = attr.ib(default=None, metadata={"tdx_name": "LocationID"})

    #: The name of the location.
    location_name = attr.ib(default=None, metadata={"tdx_name": "LocationName"})

    #: The location room identifier.
    location_room_id = attr.ib(default=None, metadata={"tdx_name": "LocationRoomID"})

    #: The name of the location room.
    location_room_name = attr.ib(
        default=None, metadata={"tdx_name": "LocationRoomName"}
    )
