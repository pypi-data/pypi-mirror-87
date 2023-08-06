import attr

from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class EligibleAssignment(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Users.EligibleAssignment"

    #: The name of the resource.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The ID of the resource.
    value = attr.ib(default=None, metadata={"tdx_name": "Value"})

    #: The email address of the resource.
    email = attr.ib(default=None, metadata={"tdx_name": "Email"})

    #: Whether the resource is a user.
    is_user = attr.ib(default=None, metadata={"tdx_name": "IsUser"})
