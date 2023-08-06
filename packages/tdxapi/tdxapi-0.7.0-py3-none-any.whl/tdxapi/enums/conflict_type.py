from enum import Enum


class ConflictType(Enum):
    """Describes the different types of conflicts that can be detected for a scheduled
    maintenance activity for a CI.
    """

    __tdx_type__ = "TeamDynamix.Api.Tickets.ConflictType"

    #: Indicates that no conflicts were detected.
    NONE = 0

    #: Indicates that an activity takes place outside of the CI's maintenance window.
    OUTSIDE_MAINTENANCE_WINDOW = 1

    #: Indicates that an activity takes place during a blackout window.
    DURING_BLACKOUT_WINDOW = 2

    #: Indicates that an activity conflicts with a pre-existing activity scheduled for
    #: the CI.
    EXISTING_ACTIVITY = 4

    #: Indicates that an activity takes place outside the maintenance window of one or
    #: more of the CI's operational children.
    OUTSIDE_CHILD_MAINTENANCE_WINDOW = 8

    #: Indicates that an activity conflicts with a pre-existing activity on one of the
    #: CI's operational children.
    EXISTING_CHILD_ACTIVITY = 16

    #: Indicates that an activity conflicts with a pre-existing activity on one of the
    #: CI's operational parents.
    EXISTING_PARENT_ACTIVITY = 32
