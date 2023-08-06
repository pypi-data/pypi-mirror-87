import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_uid


@attr.s(kw_only=True)
class ReportSearch(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Reporting.ReportSearch"

    #: The uid of the owner to filter on. If specified, will only return reports
    #: owned by this user.
    owner_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "OwnerUid"}
    )

    #: The search text to filter on. this will filter on the name of each report.
    search_text = attr.ib(default=None, metadata={"tdx_name": "SearchText"})

    #: The id of the platform application to filter on. If specified, will only
    #: include reports belonging to this application.
    app_id = attr.ib(default=None, metadata={"tdx_name": "ForAppID"})

    #: The name of the system application to filter on. If specified, will only
    #: include reports belonging to this application.
    app_class = attr.ib(default=None, metadata={"tdx_name": "ForApplicationName"})

    #: The id of the report source to filter on. If specified, will only include
    #: reports belonging to this report source.
    source_id = attr.ib(default=None, metadata={"tdx_name": "ReportSourceID"})
