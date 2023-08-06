import attr

from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class GroupApplication(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Users.GroupApplication"

    #: The ID of the associated group.
    group_id = attr.ib(default=None, metadata={"tdx_name": "GroupID"})

    #: The ID of the associated platform application.
    app_id = attr.ib(default=None, metadata={"tdx_name": "AppID"})

    #: The name of the associated platform application.
    app_name = attr.ib(default=None, metadata={"tdx_name": "AppName"})

    #: The description of the associated platform application.
    app_description = attr.ib(default=None, metadata={"tdx_name": "AppDescription"})

    #: The application class of the associated platform application.
    app_class = attr.ib(default=None, metadata={"tdx_name": "AppClass"})
