from enum import Enum


class StatusClass(Enum):
    """Describes the different classes of statuses."""

    __tdx_type__ = "TeamDynamix.Api.Statuses.StatusClass"

    #: Used for when a status class for a status could not be determined. Should not be
    #: used in normal operations.
    NONE = 0

    #: Used for new statuses.
    NEW = 1

    #: Used for statuses that are somewhere in the pipeline, but have not yet been
    #: completed.
    IN_PROCESS = 2

    #: Used for statuses that indicate completion such as "Closed" or "Closed and
    #: Approved".
    COMPLETED = 3

    #: Used for items that are cancelled.
    CANCELLED = 4

    #: Used for items that are on hold.
    ON_HOLD = 5

    #: Used for items that have been requested and not yet assigned a status.
    REQUESTED = 6
