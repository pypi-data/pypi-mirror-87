import attr

from tdxapi.enums.conflict_type import ConflictType
from tdxapi.enums.ticket_task_type import TicketTaskType
from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime, to_uid


@attr.s(kw_only=True)
class TicketTask(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Tickets.TicketTask"

    #: The ID of the task.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The ID of the ticket associated with the task.
    ticket_id = attr.ib(default=None, metadata={"tdx_name": "TicketID"})

    #: The title of the task.
    title = attr.ib(default=None, metadata={"tdx_name": "Title"})

    #: The description of the task.
    description = attr.ib(default=None, metadata={"tdx_name": "Description"})

    #: The active status of the ticket task.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: The start date of the task.
    start_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "StartDate"}
    )

    #: The end date of the task.
    end_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "EndDate"}
    )

    #: The expected duration, in operational minutes, of the task.
    complete_within_minutes = attr.ib(
        default=None, metadata={"tdx_name": "CompleteWithinMinutes"}
    )

    #: The estimated minutes of the task.
    estimated_minutes = attr.ib(default=None, metadata={"tdx_name": "EstimatedMinutes"})

    #: The time, in minutes, entered against the task.
    actual_minutes = attr.ib(default=None, metadata={"tdx_name": "ActualMinutes"})

    #: The percent complete of the task.
    percent_complete = attr.ib(default=None, metadata={"tdx_name": "PercentComplete"})

    #: The created date of the task.
    created_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CreatedDate"}
    )

    #: The UID of the user who created the task.
    created_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "CreatedUid"}
    )

    #: The full name of the user who created the task.
    created_full_name = attr.ib(default=None, metadata={"tdx_name": "CreatedFullName"})

    #: The email address of the user who created the task.
    created_email = attr.ib(default=None, metadata={"tdx_name": "CreatedEmail"})

    #: The last modified date of the task.
    modified_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "ModifiedDate"}
    )

    #: The UID of the user who last modified the task.
    modified_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ModifiedUid"}
    )

    #: The full name of the user who last modified the task.
    modified_full_name = attr.ib(
        default=None, metadata={"tdx_name": "ModifiedFullName"}
    )

    #: The completed date of the task.
    completed_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CompletedDate"}
    )

    #: The UID of the user who completed the task.
    completed_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "CompletedUid"}
    )

    #: The full name of the user who completed the task.
    completed_full_name = attr.ib(
        default=None, metadata={"tdx_name": "CompletedFullName"}
    )

    #: The UID of the user responsible for the task.
    responsible_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ResponsibleUid"}
    )

    #: The full name of the user responsible for the task.
    responsible_full_name = attr.ib(
        default=None, metadata={"tdx_name": "ResponsibleFullName"}
    )

    #: The email address of the user responsible for the task.
    responsible_email = attr.ib(default=None, metadata={"tdx_name": "ResponsibleEmail"})

    #: The ID of the group responsible for the task.
    responsible_group_id = attr.ib(
        default=None, metadata={"tdx_name": "ResponsibleGroupID"}
    )

    #: The name of the group responsible for the task.
    responsible_group_name = attr.ib(
        default=None, metadata={"tdx_name": "ResponsibleGroupName"}
    )

    #: The ID of the predecessor associated with the task.
    predecessor_id = attr.ib(default=None, metadata={"tdx_name": "PredecessorID"})

    #: The title of the predecessor associated with the task.
    predecessor_title = attr.ib(default=None, metadata={"tdx_name": "PredecessorTitle"})

    #: The order in which the task should be displayed in the list of the ticket's
    #: tasks/activities.
    order = attr.ib(default=None, metadata={"tdx_name": "Order"})

    #: The type of the task. This indicates if this is a regular ticket task, a
    #: scheduled maintenance activity, or something else.
    type = attr.ib(
        default=TicketTaskType.TICKET_TASK,
        converter=TicketTaskType,
        metadata={"tdx_name": "TypeID"},
    )

    #: The number of detected conflicts for this task.
    detected_conflict_count = attr.ib(
        default=None, metadata={"tdx_name": "DetectedConflictCount"}
    )

    #: The type of detected conflicts for this task.
    detected_conflict_types = attr.ib(
        default=ConflictType.NONE,
        converter=ConflictType,
        metadata={"tdx_name": "DetectedConflictTypes"},
    )

    #: The date the task was last scanned for conflicts.
    last_conflict_scan_date = attr.ib(
        default=None,
        converter=to_datetime,
        metadata={"tdx_name": "LastConflictScanDateUtc"},
    )

    #: The URI to retrieve the full details of the ticket task via the web API.
    uri = attr.ib(default=None, metadata={"tdx_name": "Uri"})
