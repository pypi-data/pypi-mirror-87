import attr

from tdxapi.enums.aggregate_function import AggregateFunction
from tdxapi.enums.column_data_type import ColumnDataType
from tdxapi.enums.component_function import ComponentFunction
from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class DisplayColumn(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Reporting.DisplayColumn"

    #: The text of the column header.
    header_text = attr.ib(default=None, metadata={"tdx_name": "HeaderText"})

    #: The name of the column that is selected back.
    column_name = attr.ib(default=None, metadata={"tdx_name": "ColumnName"})

    #: The type of the data selected for the column.
    data_type = attr.ib(
        default=ColumnDataType.GENERIC_DATA,
        converter=ColumnDataType,
        metadata={"tdx_name": "DataType"},
    )

    #: The full expression for sorting (including direction), or null if the column
    #: does not support sorting.
    sort_column_expression = attr.ib(
        default=None, metadata={"tdx_name": "SortColumnExpression"}
    )

    #: The name of the column used to sort, or null if the column does not
    #: support sorting.
    sort_column_name = attr.ib(default=None, metadata={"tdx_name": "SortColumnName"})

    #: The type of data in the column used to sort.
    sort_data_type = attr.ib(
        default=ColumnDataType.GENERIC_DATA,
        converter=ColumnDataType,
        metadata={"tdx_name": "SortDataType"},
    )

    #: The aggregate function being applied to calculate this column.
    aggregate = attr.ib(
        default=AggregateFunction.NONE,
        converter=AggregateFunction,
        metadata={"tdx_name": "Aggregate"},
    )

    #: The component function being applied to this column.
    component = attr.ib(
        default=ComponentFunction.NONE,
        converter=ComponentFunction,
        metadata={"tdx_name": "Component"},
    )

    #: The expression used to calculate the column's footer.
    footer_expression = attr.ib(default=None, metadata={"tdx_name": "FooterExpression"})
