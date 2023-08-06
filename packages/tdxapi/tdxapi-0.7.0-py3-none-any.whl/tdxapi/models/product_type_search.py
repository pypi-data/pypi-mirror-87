import attr

from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class ProductTypeSearch(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Assets.ProductTypeSearch"

    #: The search text to filter on. If this is set, this will sort the results
    #: by their text relevancy.
    search_text = attr.ib(default=None, metadata={"tdx_name": "SearchText"})

    #: The active status to filter on.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: A value indicating whether only top-level product types should be included.
    is_top_level = attr.ib(default=None, metadata={"tdx_name": "IsTopLevel"})

    #: The parent product type id to filter on. If this is set, only direct children
    #: of this type will be included.
    parent_product_type_id = attr.ib(
        default=None, metadata={"tdx_name": "ParentProductTypeID"}
    )
