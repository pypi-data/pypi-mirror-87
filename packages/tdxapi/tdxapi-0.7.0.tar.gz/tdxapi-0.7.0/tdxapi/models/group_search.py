import attr

from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class GroupSearch(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Users.GroupSearch"

    #: The active status to filter on.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: The search text to use for LIKE filtering on group name.
    name_like = attr.ib(default=None, metadata={"tdx_name": "NameLike"})

    #: The ID of the platform application the group is available in.
    available_in_app_id = attr.ib(default=None, metadata={"tdx_name": "HasAppID"})

    #: The system application name the group is available in.
    available_in_sys_app = attr.ib(
        default=None, metadata={"tdx_name": "HasSystemAppName"}
    )

    #: The associated platform application ID to filter on.
    associated_app_id = attr.ib(default=None, metadata={"tdx_name": "AssociatedAppID"})
