import attr

from tdxapi.enums.attachment_type import AttachmentType
from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime, to_uid


@attr.s(kw_only=True)
class Attachment(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Attachments.Attachment"

    #: The attachment id.
    id = attr.ib(default=None, converter=to_uid, metadata={"tdx_name": "ID"})

    #: The attachment type.
    type = attr.ib(
        default=AttachmentType.NONE,
        converter=AttachmentType,
        metadata={"tdx_name": "AttachmentType"},
    )

    #: The item id.
    item_id = attr.ib(default=None, metadata={"tdx_name": "ItemID"})

    #: The uid of the creator.
    created_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "CreatedUid"}
    )

    #: The full name of the creator.
    created_full_name = attr.ib(default=None, metadata={"tdx_name": "CreatedFullName"})

    #: The creation date.
    created_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CreatedDate"}
    )

    #: The file name.
    name = attr.ib(default=None, metadata={"tdx_name": "Name"})

    #: The size of the attachment, in bytes.
    size = attr.ib(default=None, metadata={"tdx_name": "Size"})

    #: The uri for this attachment.
    uri = attr.ib(default=None, metadata={"tdx_name": "Uri"})

    #: The uri to retrieve the attachment content.
    content_uri = attr.ib(default=None, metadata={"tdx_name": "ContentUri"})

    #: The content of the attachment, or null if content is not being retrieved.
    content = attr.ib(default=None, repr=False, eq=False)
