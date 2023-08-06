import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_uid


@attr.s(kw_only=True)
class UserApplication(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Apps.UserApplication"

    #: The ID of the security role that the user has within the application.
    security_role_id = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "SecurityRoleId"}
    )

    #: The name of the security role that the user has within the application.
    security_role_name = attr.ib(
        default=None, metadata={"tdx_name": "SecurityRoleName"}
    )

    #: The administrator status of the user for the application.
    is_administrator = attr.ib(default=None, metadata={"tdx_name": "IsAdministrator"})

    #: The ID of the application.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The name of the application.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The description of the application.
    description = attr.ib(default=None, metadata={"tdx_name": "Description"})

    #: The system-defined class of the application.
    app_class = attr.ib(default=None, metadata={"tdx_name": "SystemClass"})

    #: The default status of the application.
    is_default = attr.ib(default=None, metadata={"tdx_name": "IsDefault"})

    #: The active status of the application.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})
