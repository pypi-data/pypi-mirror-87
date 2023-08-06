import attr

from tdxapi.enums.component import Component
from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime, to_uid


@attr.s(kw_only=True)
class Form(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Forms.Form"

    #: The form id.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The form name.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The application id.
    app_id = attr.ib(default=None, metadata={"tdx_name": "AppID"})

    #: The name of the containing application.
    app_name = attr.ib(default=None, metadata={"tdx_name": "AppName"})

    #: The component.
    component = attr.ib(
        default=None, converter=Component, metadata={"tdx_name": "ComponentID"}
    )

    #: A value indicating whether this form is active.
    is_active = attr.ib(default=None, metadata={"tdx_name": "IsActive"})

    #: A value indicating whether this form is configured.
    is_configured = attr.ib(default=None, metadata={"tdx_name": "IsConfigured"})

    #: A value indicating whether this form is the default in its containing
    #: application.
    is_default = attr.ib(default=None, metadata={"tdx_name": "IsDefaultForApp"})

    #: A value indicating whether this form is pinned. currently only supported
    #: for tickets.
    is_pinned = attr.ib(default=None, metadata={"tdx_name": "IsPinned"})

    #: A value indicating whether the form will expand help text initially.
    should_expand_help = attr.ib(
        default=None, metadata={"tdx_name": "ShouldExpandHelp"}
    )

    #: The created date.
    created_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CreatedDate"}
    )

    #: The uid of the user who created the form.
    created_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "CreatedUid"}
    )

    #: The full name of the user who created the form.
    created_full_name = attr.ib(default=None, metadata={"tdx_name": "CreatedFullName"})

    #: The last modified date.
    modified_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "ModifiedDate"}
    )

    #: The uid of the user who last modified the form.
    modified_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ModifiedUid"}
    )

    #: The full name of the user who last modified the form.
    modified_full_name = attr.ib(
        default=None, metadata={"tdx_name": "ModifiedFullName"}
    )

    #: The number of assets associated with this form, or -1 if this total has
    #: not been loaded.
    assets_count = attr.ib(default=None, metadata={"tdx_name": "AssetsCount"})

    #: The number of configuration items associated with this form, or -1 if this
    #: total has not been loaded.
    configuration_items_count = attr.ib(
        default=None, metadata={"tdx_name": "ConfigurationItemsCount"}
    )
