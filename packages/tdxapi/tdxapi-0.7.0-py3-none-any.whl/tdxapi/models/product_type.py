import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime


def product_type_subtype(value):
    """Special converter to handle subtypes."""
    return ProductType.from_data(value)


@attr.s(kw_only=True)
class ProductType(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Assets.ProductType"

    #: The identifier.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The application id.
    app_id = attr.ib(default=None, metadata={"tdx_name": "AppID"})

    #: The name of the application.
    app_name = attr.ib(default=None, metadata={"tdx_name": "AppName"})

    #: The id of the containing parent type, or 0 if this is a root-level type.
    parent_id = attr.ib(default=None, metadata={"tdx_name": "ParentID"})

    #: The name of the containing parent type.
    parent_name = attr.ib(default=None, metadata={"tdx_name": "ParentName"})

    #: The active status of the containing parent type.
    parent_is_active = attr.ib(default=None, metadata={"tdx_name": "ParentIsActive"})

    #: The name.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The description.
    description = attr.ib(default=None, metadata={"tdx_name": "Description"})

    #: The created date.
    created_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CreatedDate"}
    )

    #: The last modified date.
    modified_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "ModifiedDate"}
    )

    #: The order of the type among its siblings.
    order = attr.ib(default=None, metadata={"tdx_name": "Order"})

    #: The active status.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: The number of product models directly belonging to this type.
    product_models_count = attr.ib(
        default=None, metadata={"tdx_name": "ProductModelsCount"}
    )

    #: The number of subtypes directly belonging to this product type.
    subtypes_count = attr.ib(default=None, metadata={"tdx_name": "SubtypesCount"})

    #: The collection of subtypes directly belonging to this category
    subtypes = attr.ib(
        default=attr.Factory(list),
        converter=product_type_subtype,
        metadata={"tdx_name": "Subtypes"},
    )
