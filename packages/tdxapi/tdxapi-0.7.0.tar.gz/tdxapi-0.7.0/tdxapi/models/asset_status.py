import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime, to_uid


@attr.s(kw_only=True)
class AssetStatus(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Assets.AssetStatus"

    #: The id.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The application id.
    app_id = attr.ib(default=None, metadata={"tdx_name": "AppID"})

    #: The name of the application.
    app_name = attr.ib(default=None, metadata={"tdx_name": "AppName"})

    #: The name.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The description.
    description = attr.ib(default=None, metadata={"tdx_name": "Description"})

    #: The order of the status in a list.
    order = attr.ib(default=None, metadata={"tdx_name": "Order"})

    #: The active status.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: A value indicating whether the status denotes that an associated asset
    #: is "out-of-service".
    is_out_of_service = attr.ib(default=None, metadata={"tdx_name": "IsOutOfService"})

    #: The created date.
    created_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CreatedDate"}
    )

    #: The uid of the creator.
    created_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "CreatedUid"}
    )

    #: The full name of the creator.
    created_full_name = attr.ib(default=None, metadata={"tdx_name": "CreatedFullName"})

    #: The last modified date.
    modified_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "ModifiedDate"}
    )

    #: The uid of the last person to modify the status.
    modified_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ModifiedUid"}
    )

    #: The full name of the last person to modify the status.
    modified_full_name = attr.ib(
        default=None, metadata={"tdx_name": "ModifiedFullName"}
    )
