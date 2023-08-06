import attr

from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class AssetStatusSearch(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Assets.AssetStatusSearch"

    #: The active status to filter on.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: The out of service status to filter on.
    is_out_of_service = attr.ib(default=None, metadata={"tdx_name": "IsOutOfService"})

    #: The search text to filter on. if this is set, this will sort the results by
    #: their text relevancy.
    search_text = attr.ib(default=None, metadata={"tdx_name": "SearchText"})
