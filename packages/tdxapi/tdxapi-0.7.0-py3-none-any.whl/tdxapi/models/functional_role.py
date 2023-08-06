import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime


@attr.s(kw_only=True)
class FunctionalRole(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Roles.FunctionalRole"

    #: The id.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The name.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The standard rate.
    standard_rate = attr.ib(default=None, metadata={"tdx_name": "StandardRate"})

    #: The cost rate.
    cost_rate = attr.ib(default=None, metadata={"tdx_name": "CostRate"})

    #: The created date.
    created_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CreatedDate"}
    )

    #: The last modified date.
    modified_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "ModifiedDate"}
    )

    #: The comments.
    comments = attr.ib(default=None, metadata={"tdx_name": "Comments"})

    #: The number of users associated with the role. This will be -1 if this total
    #: has not been loaded.
    users_count = attr.ib(default=None, metadata={"tdx_name": "UsersCount"})

    #: The number of requests associated with the role. This will be -1 if this total
    #: has not been loaded.
    requests_count = attr.ib(default=None, metadata={"tdx_name": "RequestsCount"})

    #: The number of projects associated with the role. This will be -1 if this total
    #: has not been loaded.
    projects_count = attr.ib(default=None, metadata={"tdx_name": "ProjectsCount"})

    #: The number of opportunities associated with the role. This will be -1 if this
    #: total has not been loaded.
    opportunities_count = attr.ib(
        default=None, metadata={"tdx_name": "OpportunitiesCount"}
    )

    #: The number of resource requests associated with the role. This will be -1 if
    #: this total has not been loaded.
    resource_requests_count = attr.ib(
        default=None, metadata={"tdx_name": "ResourceRequestsCount"}
    )
