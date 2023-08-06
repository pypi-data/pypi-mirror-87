import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime
from tdxapi.models.group_application import GroupApplication


@attr.s(kw_only=True)
class Group(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Users.Group"

    #: The ID of the group.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The name of the group.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The description of the group.
    description = attr.ib(default=None, metadata={"tdx_name": "Description"})

    #: The active status of the group.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: The external ID of the group.
    external_id = attr.ib(default=None, metadata={"tdx_name": "ExternalID"})

    #: The created date of the group.
    created_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CreatedDate"}
    )

    #: The last modified date of the group.
    modified_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "ModifiedDate"}
    )

    #: The platform applications associated with the group.
    apps = attr.ib(
        default=attr.Factory(list),
        converter=GroupApplication.from_data,
        metadata={"tdx_name": "PlatformApplications"},
    )
