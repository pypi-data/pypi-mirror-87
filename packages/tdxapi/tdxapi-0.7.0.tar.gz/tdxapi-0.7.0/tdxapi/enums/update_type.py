from enum import Enum


class UpdateType(Enum):
    """Types of feed entries."""

    __tdx_type__ = "TeamDynamix.Api.Feed.UpdateType"

    #: A feed entry of an indeterminate type.
    NONE = 0

    #: A feed entry for a comment on an item.
    COMMENT = 1

    #: A feed entry for an item's status changing.
    STATUS_CHANGE = 2

    #: A feed entry for an item's properties being edited.
    EDIT = 3

    #: A feed entry for a newly-created item.
    CREATED = 4

    #: A feed entry for a user adding/removing items to and from "My Work".
    MY_WORK_CHANGE = 5

    #: A feed entry for the contents of an item being merged into another item.
    MERGE = 6

    #: A feed entry for a comment on an item being moved to another item.
    MOVED_COMMENT = 7
