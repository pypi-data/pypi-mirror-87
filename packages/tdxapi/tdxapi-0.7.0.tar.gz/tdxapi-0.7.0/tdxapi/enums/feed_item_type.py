from enum import Enum


class FeedItemType(Enum):
    """Types of TeamDynamix items that have feed entries."""

    __tdx_type__ = "TeamDynamix.Api.Feed.FeedItemType"

    #: An indeterminate type of item.
    NONE = 0

    #: A project.
    PROJECT = 1

    #: A project request.
    PROJECT_REQUEST = 1

    #: A project task.
    TASK = 2

    #: A project issue.
    ISSUE = 3

    #: A project link.
    LINK = 4

    #: A project request.
    CONTACT = 6

    #: A project announcement.
    ANNOUNCEMENT = 7

    #: A ticket.
    TICKET = 9

    #: A briefcase file.
    FILE = 15

    #: A user-shared status.
    USER_STATUS = 24

    #: A ticket task.
    TICKET_TASK = 25

    #: A maintenance activity.
    MAINTENANCE_ACTIVITY = 25

    #: A Knowledge Base article.
    KNOWLEDGE_BASE_ARTICLE = 26

    #: An asset.
    ASSET = 27

    #: A plan.
    PLAN = 43

    #: A workspace.
    WORKSPACE = 45

    #: A service.
    SERVICE = 47

    #: A calendar event.
    CALENDAR_EVENT = 57

    #: An expense.
    EXPENSE = 62

    #: A configuration item.
    CONFIGURATION_ITEM = 63

    #: A risk.
    RISK = 72

    #: A portfolio issue.
    PORTFOLIO_ISSUE = 83

    #: A portfolio risk.
    PORTFOLIO_RISK = 84
