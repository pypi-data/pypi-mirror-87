import attr

from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class ContactInformation(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Assets.ContactInformation"

    #: The id.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The first address line.
    address_line1 = attr.ib(default=None, metadata={"tdx_name": "AddressLine1"})

    #: The second address line.
    address_line2 = attr.ib(default=None, metadata={"tdx_name": "AddressLine2"})

    #: The third address line.
    address_line3 = attr.ib(default=None, metadata={"tdx_name": "AddressLine3"})

    #: The fourth address line.
    address_line4 = attr.ib(default=None, metadata={"tdx_name": "AddressLine4"})

    #: The city.
    city = attr.ib(default=None, metadata={"tdx_name": "City"})

    #: The state/province.
    state = attr.ib(default=None, metadata={"tdx_name": "State"})

    #: The postal code.
    postal_code = attr.ib(default=None, metadata={"tdx_name": "PostalCode"})

    #: The country.
    country = attr.ib(default=None, metadata={"tdx_name": "Country"})

    #: The url.
    url = attr.ib(default=None, metadata={"tdx_name": "Url"})

    #: The phone number.
    phone = attr.ib(default=None, metadata={"tdx_name": "Phone"})

    #: The fax number.
    fax = attr.ib(default=None, metadata={"tdx_name": "Fax"})
