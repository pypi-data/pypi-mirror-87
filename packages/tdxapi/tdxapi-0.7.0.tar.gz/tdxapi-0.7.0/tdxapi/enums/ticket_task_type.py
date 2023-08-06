from enum import Enum


class TicketTaskType(Enum):
    """The different types of items that can be represented by ticket tasks."""

    __tdx_type__ = "TeamDynamix.Api.Tickets.TicketTaskType"

    #: An unknown or indeterminate type of task.
    NONE = 0

    #: A standard, workable ticket task.
    TICKET_TASK = 1

    #: A scheduled maintenance activity.
    MAINTENANCE_ACTIVITY = 2

    #: A task that is used as a work step in a workflow.
    WORKFLOW_TASK = 3
