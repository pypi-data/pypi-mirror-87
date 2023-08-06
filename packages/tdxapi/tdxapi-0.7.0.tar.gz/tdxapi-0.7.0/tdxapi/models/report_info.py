import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime, to_uid


@attr.s(kw_only=True)
class ReportInfo(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Reporting.ReportInfo"

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
