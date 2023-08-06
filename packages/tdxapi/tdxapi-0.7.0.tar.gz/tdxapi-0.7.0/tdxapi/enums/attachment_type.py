from enum import Enum


class AttachmentType(Enum):
    """Types of supported attachments."""

    __tdx_type__ = "TeamDynamix.Api.Attachments.AttachmentType"

    #: Indicates that the type of attachment is unknown.
    NONE = 0

    #: A project attachment.
    PROJECT = 1

    #: An issue attachment.
    ISSUE = 3

    #: An announcement attachment.
    ANNOUNCEMENT = 7

    #: A ticket attachment.
    TICKET = 9

    #: A forum post attachment.
    FORUMS = 13

    #: A Knowledge Base article attachment.
    KNOWLEDGE_BASE = 26

    #: An asset attachment.
    ASSET = 27

    #: An asset contract attachment.
    CONTRACT = 29

    #: A service attachment.
    SERVICE = 47

    #: A calendar event attachment.
    CALENDAR_EVENT = 57

    #: An expense attachment.
    EXPENSE = 62

    #: A configuration item attachment.
    CONFIGURATION_ITEM = 63

    #: A location attachment.
    LOCATION = 71

    #: A risk attachment.
    RISK = 72

    #: A portfolio issue attachment.
    PORTFOLIO_ISSUE = 83

    #: A portfolio risk attachment.
    PORTFOLIO_RISK = 84
