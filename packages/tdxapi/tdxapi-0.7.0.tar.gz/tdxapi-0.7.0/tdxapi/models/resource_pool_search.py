import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_uid


@attr.s(kw_only=True)
class ResourcePoolSearch(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Schedules.ResourcePoolSearch"

    #: The resource pool name to filter on.
    name_like = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The uid of the resource pool manager to filter on.
    manager_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ManagerUID"}
    )

    #: The maximum results to return.
    max_results = attr.ib(default=0, metadata={"tdx_name": "MaxResults"})

    #: The active status to filter on.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: A value indicating whether resource counts should be retrieved for each pool.
    #: Defaults to false.
    return_item_counts = attr.ib(
        default=None, metadata={"tdx_name": "ReturnItemCounts"}
    )
