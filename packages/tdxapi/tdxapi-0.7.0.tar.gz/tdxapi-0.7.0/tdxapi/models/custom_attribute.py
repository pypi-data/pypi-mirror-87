import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.custom_attribute_choice import CustomAttributeChoice


@attr.s(kw_only=True)
class CustomAttribute(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.CustomAttributes.CustomAttribute"

    #: The attribute id.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The attribute name.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The order of the attribute. Attributes are first sorted by order (ascending)
    #: and their name (also ascending).
    order = attr.ib(default=None, metadata={"tdx_name": "Order"})

    #: The attribute description.
    description = attr.ib(default=None, metadata={"tdx_name": "Description"})

    #: The id of the associated attribute section.
    section_id = attr.ib(default=None, metadata={"tdx_name": "SectionID"})

    #: The name of the associated attribute section.
    section_name = attr.ib(default=None, metadata={"tdx_name": "SectionName"})

    #: The field type of the attribute.
    field_type = attr.ib(default=None, metadata={"tdx_name": "FieldType"})

    #: The data type of the attribute.
    data_type = attr.ib(default=None, metadata={"tdx_name": "DataType"})

    #: The choices for the attribute.
    choices = attr.ib(
        default=attr.Factory(list),
        converter=CustomAttributeChoice.from_data,
        metadata={"tdx_name": "Choices"},
    )

    #: A value indicating whether the attribute is required.
    is_required = attr.ib(default=None, metadata={"tdx_name": "IsRequired"})

    #: A value indicating whether the attribute is updatable.
    is_updatable = attr.ib(default=None, metadata={"tdx_name": "IsUpdatable"})

    #: The value of the attribute.
    value = attr.ib(default=None, metadata={"tdx_name": "Value"})

    #: The text value of the attribute. For choice attributes, this will be a comma
    #: separated list of all the currently selected choices (referenced by choice id).
    value_text = attr.ib(default=None, metadata={"tdx_name": "ValueText"})

    #: The text of the selected choices. This will be a comma-separated list of
    #: the text of each selected choice.
    choices_text = attr.ib(default=None, metadata={"tdx_name": "ChoicesText"})

    #: The list of all item types (represented as ids) that are associated with
    #: the attribute.
    associated_item_ids = attr.ib(
        default=attr.Factory(list), metadata={"tdx_name": "AssociatedItemIDs"}
    )
