import attr

from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class ResourceItem(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.ResourceItem"

    #: The role this person or group has on the associated item.
    role = attr.ib(default=None, metadata={"tdx_name": "ItemRole"})

    #: The name of this person or group.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The initials to be displayed if no profile image is specified for the item.
    initials = attr.ib(default=None, metadata={"tdx_name": "Initials"})

    #: The id of the resource item.
    id = attr.ib(default=None, metadata={"tdx_name": "Value"})

    #: The reference id of the resource item.
    ref_id = attr.ib(default=None, metadata={"tdx_name": "RefValue"})

    #: The profile image file name of the resource.
    profile_image_file_name = attr.ib(
        default=None, metadata={"tdx_name": "ProfileImageFileName"}
    )
