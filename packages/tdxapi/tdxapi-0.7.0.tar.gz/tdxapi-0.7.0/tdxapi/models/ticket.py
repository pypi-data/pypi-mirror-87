import attr

from tdxapi.enums.article_status import ArticleStatus
from tdxapi.enums.status_class import StatusClass
from tdxapi.enums.ticket_class import TicketClass
from tdxapi.models.attachment import Attachment
from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime, to_uid
from tdxapi.models.custom_attribute_list import CustomAttributeList
from tdxapi.models.resource_item import ResourceItem
from tdxapi.models.ticket_task import TicketTask


@attr.s(kw_only=True)
class Ticket(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Tickets.Ticket"

    #: The ID of the ticket.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The ID of the parent associated with the ticket.
    parent_id = attr.ib(default=None, metadata={"tdx_name": "ParentID"})

    #: The title of the parent associated with the ticket.
    parent_title = attr.ib(default=None, metadata={"tdx_name": "ParentTitle"})

    #: The classification of the parent associated with the ticket.
    parent_classification = attr.ib(
        default=TicketClass.TICKET,
        converter=TicketClass,
        metadata={"tdx_name": "ParentClass"},
    )

    #: The ID of the ticket type associated with the ticket.
    type_id = attr.ib(default=None, metadata={"tdx_name": "TypeID"})

    #: The name of the ticket type associated with the ticket.
    type_name = attr.ib(default=None, metadata={"tdx_name": "TypeName"})

    #: The ID of the category associated with the ticket's type.
    type_category_id = attr.ib(default=None, metadata={"tdx_name": "TypeCategoryID"})

    #: The name of the category associated with the ticket's type.
    type_category_name = attr.ib(
        default=None, metadata={"tdx_name": "TypeCategoryName"}
    )

    #: The classification associated with the ticket.
    classification = attr.ib(
        default=TicketClass.TICKET,
        converter=TicketClass,
        metadata={"tdx_name": "Classification"},
    )

    #: The application-defined name of the classification associated with the ticket.
    classification_name = attr.ib(
        default=None, metadata={"tdx_name": "ClassificationName"}
    )

    #: The ID of the form associated with the ticket.
    form_id = attr.ib(default=None, metadata={"tdx_name": "FormID"})

    #: The name of the form associated with the ticket.
    form_name = attr.ib(default=None, metadata={"tdx_name": "FormName"})

    #: The title of the ticket.
    title = attr.ib(default=None, metadata={"tdx_name": "Title"})

    #: The description of the ticket.
    description = attr.ib(default=None, metadata={"tdx_name": "Description"})

    #: The URI to retrieve the full details of the ticket via the web API.
    uri = attr.ib(default=None, metadata={"tdx_name": "Uri"})

    #: The ID of the account/department associated with the ticket.
    account_id = attr.ib(default=None, metadata={"tdx_name": "AccountID"})

    #: The name of the account/department associated with the ticket.
    account_name = attr.ib(default=None, metadata={"tdx_name": "AccountName"})

    #: The ID of the ticket source associated with the ticket.
    source_id = attr.ib(default=None, metadata={"tdx_name": "SourceID"})

    #: The name of the ticket source associated with the ticket.
    source_name = attr.ib(default=None, metadata={"tdx_name": "SourceName"})

    #: The ID of the ticket status associated with the ticket.
    status_id = attr.ib(default=None, metadata={"tdx_name": "StatusID"})

    #: The name of the ticket status associated with the ticket.
    status_name = attr.ib(default=None, metadata={"tdx_name": "StatusName"})

    #: The class of the ticket status associated with the ticket.
    status_class = attr.ib(
        default=StatusClass.NEW,
        converter=StatusClass,
        metadata={"tdx_name": "StatusClass"},
    )

    #: The ID of the impact associated with the ticket.
    impact_id = attr.ib(default=None, metadata={"tdx_name": "ImpactID"})

    #: The name of the impact associated with the ticket.
    impact_name = attr.ib(default=None, metadata={"tdx_name": "ImpactName"})

    #: The ID of the urgency associated with the ticket.
    urgency_id = attr.ib(default=None, metadata={"tdx_name": "UrgencyID"})

    #: The name of the urgency associated with the ticket.
    urgency_name = attr.ib(default=None, metadata={"tdx_name": "UrgencyName"})

    #: The ID of the priority associated with the ticket.
    priority_id = attr.ib(default=None, metadata={"tdx_name": "PriorityID"})

    #: The name of the priority associated with the ticket.
    priority_name = attr.ib(default=None, metadata={"tdx_name": "PriorityName"})

    #: The order of the priority associated with the ticket.
    priority_order = attr.ib(default=None, metadata={"tdx_name": "PriorityOrder"})

    #: The ID of the Service Level Agreement (SLA) associated with the ticket.
    sla_id = attr.ib(default=None, metadata={"tdx_name": "SlaID"})

    #: The name of the Service Level Agreement (SLA) associated with the ticket.
    sla_name = attr.ib(default=None, metadata={"tdx_name": "SlaName"})

    #: Whether the Service Level Agreement (SLA) associated with the ticket has been
    #: violated.
    is_sla_violated = attr.ib(default=None, metadata={"tdx_name": "IsSlaViolated"})

    #: Whether the Service Level Agreement (SLA) associated with the ticket has its
    #: "Respond By" component violated.
    is_sla_respond_by_violated = attr.ib(
        default=None, metadata={"tdx_name": "IsSlaRespondByViolated"}
    )

    #: Whether the Service Level Agreement (SLA) associated with the ticket has its
    #: "Resolve By" component violated.
    is_sla_resolve_by_violated = attr.ib(
        default=None, metadata={"tdx_name": "IsSlaResolveByViolated"}
    )

    #: The "Respond By" deadline of the Service Level Agreement (SLA) associated with
    #: the ticket.
    respond_by_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "RespondByDate"}
    )

    #: The "Resolve By" deadline of the Service Level Agreement (SLA) associated with
    #: the ticket.
    resolve_by_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "ResolveByDate"}
    )

    #: The date the Service Level Agreement (SLA) associated with the ticket was
    #: started.
    sla_begin_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "SlaBeginDate"}
    )

    #: The on hold status of the ticket.
    is_on_hold = attr.ib(default=None, metadata={"tdx_name": "IsOnHold"})

    #: The date the ticket was placed on hold.
    placed_on_hold_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "PlacedOnHoldDate"}
    )

    #: The date the ticket goes off hold.
    goes_off_hold_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "GoesOffHoldDate"}
    )

    #: The created date of the ticket.
    created_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CreatedDate"}
    )

    #: The UID of the user who created the ticket.
    created_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "CreatedUid"}
    )

    #: The full name of the user who created the ticket.
    created_full_name = attr.ib(default=None, metadata={"tdx_name": "CreatedFullName"})

    #: The email address of the user who created the ticket.
    created_email = attr.ib(default=None, metadata={"tdx_name": "CreatedEmail"})

    #: The last modified date of the ticket.
    modified_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "ModifiedDate"}
    )

    #: The UID of the user who last modified the ticket.
    modified_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ModifiedUid"}
    )

    #: The full name of the user who last modified the ticket.
    modified_full_name = attr.ib(
        default=None, metadata={"tdx_name": "ModifiedFullName"}
    )

    #: The full name of the requestor associated with the ticket.
    requestor_name = attr.ib(default=None, metadata={"tdx_name": "RequestorName"})

    #: The first name of the requestor associated with the ticket.
    requestor_first_name = attr.ib(
        default=None, metadata={"tdx_name": "RequestorFirstName"}
    )

    #: The last name of the requestor associated with the ticket.
    requestor_last_name = attr.ib(
        default=None, metadata={"tdx_name": "RequestorLastName"}
    )

    #: The email address of the requestor associated with the ticket.
    requestor_email = attr.ib(default=None, metadata={"tdx_name": "RequestorEmail"})

    #: The phone number of the requestor associated with the ticket.
    requestor_phone = attr.ib(default=None, metadata={"tdx_name": "RequestorPhone"})

    #: The UID of the requestor associated with the ticket.
    requestor_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "RequestorUid"}
    )

    #: The time, in minutes, entered against the ticket or associated tasks/activities.
    actual_minutes = attr.ib(default=None, metadata={"tdx_name": "ActualMinutes"})

    #: The estimated minutes of the ticket.
    estimated_minutes = attr.ib(default=None, metadata={"tdx_name": "EstimatedMinutes"})

    #: The age of the ticket, in days.
    days_old = attr.ib(default=None, metadata={"tdx_name": "DaysOld"})

    #: The start date of the ticket.
    start_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "StartDate"}
    )

    #: The end date of the ticket.
    end_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "EndDate"}
    )

    #: The UID of the responsible user associated with the ticket.
    responsible_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ResponsibleUid"}
    )

    #: The full name of the responsible user associated with the ticket.
    responsible_full_name = attr.ib(
        default=None, metadata={"tdx_name": "ResponsibleFullName"}
    )

    #: The email address of the responsible user associated with the ticket.
    responsible_email = attr.ib(default=None, metadata={"tdx_name": "ResponsibleEmail"})

    #: The ID of the responsible group associated with the ticket.
    responsible_group_id = attr.ib(
        default=None, metadata={"tdx_name": "ResponsibleGroupID"}
    )

    #: The name of the responsible group associated with the ticket.
    responsible_group_name = attr.ib(
        default=None, metadata={"tdx_name": "ResponsibleGroupName"}
    )

    #: The date the ticket was responded to.
    responded_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "RespondedDate"}
    )

    #: The UID of the user who responded to the ticket.
    responded_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "RespondedUid"}
    )

    #: The full name of the user who responded to the ticket.
    responded_full_name = attr.ib(
        default=None, metadata={"tdx_name": "RespondedFullName"}
    )

    #: The completed/closed date of the ticket.
    completed_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CompletedDate"}
    )

    #: The UID of the user who completed/closed the ticket.
    completed_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "CompletedUid"}
    )

    #: The full name of the user who completed/closed the ticket.
    completed_full_name = attr.ib(
        default=None, metadata={"tdx_name": "CompletedFullName"}
    )

    #: The UID of the reviewing user associated with the ticket.
    reviewer_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ReviewerUid"}
    )

    #: The full name of the reviewing user associated with the ticket.
    reviewer_full_name = attr.ib(
        default=None, metadata={"tdx_name": "ReviewerFullName"}
    )

    #: The email address of the reviewing user associated with the ticket.
    reviewer_email = attr.ib(default=None, metadata={"tdx_name": "ReviewerEmail"})

    #: The ID of the reviewing group associated with the ticket.
    reviewing_group_id = attr.ib(
        default=None, metadata={"tdx_name": "ReviewingGroupID"}
    )

    #: The name of the reviewing group associated with the ticket.
    reviewing_group_name = attr.ib(
        default=None, metadata={"tdx_name": "ReviewingGroupName"}
    )

    #: The time budget of the ticket.
    time_budget = attr.ib(default=None, metadata={"tdx_name": "TimeBudget"})

    #: The expense budget of the ticket.
    expenses_budget = attr.ib(default=None, metadata={"tdx_name": "ExpensesBudget"})

    #: The used time budget of the ticket.
    time_budget_used = attr.ib(default=None, metadata={"tdx_name": "TimeBudgetUsed"})

    #: The used expense budget of the ticket.
    expenses_budget_used = attr.ib(
        default=None, metadata={"tdx_name": "ExpensesBudgetUsed"}
    )

    #: Whether the ticket has been converted to a project task.
    is_converted_to_task = attr.ib(
        default=None, metadata={"tdx_name": "IsConvertedToTask"}
    )

    #: The date the ticket was converted to a project task.
    converted_to_task_date = attr.ib(
        default=None,
        converter=to_datetime,
        metadata={"tdx_name": "ConvertedToTaskDate"},
    )

    #: The UID of the user who converted the ticket to a project task.
    converted_to_task_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ConvertedToTaskUid"}
    )

    #: The full name of the user who converted the ticket to a project task.
    converted_to_task_full_name = attr.ib(
        default=None, metadata={"tdx_name": "ConvertedToTaskFullName"}
    )

    #: The ID of the associated project when the ticket has been converted to a project
    #: task.
    task_project_id = attr.ib(default=None, metadata={"tdx_name": "TaskProjectID"})

    #: The name of the associated project when the ticket has been converted to a
    #: project task.
    task_project_name = attr.ib(default=None, metadata={"tdx_name": "TaskProjectName"})

    #: The ID of the associated project plan when the ticket has been converted to a
    #: project task.
    task_plan_id = attr.ib(default=None, metadata={"tdx_name": "TaskPlanID"})

    #: The name of the associated project plan when the ticket has been converted to a
    #: project task.
    task_plan_name = attr.ib(default=None, metadata={"tdx_name": "TaskPlanName"})

    #: The ID of the associated project task when the ticket has been converted to a
    #: project task.
    task_id = attr.ib(default=None, metadata={"tdx_name": "TaskID"})

    #: The title of the associated project task when the ticket has been converted to a
    #: project task.
    task_title = attr.ib(default=None, metadata={"tdx_name": "TaskTitle"})

    #: The start date of the associated project task when the ticket has been converted
    #: to a project task.
    task_start_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "TaskStartDate"}
    )

    #: The end date of the associated project task when the ticket has been converted to
    #: a project task.
    task_end_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "TaskEndDate"}
    )

    #: The percent complete of the associated project task when the ticket has been
    #: converted to a project task.
    task_percent_complete = attr.ib(
        default=None, metadata={"tdx_name": "TaskPercentComplete"}
    )

    #: The ID of the location associated with the ticket.
    location_id = attr.ib(default=None, metadata={"tdx_name": "LocationID"})

    #: The name of the location associated with the ticket.
    location_name = attr.ib(default=None, metadata={"tdx_name": "LocationName"})

    #: The ID of the location room associated with the ticket.
    location_room_id = attr.ib(default=None, metadata={"tdx_name": "LocationRoomID"})

    #: The name of the location room associated with the ticket.
    location_room_name = attr.ib(
        default=None, metadata={"tdx_name": "LocationRoomName"}
    )

    #: The reference code of the ticket.
    ref_code = attr.ib(default=None, metadata={"tdx_name": "RefCode"})

    #: The ID of the service associated with the ticket.
    service_id = attr.ib(default=None, metadata={"tdx_name": "ServiceID"})

    #: The name of the service associated with the ticket.
    service_name = attr.ib(default=None, metadata={"tdx_name": "ServiceName"})

    #: The ID of the category associated with the ticket's service.
    service_category_id = attr.ib(
        default=None, metadata={"tdx_name": "ServiceCategoryID"}
    )

    #: The name of the category associated with the ticket's service.
    service_category_name = attr.ib(
        default=None, metadata={"tdx_name": "ServiceCategoryName"}
    )

    #: The ID of the Knowledge Base article associated with the ticket.
    article_id = attr.ib(default=None, metadata={"tdx_name": "ArticleID"})

    #: The subject of the Knowledge Base article associated with the ticket.
    article_subject = attr.ib(default=None, metadata={"tdx_name": "ArticleSubject"})

    #: The ID of the Knowledge Base article associated with the ticket.
    article_status = attr.ib(
        default=ArticleStatus.NOT_SUBMITTED,
        converter=ArticleStatus,
        metadata={"tdx_name": "ArticleStatus"},
    )

    #: A delimited string of the category hierarchy associated with the ticket's
    #: Knowledge Base article.
    article_category_path_names = attr.ib(
        default=None, metadata={"tdx_name": "ArticleCategoryPathNames"}
    )

    #: The ID of the client portal application associated with the ticket's Knowledge
    #: Base article.
    article_app_id = attr.ib(default=None, metadata={"tdx_name": "ArticleAppID"})

    #: The ID of the shortcut that is used when viewing the ticket's Knowledge Base
    #: article. This is set when the ticket is associated with a cross client portal
    #: article shortcut.
    article_shortcut_id = attr.ib(
        default=None, metadata={"tdx_name": "ArticleShortcutID"}
    )

    #: The ID of the ticketing application associated with the ticket.
    app_id = attr.ib(default=None, metadata={"tdx_name": "AppID"})

    #: The custom attributes associated with the ticket.
    attributes = attr.ib(
        default=attr.Factory(CustomAttributeList),
        converter=CustomAttributeList.from_data,
        metadata={"tdx_name": "Attributes"},
    )

    #: The attachments associated with the ticket.
    attachments = attr.ib(
        default=attr.Factory(list),
        converter=Attachment.from_data,
        metadata={"tdx_name": "Attachments"},
    )

    #: The ticket tasks associated with the ticket.
    tasks = attr.ib(
        default=attr.Factory(list),
        converter=TicketTask.from_data,
        metadata={"tdx_name": "Tasks"},
    )

    #: The list of people who can be notified for the ticket.
    notify = attr.ib(
        default=attr.Factory(list),
        converter=ResourceItem.from_data,
        metadata={"tdx_name": "Notify"},
    )
