import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.chart_setting import ChartSetting
from tdxapi.models.converters import to_datetime, to_uid
from tdxapi.models.display_column import DisplayColumn
from tdxapi.models.order_by_column import OrderByColumn


@attr.s(kw_only=True)
class Report(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Reporting.Report"

    #: The report description.
    description = attr.ib(default=None, metadata={"tdx_name": "Description"})

    #: The maximum number of results that can be returned by the report.
    max_results = attr.ib(default=None, metadata={"tdx_name": "MaxResults"})

    #: The columns displayed for the report.
    displayed_columns = attr.ib(
        default=attr.Factory(list),
        converter=DisplayColumn.from_data,
        metadata={"tdx_name": "DisplayedColumns"},
    )

    #: The columns used to sort the rows in the report.
    sort_order = attr.ib(
        default=attr.Factory(list),
        converter=OrderByColumn.from_data,
        metadata={"tdx_name": "SortOrder"},
    )

    #: The type of the chart/graph that is configured for the report.
    chart_type = attr.ib(default=None, metadata={"tdx_name": "ChartType"})

    #: The chart settings for the report.
    chart_settings = attr.ib(
        default=attr.Factory(list),
        converter=ChartSetting.from_data,
        metadata={"tdx_name": "ChartSettings"},
    )

    #: The rows of data retrieved for the report, or null if report data is not
    #: being retrieved.
    data = attr.ib(default=attr.Factory(list), metadata={"tdx_name": "DataRows"})

    #: The id of the report.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The name of the report.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The uid of the creator.
    created_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "CreatedUid"}
    )

    #: The full name of the creator.
    created_full_name = attr.ib(default=None, metadata={"tdx_name": "CreatedFullName"})

    #: The date/time the report was created.
    created_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CreatedDate"}
    )

    #: The name of the associated system application.
    app_class = attr.ib(default=None, metadata={"tdx_name": "SystemAppName"})

    #: The id of the containing platform application.
    app_id = attr.ib(default=None, metadata={"tdx_name": "PlatformAppID"})

    #: The name of the containing platform application.
    app_name = attr.ib(default=None, metadata={"tdx_name": "PlatformAppName"})

    #: The id of the associated report source.
    source_id = attr.ib(default=None, metadata={"tdx_name": "ReportSourceID"})

    #: The name of the associated report source.
    source_name = attr.ib(default=None, metadata={"tdx_name": "ReportSourceName"})

    #: The uri to retrieve the individual report.
    uri = attr.ib(default=None, metadata={"tdx_name": "Uri"})
