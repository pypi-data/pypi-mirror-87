import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.custom_attribute_list import CustomAttributeList


@attr.s(kw_only=True)
class VendorSearch(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Assets.VendorSearch"

    #: The text to perform a like search on for the vendor name.
    name_like = attr.ib(default=None, metadata={"tdx_name": "NameLike"})

    #: The search text to filter on. If this is set, this will sort the results
    #: by their text relevancy.
    search_text = attr.ib(default=None, metadata={"tdx_name": "SearchText"})

    #: A value indicating whether or not only vendors who have been classified
    #: as product manufacturers should be returned.
    only_manufacturers = attr.ib(
        default=None, metadata={"tdx_name": "OnlyManufacturers"}
    )

    #: A value indicating whether or not only vendors who have been classified
    #: as asset suppliers should be returned.
    only_suppliers = attr.ib(default=None, metadata={"tdx_name": "OnlySuppliers"})

    #: A value indicating whether or not only vendors who have been classified
    #: as contract providers should be returned.
    only_contract_providers = attr.ib(
        default=None, metadata={"tdx_name": "OnlyContractProviders"}
    )

    #: The active status to filter on.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: The custom attributes to filter on.
    custom_attributes = attr.ib(
        default=attr.Factory(CustomAttributeList),
        converter=CustomAttributeList.from_data,
        metadata={"tdx_name": "CustomAttributes"},
    )
