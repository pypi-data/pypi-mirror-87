import attr

from tdxapi.models.bases import TdxModel


@attr.s(kw_only=True)
class Permission(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Roles.Permission"

    #: The id of the permission.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The short name for the permission.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The full description for the permission.
    description = attr.ib(default=None, metadata={"tdx_name": "Description"})

    #: The id of the containing section.
    section_id = attr.ib(default=None, metadata={"tdx_name": "SectionID"})

    #: The name of the containing section.
    section_name = attr.ib(default=None, metadata={"tdx_name": "SectionName"})
