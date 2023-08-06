import attr

from tdxapi.models.attachment import Attachment
from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime, to_uid
from tdxapi.models.custom_attribute_list import CustomAttributeList


@attr.s(kw_only=True)
class Asset(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Assets.Asset"

    #: The id.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The application id.
    app_id = attr.ib(default=None, metadata={"tdx_name": "AppID"})

    #: The name of the application.
    app_name = attr.ib(default=None, metadata={"tdx_name": "AppName"})

    #: The id of the form. If a value of 0 is provided, then the default asset form
    #: for the application will be used.
    form_id = attr.ib(default=None, metadata={"tdx_name": "FormID"})

    #: The name of the form.
    form_name = attr.ib(default=None, metadata={"tdx_name": "FormName"})

    #: The product model id.
    product_model_id = attr.ib(default=None, metadata={"tdx_name": "ProductModelID"})

    #: The name of the product model.
    product_model_name = attr.ib(
        default=None, metadata={"tdx_name": "ProductModelName"}
    )

    #: The manufacturer id.
    manufacturer_id = attr.ib(default=None, metadata={"tdx_name": "ManufacturerID"})

    #: The name of the manufacturer.
    manufacturer_name = attr.ib(default=None, metadata={"tdx_name": "ManufacturerName"})

    #: The supplier id.
    supplier_id = attr.ib(default=None, metadata={"tdx_name": "SupplierID"})

    #: The name of the supplier.
    supplier_name = attr.ib(default=None, metadata={"tdx_name": "SupplierName"})

    #: The status id.
    status_id = attr.ib(default=None, metadata={"tdx_name": "StatusID"})

    #: The name of the status.
    status_name = attr.ib(default=None, metadata={"tdx_name": "StatusName"})

    #: The id of the containing location.
    location_id = attr.ib(default=None, metadata={"tdx_name": "LocationID"})

    #: The name of the containing location.
    location_name = attr.ib(default=None, metadata={"tdx_name": "LocationName"})

    #: The id of the containing room.
    location_room_id = attr.ib(default=None, metadata={"tdx_name": "LocationRoomID"})

    #: The name of the containing room.
    location_room_name = attr.ib(
        default=None, metadata={"tdx_name": "LocationRoomName"}
    )

    #: The asset's service tag.
    service_tag = attr.ib(default=None, metadata={"tdx_name": "Tag"})

    #: The serial number.
    serial_number = attr.ib(default=None, metadata={"tdx_name": "SerialNumber"})

    #: The name of the asset.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The purchase cost.
    purchase_cost = attr.ib(default=None, metadata={"tdx_name": "PurchaseCost"})

    #: The acquisition date.
    acquisition_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "AcquisitionDate"}
    )

    #: The expected replacement date.
    expected_replacement_date = attr.ib(
        default=None,
        converter=to_datetime,
        metadata={"tdx_name": "ExpectedReplacementDate"},
    )

    #: The requesting customer id.
    requesting_customer_id = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "RequestingCustomerID"}
    )

    #: The name of the requesting customer.
    requesting_customer_name = attr.ib(
        default=None, metadata={"tdx_name": "RequestingCustomerName"}
    )

    #: The requesting department id.
    requesting_department_id = attr.ib(
        default=None, metadata={"tdx_name": "RequestingDepartmentID"}
    )

    #: The name of the requesting department.
    requesting_department_name = attr.ib(
        default=None, metadata={"tdx_name": "RequestingDepartmentName"}
    )

    #: The owning customer id.
    owning_customer_id = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "OwningCustomerID"}
    )

    #: The name of the owning customer.
    owning_customer_name = attr.ib(
        default=None, metadata={"tdx_name": "OwningCustomerName"}
    )

    #: The owning department id.
    owning_department_id = attr.ib(
        default=None, metadata={"tdx_name": "OwningDepartmentID"}
    )

    #: The name of the owning department.
    owning_department_name = attr.ib(
        default=None, metadata={"tdx_name": "OwningDepartmentName"}
    )

    #: The id of the parent asset.
    parent_id = attr.ib(default=None, metadata={"tdx_name": "ParentID"})

    #: The serial number of the parent asset.
    parent_serial_number = attr.ib(
        default=None, metadata={"tdx_name": "ParentSerialNumber"}
    )

    #: The name of the parent asset.
    parent_name = attr.ib(default=None, metadata={"tdx_name": "ParentName"})

    #: The tag of the parent asset.
    parent_service_tag = attr.ib(default=None, metadata={"tdx_name": "ParentTag"})

    #: The id of the associated maintenance window.
    maintenance_schedule_id = attr.ib(
        default=None, metadata={"tdx_name": "MaintenanceScheduleID"}
    )

    #: The name of the associated maintenance window.
    maintenance_schedule_name = attr.ib(
        default=None, metadata={"tdx_name": "MaintenanceScheduleName"}
    )

    #: The id of the associated configuration item record.
    configuration_item_id = attr.ib(
        default=None, metadata={"tdx_name": "ConfigurationItemID"}
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

    #: The uid of the last person to modify the asset.
    modified_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ModifiedUid"}
    )

    #: The full name of the last person to modify the asset.
    modified_full_name = attr.ib(
        default=None, metadata={"tdx_name": "ModifiedFullName"}
    )

    #: The external id. This value is used to map the asset to its representation in
    #: external sources such as third-party cmdbs.
    external_id = attr.ib(default=None, metadata={"tdx_name": "ExternalID"})

    #: The id of the configuration item source, if the asset originated in a
    #: third-party cmdb system.
    external_source_id = attr.ib(
        default=None, metadata={"tdx_name": "ExternalSourceID"}
    )

    #: The name of the configuration item source, if the asset originated in a
    #: third-party cmdb system.
    external_source_name = attr.ib(
        default=None, metadata={"tdx_name": "ExternalSourceName"}
    )

    #: The custom attributes associated with the asset. Since assets support custom
    #: forms, the isrequired property is ignored. Alternatively, required status is
    #: driven by the form, which can be changed via the formid property.
    attributes = attr.ib(
        default=attr.Factory(CustomAttributeList),
        converter=CustomAttributeList.from_data,
        metadata={"tdx_name": "Attributes"},
    )

    #: The attachments associated with the asset.
    attachments = attr.ib(
        default=attr.Factory(list),
        converter=Attachment.from_data,
        metadata={"tdx_name": "Attachments"},
    )

    #: The uri to retrieve the individual asset.
    uri = attr.ib(default=None, metadata={"tdx_name": "Uri"})
