import attr

from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class ChartSetting(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Reporting.ChartSetting"

    #: The axis represented by this setting.
    axis = attr.ib(default=None, metadata={"tdx_name": "Axis"})

    #: The label describing the column used for the setting.
    column_label = attr.ib(default=None, metadata={"tdx_name": "ColumnLabel"})

    #: The name of the column used for the setting.
    column_name = attr.ib(default=None, metadata={"tdx_name": "ColumnName"})
