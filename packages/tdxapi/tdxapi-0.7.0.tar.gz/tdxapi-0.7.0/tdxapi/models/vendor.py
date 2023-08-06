import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.contact_information import ContactInformation
from tdxapi.models.converters import to_datetime, to_uid
from tdxapi.models.custom_attribute_list import CustomAttributeList


@attr.s(kw_only=True)
class Vendor(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Assets.Vendor"

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

    #: The account number used by the vendor to represent the organization.
    account_number = attr.ib(default=None, metadata={"tdx_name": "AccountNumber"})

    #: A value indicating whether the vendor is classified as a contract provider.
    is_contract_provider = attr.ib(
        default=None, metadata={"tdx_name": "IsContractProvider"}
    )

    #: A value indicating whether the vendor is classified as a manufacturer
    #: of product models.
    is_manufacturer = attr.ib(default=None, metadata={"tdx_name": "IsManufacturer"})

    #: A value indicating whether the vendor is classified as a supplier of assets.
    is_supplier = attr.ib(default=None, metadata={"tdx_name": "IsSupplier"})

    #: The contact information for the company.
    company_information = attr.ib(
        default=None,
        converter=ContactInformation.from_data,
        metadata={"tdx_name": "CompanyInformation"},
    )

    #: The name of the primary contact.
    contact_name = attr.ib(default=None, metadata={"tdx_name": "ContactName"})

    #: The title of the primary contact.
    contact_title = attr.ib(default=None, metadata={"tdx_name": "ContactTitle"})

    #: The department of the primary contact.
    contact_department = attr.ib(
        default=None, metadata={"tdx_name": "ContactDepartment"}
    )

    #: The email address of the primary contact.
    contact_email = attr.ib(default=None, metadata={"tdx_name": "ContactEmail"})

    #: The information for the primary contact at the company.
    primary_contact_information = attr.ib(
        default=None,
        converter=ContactInformation.from_data,
        metadata={"tdx_name": "PrimaryContactInformation"},
    )

    #: The number of contracts provided by this vendor.
    contracts_count = attr.ib(default=None, metadata={"tdx_name": "ContractsCount"})

    #: The number of product models manufactured by this vendor.
    product_models_count = attr.ib(
        default=None, metadata={"tdx_name": "ProductModelsCount"}
    )

    #: The number of assets supplied by this vendor.
    assets_supplied_count = attr.ib(
        default=None, metadata={"tdx_name": "AssetsSuppliedCount"}
    )

    #: The custom attributes associated with the vendor.
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

    #: The uid of the last person to modify the vendor.
    modified_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ModifiedUid"}
    )

    #: The full name of the last person to modify the vendor.
    modified_full_name = attr.ib(
        default=None, metadata={"tdx_name": "ModifiedFullName"}
    )
