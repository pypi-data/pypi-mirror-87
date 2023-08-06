import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime, to_uid


@attr.s(kw_only=True)
class ConfigurationItemRelationship(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Cmdb.ConfigurationItemRelationship"

    #: The id.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The id of the parent ci.
    parent_id = attr.ib(default=None, metadata={"tdx_name": "ParentID"})

    #: The name of the parent ci.
    parent_name = attr.ib(default=None, metadata={"tdx_name": "ParentName"})

    #: The type id of the parent ci.
    parent_type_id = attr.ib(default=None, metadata={"tdx_name": "ParentTypeID"})

    #: The type name of the parent ci.
    parent_type_name = attr.ib(default=None, metadata={"tdx_name": "ParentTypeName"})

    #: The id of the child ci.
    child_id = attr.ib(default=None, metadata={"tdx_name": "ChildID"})

    #: The name of the child ci.
    child_name = attr.ib(default=None, metadata={"tdx_name": "ChildName"})

    #: The type id of the child ci.
    child_type_id = attr.ib(default=None, metadata={"tdx_name": "ChildTypeID"})

    #: The type name of the child ci.
    child_type_name = attr.ib(default=None, metadata={"tdx_name": "ChildTypeName"})

    #: A value indicating whether this relationship is maintained automatically by
    #: the system.
    is_system_defined = attr.ib(
        default=None, metadata={"tdx_name": "IsSystemMaintained"}
    )

    #: The id of the type used for the relationship.
    relationship_type_id = attr.ib(
        default=None, metadata={"tdx_name": "RelationshipTypeID"}
    )

    #: The description of the relationship from the perspective of the parent ci.
    description = attr.ib(default=None, metadata={"tdx_name": "Description"})

    #: The description of the relationship from the perspective of the child ci.
    inverse_description = attr.ib(
        default=None, metadata={"tdx_name": "InverseDescription"}
    )

    #: A value indicating if this relationship is an operational dependency.
    is_operational_dependency = attr.ib(
        default=None, metadata={"tdx_name": "IsOperationalDependency"}
    )

    #: The date/time the relationship was created.
    created_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CreatedDateUtc"}
    )

    #: The uid of the creator.
    created_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "CreatedUID"}
    )

    #: The full name of the creator.
    created_full_name = attr.ib(default=None, metadata={"tdx_name": "CreatedFullName"})
