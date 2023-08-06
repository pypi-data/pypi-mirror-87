import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime, to_uid
from tdxapi.models.custom_attribute_list import CustomAttributeList


@attr.s(kw_only=True)
class Account(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Accounts.Account"

    #: The id.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The name.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The id of the account's parent. set to null if the account has no parent.
    parent_id = attr.ib(default=None, metadata={"tdx_name": "ParentID"})

    #: The name of the account's parent.
    parent_name = attr.ib(default=None, metadata={"tdx_name": "ParentName"})

    #: The active status.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: The first address line.
    address_line1 = attr.ib(default=None, metadata={"tdx_name": "Address1"})

    #: The second address line.
    address_line2 = attr.ib(default=None, metadata={"tdx_name": "Address2"})

    #: The third address line.
    address_line3 = attr.ib(default=None, metadata={"tdx_name": "Address3"})

    #: The fourth address line.
    address_line4 = attr.ib(default=None, metadata={"tdx_name": "Address4"})

    #: The city.
    city = attr.ib(default=None, metadata={"tdx_name": "City"})

    #: The name of the state/province.
    state_name = attr.ib(default=None, metadata={"tdx_name": "StateName"})

    #: The abbreviation of the state/province.
    state_abbr = attr.ib(default=None, metadata={"tdx_name": "StateAbbr"})

    #: The postal code.
    postal_code = attr.ib(default=None, metadata={"tdx_name": "PostalCode"})

    #: The country.
    country = attr.ib(default=None, metadata={"tdx_name": "Country"})

    #: The phone number.
    phone = attr.ib(default=None, metadata={"tdx_name": "Phone"})

    #: The fax number.
    fax = attr.ib(default=None, metadata={"tdx_name": "Fax"})

    #: The website url.
    url = attr.ib(default=None, metadata={"tdx_name": "Url"})

    #: The account notes.
    notes = attr.ib(default=None, metadata={"tdx_name": "Notes"})

    #: The created date.
    created_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CreatedDate"}
    )

    #: The last modified date.
    modified_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "ModifiedDate"}
    )

    #: The account code.
    code = attr.ib(default=None, metadata={"tdx_name": "Code"})

    #: The industry id.
    industry_id = attr.ib(default=None, metadata={"tdx_name": "IndustryID"})

    #: The name of the industry.
    industry_name = attr.ib(default=None, metadata={"tdx_name": "IndustryName"})

    #: The uid of the department manager.
    manager_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ManagerUID"}
    )

    #: The full name of the department manager.
    manager_full_name = attr.ib(default=None, metadata={"tdx_name": "ManagerFullName"})

    #: The custom attributes associated with the account.
    attributes = attr.ib(
        default=attr.Factory(CustomAttributeList),
        converter=CustomAttributeList.from_data,
        metadata={"tdx_name": "Attributes"},
    )
