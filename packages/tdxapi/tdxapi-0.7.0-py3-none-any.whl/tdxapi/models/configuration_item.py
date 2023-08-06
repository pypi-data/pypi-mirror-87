import attr

from tdxapi.enums.backing_item_type import BackingItemType
from tdxapi.models.attachment import Attachment
from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime, to_uid
from tdxapi.models.custom_attribute_list import CustomAttributeList


@attr.s(kw_only=True)
class ConfigurationItem(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Cmdb.ConfigurationItem"

    #: The id.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The application id.
    app_id = attr.ib(default=None, metadata={"tdx_name": "AppID"})

    #: The name of the application.
    app_name = attr.ib(default=None, metadata={"tdx_name": "AppName"})

    #: The id of the form. If a value of 0 is provided, then the default configuration
    #: item form for the application will be used.
    form_id = attr.ib(default=None, metadata={"tdx_name": "FormID"})

    #: The name of the form.
    form_name = attr.ib(default=None, metadata={"tdx_name": "FormName"})

    #: A value indicating whether this configuration item is maintained automatically
    #: by the system.
    is_system_defined = attr.ib(
        default=None, metadata={"tdx_name": "IsSystemMaintained"}
    )

    #: The id of the underlying teamdynamix item in the system that this
    #: configuration item represents.
    backing_item_id = attr.ib(default=None, metadata={"tdx_name": "BackingItemID"})

    #: The type of the underlying teamdynamix item in the system that this
    #: configuration item represents.
    backing_item_type = attr.ib(
        default=BackingItemType.CONFIGURATION_ITEM,
        converter=BackingItemType,
        metadata={"tdx_name": "BackingItemType"},
    )

    #: The name.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The id of the associated configuration item type.
    type_id = attr.ib(default=None, metadata={"tdx_name": "TypeID"})

    #: The name of the associated configuration item type.
    type_name = attr.ib(default=None, metadata={"tdx_name": "TypeName"})

    #: The id of the associated maintenance window.
    maintenance_schedule_id = attr.ib(
        default=None, metadata={"tdx_name": "MaintenanceScheduleID"}
    )

    #: The name of the associated maintenance window.
    maintenance_schedule_name = attr.ib(
        default=None, metadata={"tdx_name": "MaintenanceScheduleName"}
    )

    #: The uid of the configuration item's owner.
    owner_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "OwnerUID"}
    )

    #: The full name of the configuration item's owner.
    owner_full_name = attr.ib(default=None, metadata={"tdx_name": "OwnerFullName"})

    #: The id of the acct/dept which owns the configuration item.
    owning_department_id = attr.ib(
        default=None, metadata={"tdx_name": "OwningDepartmentID"}
    )

    #: The name of the acct/dept which owns the configuration item.
    owning_department_name = attr.ib(
        default=None, metadata={"tdx_name": "OwningDepartmentName"}
    )

    #: The id of the configuration item's owning group.
    owning_group_id = attr.ib(default=None, metadata={"tdx_name": "OwningGroupID"})

    #: The name of the configuration item's owning group.
    owning_group_name = attr.ib(default=None, metadata={"tdx_name": "OwningGroupName"})

    #: The id of the location associated with the configuration item.
    location_id = attr.ib(default=None, metadata={"tdx_name": "LocationID"})

    #: The name of the location associated with the configuration item.
    location_name = attr.ib(default=None, metadata={"tdx_name": "LocationName"})

    #: The id of the location room associated with the configuration item.
    location_room_id = attr.ib(default=None, metadata={"tdx_name": "LocationRoomID"})

    #: The name of the location room associated with the configuration item.
    location_room_name = attr.ib(
        default=None, metadata={"tdx_name": "LocationRoomName"}
    )

    #: The active status. this will default to true.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: The date/time the configuration item was created.
    created_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CreatedDateUtc"}
    )

    #: The uid of the creator.
    created_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "CreatedUid"}
    )

    #: The full name of the creator.
    created_full_name = attr.ib(default=None, metadata={"tdx_name": "CreatedFullName"})

    #: The date/time the configuration item was last modified.
    modified_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "ModifiedDateUtc"}
    )

    #: The uid of the last person to modify the configuration item.
    modified_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ModifiedUid"}
    )

    #: The full name of the last person to modify the configuration item.
    modified_full_name = attr.ib(
        default=None, metadata={"tdx_name": "ModifiedFullName"}
    )

    #: The external id. This value is used to map the configuration item to its
    #: representation in external sources such as third-party cmdbs.
    external_id = attr.ib(default=None, metadata={"tdx_name": "ExternalID"})

    #: The id of the configuration item source, if the configuration item originated
    #: in a third-party cmdb system.
    external_source_id = attr.ib(
        default=None, metadata={"tdx_name": "ExternalSourceID"}
    )

    #: The name of the configuration item source, if the configuration item originated
    #: in a third-party cmdb system.
    external_source_name = attr.ib(
        default=None, metadata={"tdx_name": "ExternalSourceName"}
    )

    #: The custom attributes associated with the configuration item. Only supported
    #: for configuration items that are not system-maintained. Further, since
    #: configuration items support custom forms, the isrequired property is ignored.
    #: Alternatively, required status is driven by the form, which can be changed
    #: via the formid property.
    attributes = attr.ib(
        default=attr.Factory(CustomAttributeList),
        converter=CustomAttributeList.from_data,
        metadata={"tdx_name": "Attributes"},
    )

    #: The attachments associated with the configuration item. Only supported for
    #: configuration items that are not system-maintained.
    attachments = attr.ib(
        default=attr.Factory(list),
        converter=Attachment.from_data,
        metadata={"tdx_name": "Attachments"},
    )

    #: The uri to retrieve the individual configuration item.
    uri = attr.ib(default=None, metadata={"tdx_name": "Uri"})
