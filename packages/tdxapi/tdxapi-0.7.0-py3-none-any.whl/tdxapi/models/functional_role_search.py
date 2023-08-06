import attr

from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class FunctionalRoleSearch(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Roles.FunctionalRoleSearch"

    #: The functional role name.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The maximum results to return.
    max_results = attr.ib(default=0, metadata={"tdx_name": "MaxResults"})

    #: A value indicating whether the counts of associated items should be returned.
    #: Note: this currently only affects standard functional role selections, as
    #: admin selections will always include item counts.
    return_item_counts = attr.ib(
        default=None, metadata={"tdx_name": "ReturnItemCounts"}
    )
