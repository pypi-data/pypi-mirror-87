import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime, to_uid
from tdxapi.models.custom_attribute_list import CustomAttributeList


@attr.s(kw_only=True)
class AssetSearch(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Assets.AssetSearch"

    #: The text to perform a like search on for the asset serial number and tag.
    serial_like = attr.ib(default=None, metadata={"tdx_name": "SerialLike"})

    #: The search text to filter on. If this is set, this will sort the results by
    #: their text relevancy.
    search_text = attr.ib(default=None, metadata={"tdx_name": "SearchText"})

    #: The id of the saved search this search is associated with.
    saved_search_id = attr.ib(default=None, metadata={"tdx_name": "SavedSearchID"})

    #: The current status ids to filter on. Only assets that currently have one of
    #: these statuses will be included.
    status_ids = attr.ib(default=attr.Factory(list), metadata={"tdx_name": "StatusIDs"})

    #: The external ids to filter on. Only assets that have one of these external id
    #: values will be included.
    external_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "ExternalIDs"}
    )

    #: The "in service" status to filter on (based on the out of service flag of
    #: each asset's status).
    is_in_service = attr.ib(default=None, metadata={"tdx_name": "IsInService"})

    #: The past status ids to filter on. Only assets that have had one of these
    #: statuses will be included.
    status_ids_past = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "StatusIDsPast"}
    )

    #: The supplier ids to filter on. Only assets that are supplied by one of these
    #: vendors will be included.
    supplier_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "SupplierIDs"}
    )

    #: The manufacturer ids to filter on. Only assets that are manufactured by one
    #: of these vendors will be included.
    manufacturer_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "ManufacturerIDs"}
    )

    #: The location ids to filter on. Only assets that are at one of these locations
    #: will be included.
    location_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "LocationIDs"}
    )

    #: The room id to filter on. Only assets that are located in this room will be
    #: included.
    room_id = attr.ib(default=None, metadata={"tdx_name": "RoomID"})

    #: The parent asset ids to filter on. Only assets that have one of these listed
    #: as a parent will be included.
    parent_ids = attr.ib(default=attr.Factory(list), metadata={"tdx_name": "ParentIDs"})

    #: The contract ids to filter on. Only assets that belong to one or more of
    #: these contracts will be included.
    contract_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "ContractIDs"}
    )

    #: The contract ids to exclude on. Only assets that do not belong to any of these
    #: contracts will be included.
    exclude_contract_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "ExcludeContractIDs"}
    )

    #: The ticket ids to filter on. Only assets that are associated with one or more
    #: of these tickets will be included.
    ticket_ids = attr.ib(default=attr.Factory(list), metadata={"tdx_name": "TicketIDs"})

    #: The form ids to filter on. Only assets that use one or more of these forms
    #: will be included.
    form_ids = attr.ib(default=attr.Factory(list), metadata={"tdx_name": "FormIDs"})

    #: The ticket ids to exclude on. Only assets that are not associated with any
    #: of these tickets will be included.
    exclude_ticket_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "ExcludeTicketIDs"}
    )

    #: The product model ids to filter on. Only assets that are one of these product
    #: models will be included.
    product_model_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "ProductModelIDs"}
    )

    #: The maintenance window ids to filter on. Only assets that have one of these
    #: maintenance windows will be included.
    maintenance_schedule_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "MaintenanceScheduleIDs"}
    )

    #: The using account/department ids to filter on. Only assets that are currently
    #: used by one or more of these accounts will be included.
    using_department_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "UsingDepartmentIDs"}
    )

    #: The requested account/department ids to filter on. Only assets that are listed
    #: as requested by one of these accounts will be included.
    requesting_department_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "RequestingDepartmentIDs"}
    )

    #: The owning account/department ids to filter on. Only assets that are currently
    #: owned by one of these accounts will be included.
    owning_department_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "OwningDepartmentIDs"}
    )

    #: The past owning account/department ids to filter on. Only assets that have
    #: been historically owned by one or more of these accounts will be included.
    owning_department_ids_past = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "OwningDepartmentIDsPast"}
    )

    #: The using person ids to filter on. Only assets that are currently used by
    #: one or more of these people will be included.
    using_customer_ids = attr.ib(
        default=attr.Factory(list),
        converter=to_uid,
        metadata={"tdx_name": "UsingCustomerIDs"},
    )

    #: The requestor ids to filter on. Only assets that are listed as requested by
    #: one of these people will be included.
    requesting_customer_ids = attr.ib(
        default=attr.Factory(list),
        converter=to_uid,
        metadata={"tdx_name": "RequestingCustomerIDs"},
    )

    #: The owner ids to filter on. Only assets that are currently owned by one of
    #: these people will be included.
    owning_customer_ids = attr.ib(
        default=attr.Factory(list),
        converter=to_uid,
        metadata={"tdx_name": "OwningCustomerIDs"},
    )

    #: The past owner ids to filter on. Only assets that have been historically owned
    #: by one or more of these people will be included.
    owning_customer_ids_past = attr.ib(
        default=attr.Factory(list),
        converter=to_uid,
        metadata={"tdx_name": "OwningCustomerIDsPast"},
    )

    #: The custom attributes to filter on.
    custom_attributes = attr.ib(
        default=attr.Factory(CustomAttributeList),
        converter=CustomAttributeList.from_data,
        metadata={"tdx_name": "CustomAttributes"},
    )

    #: The minimum purchase cost to filter on.
    purchase_cost_from = attr.ib(
        default=None, metadata={"tdx_name": "PurchaseCostFrom"}
    )

    #: The maximum purchase cost to filter on.
    purchase_cost_to = attr.ib(default=None, metadata={"tdx_name": "PurchaseCostTo"})

    #: The contract provider to filter on. Only assets that belong to at least one
    #: contract provided by this vendor will be included.
    contract_provider_id = attr.ib(
        default=None, metadata={"tdx_name": "ContractProviderID"}
    )

    #: The minimum acquisition date to filter on.
    acquisition_date_from = attr.ib(
        default=None,
        converter=to_datetime,
        metadata={"tdx_name": "AcquisitionDateFrom"},
    )

    #: The maximum acquisition date to filter on.
    acquisition_date_to = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "AcquisitionDateTo"}
    )

    #: The minimum expected replacement date to filter on.
    expected_replacement_date_from = attr.ib(
        default=None,
        converter=to_datetime,
        metadata={"tdx_name": "ExpectedReplacementDateFrom"},
    )

    #: The maximum expected replacement date to filter on.
    expected_replacement_date_to = attr.ib(
        default=None,
        converter=to_datetime,
        metadata={"tdx_name": "ExpectedReplacementDateTo"},
    )

    #: The minimum contract end date to filter on.
    contract_end_date_from = attr.ib(
        default=None,
        converter=to_datetime,
        metadata={"tdx_name": "ContractEndDateFrom"},
    )

    #: The maximum contract end date to filter on.
    contract_end_date_to = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "ContractEndDateTo"}
    )

    #: A value indicating whether only assets that are parents should be included.
    only_parent_assets = attr.ib(
        default=None, metadata={"tdx_name": "OnlyParentAssets"}
    )

    #: The maximum number of records to return.
    max_results = attr.ib(default=0, metadata={"tdx_name": "MaxResults"})
