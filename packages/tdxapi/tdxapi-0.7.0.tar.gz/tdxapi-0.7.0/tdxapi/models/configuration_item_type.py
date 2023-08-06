import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime, to_uid


@attr.s(kw_only=True)
class ConfigurationItemType(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Cmdb.ConfigurationItemType"

    #: The id.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The application id.
    app_id = attr.ib(default=None, metadata={"tdx_name": "AppID"})

    #: The name of the application.
    app_name = attr.ib(default=None, metadata={"tdx_name": "AppName"})

    #: A value indicating whether this item type is system-defined.
    is_system_defined = attr.ib(default=None, metadata={"tdx_name": "IsSystemDefined"})

    #: The name.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The active status.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: The created date.
    created_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CreatedDateUtc"}
    )

    #: The uid of the creator.
    created_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "CreatedUid"}
    )

    #: The full name of the creator.
    created_full_name = attr.ib(default=None, metadata={"tdx_name": "CreatedFullName"})

    #: The last modified date.
    modified_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "ModifiedDateUtc"}
    )

    #: The uid of the last person to modify the item type.
    modified_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ModifiedUid"}
    )

    #: The full name of the last person to modify the item type.
    modified_full_name = attr.ib(
        default=None, metadata={"tdx_name": "ModifiedFullName"}
    )
