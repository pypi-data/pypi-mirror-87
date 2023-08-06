import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_uid
from tdxapi.models.custom_attribute_list import CustomAttributeList


@attr.s(kw_only=True)
class AccountSearch(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Accounts.AccountSearch"

    #: The search text to use.
    search_text = attr.ib(default=None, metadata={"tdx_name": "SearchText"})

    #: The uids of the department managers to filter on.
    manager_uids = attr.ib(
        default=attr.Factory(list),
        converter=to_uid,
        metadata={"tdx_name": "ManagerUids"},
    )

    #: The custom attributes to filter on.
    custom_attributes = attr.ib(
        default=attr.Factory(CustomAttributeList),
        converter=CustomAttributeList.from_data,
        metadata={"tdx_name": "CustomAttributes"},
    )

    #: The active status to filter on.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: The maximum number of records to return.
    max_results = attr.ib(default=0, metadata={"tdx_name": "MaxResults"})

    #: The id of the parent account to filter on.
    parent_account_id = attr.ib(default=None, metadata={"tdx_name": "ParentAccountID"})

    #: The name of the parent account to filter on.
    parent_account_name = attr.ib(
        default=None, metadata={"tdx_name": "ParentAccountName"}
    )
