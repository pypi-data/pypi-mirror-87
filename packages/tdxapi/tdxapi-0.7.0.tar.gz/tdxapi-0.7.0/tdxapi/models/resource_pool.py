import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime, to_uid


@attr.s(kw_only=True)
class ResourcePool(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Schedules.ResourcePool"

    #: The resource pool id.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The resource pool name.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The date/time the resource pool was created.
    created_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CreatedDate"}
    )

    #: The date/time the resource pool was last modified.
    modified_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "ModifiedDate"}
    )

    #: A value indicating whether the resource pool is active.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: A value indicating whether an email notification will be delivered to the
    #: manager when a resource is assigned.
    notify_on_assignment = attr.ib(
        default=None, metadata={"tdx_name": "NotifyOnAssignment"}
    )

    #: A value indicating whether the resource pool requires approval.
    requires_approval = attr.ib(default=None, metadata={"tdx_name": "RequiresApproval"})

    #: The full name of the resource pool manager.
    manager_full_name = attr.ib(default=None, metadata={"tdx_name": "ManagerFullName"})

    #: The uid of the resource pool manager.
    manager_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ManagerUID"}
    )

    #: The number of resources in the resource pool. This will be -1 if this total
    #: has not been loaded.
    resource_count = attr.ib(default=None, metadata={"tdx_name": "ResourceCount"})
