import attr

from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class Priority(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.PriorityFactors.Priority"

    #: The ID of the priority.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The name of the priority.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The description of the priority.
    description = attr.ib(default=None, metadata={"tdx_name": "Description"})

    #: The order of the priority in a list.
    order = attr.ib(default=None, metadata={"tdx_name": "Order"})

    #: The active status of the priority.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: The default status of the priority.
    is_default = attr.ib(default=None, metadata={"tdx_name": "IsDefault"})
