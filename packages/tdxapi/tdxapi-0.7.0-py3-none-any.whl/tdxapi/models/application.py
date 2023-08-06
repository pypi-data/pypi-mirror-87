import attr

from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class Application(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Apps.OrgApplication"

    #: The application id.
    id = attr.ib(default=None, metadata={"tdx_name": "AppID"})

    #: The application name.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The application description.
    description = attr.ib(default=None, metadata={"tdx_name": "Description"})

    #: The type of application. Types include standard, ticketing, assets/ci,
    #: client portal, or external.
    type = attr.ib(default=None, metadata={"tdx_name": "Type"})

    #: The application class.
    app_class = attr.ib(default=None, metadata={"tdx_name": "AppClass"})

    #: The external url.
    external_url = attr.ib(default=None, metadata={"tdx_name": "ExternalUrl"})

    #: The purpose of ticketing application.
    purpose = attr.ib(default=None, metadata={"tdx_name": "Purpose"})

    #: A value indicating whether the application is active.
    is_active = attr.ib(default=None, metadata={"tdx_name": "Active"})

    #: The client portal partial url.
    partial_url = attr.ib(default=None, metadata={"tdx_name": "PartialUrl"})
