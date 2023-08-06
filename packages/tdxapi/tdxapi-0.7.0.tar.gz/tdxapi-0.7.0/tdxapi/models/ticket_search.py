import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime, to_uid
from tdxapi.models.custom_attribute_list import CustomAttributeList


@attr.s(kw_only=True)
class TicketSearch(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Tickets.TicketSearch"

    #: The ticket classifications to filter on. Use Ticket to perform no classification
    #: filtering.
    ticket_classifications = attr.ib(
        default=attr.Factory(list),
        metadata={"tdx_name": "TicketClassification"},
    )

    #: The maximum number of results to return.
    max_results = attr.ib(default=0, metadata={"tdx_name": "MaxResults"})

    #: The ticket ID to filter on.
    ticket_id = attr.ib(default=None, metadata={"tdx_name": "TicketID"})

    #: The parent ticket ID to filter on.
    parent_ticket_id = attr.ib(default=None, metadata={"tdx_name": "ParentTicketID"})

    #: The search text to filter on.
    search_text = attr.ib(default=None, metadata={"tdx_name": "SearchText"})

    #: The status IDs to filter on.
    status_ids = attr.ib(default=attr.Factory(list), metadata={"tdx_name": "StatusIDs"})

    #: The historical status IDs to filter on.
    past_status_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "PastStatusIDs"}
    )

    #: The status class IDs to filter on.
    status_classes = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "StatusClassIDs"}
    )

    #: The priority IDs to filter on.
    priority_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "PriorityIDs"}
    )

    #: The urgency IDs to filter on.
    urgency_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "UrgencyIDs"}
    )

    #: The impact IDs to filter on.
    impact_ids = attr.ib(default=attr.Factory(list), metadata={"tdx_name": "ImpactIDs"})

    #: The account/department IDs to filter on.
    account_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "AccountIDs"}
    )

    #: The ticket type IDs to filter on.
    type_ids = attr.ib(default=attr.Factory(list), metadata={"tdx_name": "TypeIDs"})

    #: The source IDs to filter on.
    source_ids = attr.ib(default=attr.Factory(list), metadata={"tdx_name": "SourceIDs"})

    #: The minimum updated date to filter on.
    updated_date_from = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "UpdatedDateFrom"}
    )

    #: The maximum updated date to filter on.
    updated_date_to = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "UpdatedDateTo"}
    )

    #: The UID of the updating user to filter on.
    updated_by_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "UpdatedByUid"}
    )

    #: The minimum last modified date to filter on.
    modified_date_from = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "ModifiedDateFrom"}
    )

    #: The maximum last modified date to filter on.
    modified_date_to = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "ModifiedDateTo"}
    )

    #: The UID of the last modifying user to filter on.
    modified_by_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ModifiedByUid"}
    )

    #: The minimum start date to filter on.
    start_date_from = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "StartDateFrom"}
    )

    #: The maximum start date to filter on.
    start_date_to = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "StartDateTo"}
    )

    #: The minimum end date to filter on.
    end_date_from = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "EndDateFrom"}
    )

    #: The maximum end date to filter on.
    end_date_to = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "EndDateTo"}
    )

    #: The minimum responded date to filter on.
    responded_date_from = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "RespondedDateFrom"}
    )

    #: The maximum responded date to filter on.
    responded_date_to = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "RespondedDateTo"}
    )

    #: The UID of the responding user to filter on.
    responded_by_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "RespondedByUid"}
    )

    #: The minimum closed date to filter on.
    closed_date_from = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "ClosedDateFrom"}
    )

    #: The maximum closed date to filter on.
    closed_date_to = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "ClosedDateTo"}
    )

    #: The UID of the closing person to filter on.
    closed_by_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ClosedByUid"}
    )

    #: The minimum SLA "Respond By" deadline to filter on.
    respond_by_date_from = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "RespondByDateFrom"}
    )

    #: The maximum SLA "Respond By" deadline to filter on.
    respond_by_date_to = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "RespondByDateTo"}
    )

    #: The minimum SLA "Resolve By" deadline to filter on.
    close_by_date_from = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CloseByDateFrom"}
    )

    #: The maximum SLA "Resolve By" deadline to filter on.
    close_by_date_to = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CloseByDateTo"}
    )

    #: The minimum created date to filter on.
    created_date_from = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CreatedDateFrom"}
    )

    #: The maximum created date to filter on.
    created_date_to = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CreatedDateTo"}
    )

    #: The UID of the creating user to filter on.
    created_by_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "CreatedByUid"}
    )

    #: The minimum age to filter on.
    days_old_from = attr.ib(default=None, metadata={"tdx_name": "DaysOldFrom"})

    #: The maximum age to filter on.
    days_old_to = attr.ib(default=None, metadata={"tdx_name": "DaysOldTo"})

    #: The UIDs of the responsible users to filter on.
    responsibility_uids = attr.ib(
        default=attr.Factory(list),
        converter=to_uid,
        metadata={"tdx_name": "ResponsibilityUids"},
    )

    #: The IDs of the responsible groups to filter on.
    responsibility_group_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "ResponsibilityGroupIDs"}
    )

    #: The filter to use for responsible_uids and responsible_group_ids with regards to
    #: ticket tasks.
    responsibility_completed_task = attr.ib(
        default=None, metadata={"tdx_name": "CompletedTaskResponsibilityFilter"}
    )

    #: The UIDs of the primarily-responsible users to filter on.
    primary_responsibility_uids = attr.ib(
        default=attr.Factory(list),
        converter=to_uid,
        metadata={"tdx_name": "PrimaryResponsibilityUids"},
    )

    #: The IDs of the primarily-responsible groups to filter on.
    primary_responsibility_group_ids = attr.ib(
        default=attr.Factory(list),
        metadata={"tdx_name": "PrimaryResponsibilityGroupIDs"},
    )

    #: The SLA IDs to filter on.
    sla_ids = attr.ib(default=attr.Factory(list), metadata={"tdx_name": "SlaIDs"})

    #: The SLA violation status to filter on.
    sla_violated = attr.ib(default=None, metadata={"tdx_name": "SlaViolationStatus"})

    #: The unmet SLA deadlines to filter on.
    sla_unmet_constraints = attr.ib(
        default=None,
        metadata={"tdx_name": "SlaUnmetConstraints"},
    )

    #: The associated Knowledge Base article IDs to filter on.
    article_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "KBArticleIDs"}
    )

    #: The assignment status to filter on.
    is_assigned = attr.ib(default=None, metadata={"tdx_name": "AssignmentStatus"})

    #: The task conversion status to filter on.
    converted_to_task = attr.ib(default=None, metadata={"tdx_name": "ConvertedToTask"})

    #: The UID of the reviewing user to filter on.
    reviewer_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ReviewerUid"}
    )

    #: The requestor UIDs to filter on.
    requestor_uids = attr.ib(
        default=attr.Factory(list),
        converter=to_uid,
        metadata={"tdx_name": "RequestorUids"},
    )

    #: The text to perform a LIKE search on the requestor's full name.
    requestor_name_like = attr.ib(
        default=None, metadata={"tdx_name": "RequestorNameSearch"}
    )

    #: The text to perform a LIKE search on the requestor's email address.
    requestor_email_like = attr.ib(
        default=None, metadata={"tdx_name": "RequestorEmailSearch"}
    )

    #: The text to perform a LIKE search on the requestor's phone number.
    requestor_phone_like = attr.ib(
        default=None, metadata={"tdx_name": "RequestorPhoneSearch"}
    )

    #: The IDs of the associated configuration items to filter on. To be included in the
    #: search results, a ticket must be associated with one or more of the listed CIs.
    configuration_item_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "ConfigurationItemIDs"}
    )

    #: The IDs of the associated CIs to exclude on. To be included in the search
    #: results, a ticket must NOT be associated with any of the listed CIs.
    exclude_configuration_item_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "ExcludeConfigurationItemIDs"}
    )

    #: The "On Hold" status to filter on.
    is_on_hold = attr.ib(default=None, metadata={"tdx_name": "IsOnHold"})

    #: The minimum "Goes Off Hold" date to filter on.
    goes_off_hold_from = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "GoesOffHoldFrom"}
    )

    #: The maximum "Goes Off Hold" date to filter on.
    goes_off_hold_to = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "GoesOffHoldTo"}
    )

    #: The associated location IDs to filter on.
    location_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "LocationIDs"}
    )

    #: The associated location room IDs to filter on.
    location_room_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "LocationRoomIDs"}
    )

    #: The associated service IDs to filter on.
    service_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "ServiceIDs"}
    )

    #: The associated custom attributes to filter on.
    custom_attributes = attr.ib(
        default=attr.Factory(CustomAttributeList),
        converter=CustomAttributeList.from_data,
        metadata={"tdx_name": "CustomAttributes"},
    )

    #: Whether the returned tickets should have a reference code.
    has_reference_code = attr.ib(
        default=None, metadata={"tdx_name": "HasReferenceCode"}
    )
