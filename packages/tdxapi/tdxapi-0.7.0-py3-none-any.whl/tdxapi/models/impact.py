import attr

from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class Impact(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.PriorityFactors.Impact"

    #: The ID of the impact.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The name of the impact.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The description of the impact.
    description = attr.ib(default=None, metadata={"tdx_name": "Description"})

    #: The order of the impact in a list.
    order = attr.ib(default=None, metadata={"tdx_name": "Order"})

    #: The active status of the impact.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: The default status of the impact.
    is_default = attr.ib(default=None, metadata={"tdx_name": "IsDefault"})
