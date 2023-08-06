from enum import Enum


class Component(Enum):
    """TeamDynamix components that support custom attributes."""

    __tdx_type__ = "TeamDynamix.Api.CustomAttributes.CustomAttributeComponent"

    #: Indicates that custom attributes are for projects and project requests in the
    #: Projects/Workspaces and Portfolio Planning systems.
    PROJECT = 1

    #: Indicates that custom attributes are for issues in the Projects/Workspaces
    #: system.
    ISSUE = 3

    #: Indicates that custom attributes are for files in the File Cabinet system.
    FILE_CABINET_FILE = 8

    #: Indicates that custom attributes are for tickets in the Tickets system.
    TICKET = 9

    #: Indicates that custom attributes are for accounts.
    ACCOUNT = 14

    #: Indicates that custom attributes are for articles in the Knowledge Base system.
    KNOWLEDGE_BASE_ARTICLE = 26

    #: Indicates that custom attributes are for assets in the Assets/CIs system.
    ASSET = 27

    #: Indicates that custom attributes are for vendors in the Assets/CIs system.
    VENDOR = 28

    #: Indicates that custom attributes are for contracts in the Assets/CIs system.
    CONTRACT = 29

    #: Indicates that custom attributes are for product models in the Assets/CIs system.
    PRODUCT_MODEL = 30

    #: Indicates that custom attributes are for people.
    PERSON = 31

    #: Indicates that custom attributes are for services.
    SERVICE = 47

    #: Indicates that custom attributes are for Risk Register risks in the
    #: Projects/Workspaces and Portfolio Planning systems.
    RISK = 72

    #: Indicates that custom attributes are for standalone configuration items in the
    #: Assets/CIs system.
    CONFIGURATION_ITEM = 63

    #: Indicates that custom attributes are for locations.
    LOCATION = 71

    #: Indicates that custom attributes are for rooms associated with a location.
    LOCATION_ROOM = 80
