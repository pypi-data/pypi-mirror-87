import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.custom_attribute_list import CustomAttributeList


@attr.s(kw_only=True)
class ProductModelSearch(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Assets.ProductModelSearch"

    #: The search text to filter on. if this is set, this will sort the results by
    #: their text relevancy.
    search_text = attr.ib(default=None, metadata={"tdx_name": "SearchText"})

    #: The id of the manufacturer to filter on.
    manufacturer_id = attr.ib(default=None, metadata={"tdx_name": "ManufacturerID"})

    #: The id of the product type to filter on. this will not filter on product
    #: subtypes.
    product_type_id = attr.ib(default=None, metadata={"tdx_name": "ProductTypeID"})

    #: The active status to filter on.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: The custom attributes to filter on.
    custom_attributes = attr.ib(
        default=attr.Factory(CustomAttributeList),
        converter=CustomAttributeList.from_data,
        metadata={"tdx_name": "CustomAttributes"},
    )
