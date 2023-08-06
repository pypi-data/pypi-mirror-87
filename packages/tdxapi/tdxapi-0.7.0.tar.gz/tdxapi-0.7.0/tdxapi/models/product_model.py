import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime, to_uid
from tdxapi.models.custom_attribute_list import CustomAttributeList


@attr.s(kw_only=True)
class ProductModel(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Assets.ProductModel"

    #: The id.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The application id.
    app_id = attr.ib(default=None, metadata={"tdx_name": "AppID"})

    #: The name of the application.
    app_name = attr.ib(default=None, metadata={"tdx_name": "AppName"})

    #: The name.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The description.
    description = attr.ib(default=None, metadata={"tdx_name": "Description"})

    #: The active status.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: The manufacturer id.
    manufacturer_id = attr.ib(default=None, metadata={"tdx_name": "ManufacturerID"})

    #: The name of the manufacturer.
    manufacturer_name = attr.ib(default=None, metadata={"tdx_name": "ManufacturerName"})

    #: The id of the containing product type.
    product_type_id = attr.ib(default=None, metadata={"tdx_name": "ProductTypeID"})

    #: The name of the containing product type.
    product_type_name = attr.ib(default=None, metadata={"tdx_name": "ProductTypeName"})

    #: The part number.
    part_number = attr.ib(default=None, metadata={"tdx_name": "PartNumber"})

    #: The custom attributes associated with the product model.
    attributes = attr.ib(
        default=attr.Factory(CustomAttributeList),
        converter=CustomAttributeList.from_data,
        metadata={"tdx_name": "Attributes"},
    )

    #: The created date.
    created_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CreatedDate"}
    )

    #: The uid of the creator.
    created_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "CreatedUid"}
    )

    #: The full name of the creator.
    created_full_name = attr.ib(default=None, metadata={"tdx_name": "CreatedFullName"})

    #: The last modified date.
    modified_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "ModifiedDate"}
    )

    #: The uid of the last person to modify the product model.
    modified_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ModifiedUid"}
    )

    #: The full name of the last person to modify the product model.
    modified_full_name = attr.ib(
        default=None, metadata={"tdx_name": "ModifiedFullName"}
    )
