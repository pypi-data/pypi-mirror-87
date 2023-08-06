import attr

from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class Urgency(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.PriorityFactors.Urgency"

    #: The ID of the urgency.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The name of the urgency.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The description of the urgency.
    description = attr.ib(default=None, metadata={"tdx_name": "Description"})

    #: The order of the urgency in a list.
    order = attr.ib(default=None, metadata={"tdx_name": "Order"})

    #: The active status of the urgency.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: The default status of the urgency.
    is_default = attr.ib(default=None, metadata={"tdx_name": "IsDefault"})
