from enum import Enum


class UserType(Enum):
    """Types of users and customers tracked within TeamDynamix."""

    __tdx_type__ = "TeamDynamix.Api.Users.UserType"

    #: Indicates that the type of the user could not be determined. Should not be used
    #: in normal operations.
    NONE = 0

    #: Indicates that the user is classified as a full TeamDynamix user.
    USER = 1

    #: Indicates that the user is classified as a customer, which means that they cannot
    #: log in to TeamDynamix.
    CUSTOMER = 2

    #: Indicates that the user is classified as a resource placeholder. These users act
    #: as a placeholder for actual users when planning out projects without knowing
    #: exactly who will be acting as the resource in question.
    RESOURCE_PLACEHOLDER = 8
