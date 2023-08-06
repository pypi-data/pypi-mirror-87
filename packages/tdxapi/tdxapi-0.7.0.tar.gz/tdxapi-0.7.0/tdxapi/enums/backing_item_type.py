from enum import Enum


class BackingItemType(Enum):
    """Types of TeamDynamix items that a configuration item can represent."""

    __tdx_type__ = "TeamDynamix.Api.Cmdb.BackingItemType"

    #: Indicates that a configuration item is not backed by any other type of
    #: TeamDynamix item; that is, that the configuration item is not automatically
    #: maintained by the system.
    CONFIGURATION_ITEM = 63

    #: Indicates that a configuration item is based on a TeamDynamix asset in the asset
    #: management application.
    ASSET = 27

    #: Indicates that a configuration item is based on a TeamDynamix service in the
    #: service catalog.
    SERVICE = 47
