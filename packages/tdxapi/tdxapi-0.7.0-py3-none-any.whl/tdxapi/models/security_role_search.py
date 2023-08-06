import attr

from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class SecurityRoleSearch(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Roles.SecurityRoleSearch"

    #: The security role name.
    name_like = attr.ib(default=None, metadata={"tdx_name": "NameLike"})

    #: The application id. providing a non-zero value will search for
    #: application-specific security roles, while a value of 0 will search for
    #: global security roles.
    app_id = attr.ib(default=None, metadata={"tdx_name": "AppID"})

    #: The license type.
    license_type = attr.ib(default=None, metadata={"tdx_name": "LicenseTypeID"})
