import attr

from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class OrderByColumn(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Reporting.OrderByColumn"

    #: The label describing the column used to sort.
    column_label = attr.ib(default=None, metadata={"tdx_name": "ColumnLabel"})

    #: The name of the column used to sort.
    column_name = attr.ib(default=None, metadata={"tdx_name": "ColumnName"})

    #: A value indicating whether this column uses ascending or descending order.
    is_ascending = attr.ib(default=None, metadata={"tdx_name": "IsAscending"})
