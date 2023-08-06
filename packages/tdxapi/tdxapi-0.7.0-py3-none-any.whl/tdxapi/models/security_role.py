import attr

from tdxapi.enums.license_type import LicenseType
from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime, to_uid


@attr.s(kw_only=True)
class SecurityRole(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Roles.SecurityRole"

    #: The id.
    id = attr.ib(default=None, converter=to_uid, metadata={"tdx_name": "ID"})

    #: The name of the security role.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The created date.
    created_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CreatedDate"}
    )

    #: The modified date.
    modified_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "ModifiedDate"}
    )

    #: The number of users who have the security role. this will be -1 if this
    #: total has not been loaded.
    user_count = attr.ib(default=None, metadata={"tdx_name": "UserCount"})

    #: The id of the associated application, or 0 if this is a top-level security role.
    app_id = attr.ib(default=None, metadata={"tdx_name": "AppID"})

    #: The permissions granted to users with this security role. each value refers
    #: to the id of a permission.
    permissions = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "Permissions"}
    )

    #: The license type of the security role.
    license_type = attr.ib(
        default=LicenseType.NONE,
        converter=LicenseType,
        metadata={"tdx_name": "LicenseType"},
    )

    #: The name of the license type of the security role.
    license_type_name = attr.ib(default=None, metadata={"tdx_name": "LicenseTypeName"})
