import html
import re

import attr

from tdxapi.enums.feed_item_type import FeedItemType
from tdxapi.enums.update_type import UpdateType
from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime, to_uid
from tdxapi.models.item_update_like import ItemUpdateLike
from tdxapi.models.item_update_reply import ItemUpdateReply
from tdxapi.models.participant import Participant


@attr.s(kw_only=True)
class ItemUpdate(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Feed.ItemUpdate"

    #: The id of the feed entry.
    id = attr.ib(default=None, metadata={"tdx_name": "ID"})

    #: The uid of the creator.
    created_uid = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "CreatedUid"}
    )

    #: The integer based id of the creator.
    created_ref_id = attr.ib(default=None, metadata={"tdx_name": "CreatedRefID"})

    #: The full name of the creator.
    created_full_name = attr.ib(default=None, metadata={"tdx_name": "CreatedFullName"})

    #: The first name of the creator.
    created_first_name = attr.ib(
        default=None, metadata={"tdx_name": "CreatedFirstName"}
    )

    #: The last name of the creator.
    created_last_name = attr.ib(default=None, metadata={"tdx_name": "CreatedLastName"})

    #: The profile image file name of the creator.
    created_profile_image_file_name = attr.ib(
        default=None, metadata={"tdx_name": "CreatedByPicPath"}
    )

    #: The creation date of the feed entry.
    created_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "CreatedDate"}
    )

    #: The date the feed entry was last updated. Replying to this feed entry will
    #: update this date.
    modified_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "LastUpdatedDate"}
    )

    #: The id of the associated project.
    project_id = attr.ib(default=None, metadata={"tdx_name": "ProjectID"})

    #: The name of the associated project.
    project_name = attr.ib(default=None, metadata={"tdx_name": "ProjectName"})

    #: The id of the associated plan or ticket.
    plan_id = attr.ib(default=None, metadata={"tdx_name": "PlanID"})

    #: The name of the associated plan or ticket.
    plan_name = attr.ib(default=None, metadata={"tdx_name": "PlanName"})

    #: The item type.
    item_type = attr.ib(
        default=FeedItemType.NONE,
        converter=FeedItemType,
        metadata={"tdx_name": "ItemType"},
    )

    #: The item id.
    item_id = attr.ib(default=None, metadata={"tdx_name": "ItemID"})

    #: The item title.
    item_title = attr.ib(default=None, metadata={"tdx_name": "ItemTitle"})

    #: The reference id. This value is used when the associated item is normally
    #: referred to by a guid.
    ref_id = attr.ib(
        default=None, converter=to_uid, metadata={"tdx_name": "ReferenceID"}
    )

    #: The body of the feed entry.
    body = attr.ib(default=None, metadata={"tdx_name": "Body"})

    #: The type of the feed entry.
    type = attr.ib(default=0, converter=UpdateType, metadata={"tdx_name": "UpdateType"})

    #: The list of notified people.
    notified_list = attr.ib(default=None, metadata={"tdx_name": "NotifiedList"})

    #: A value indicating whether this feed entry is private.
    is_private = attr.ib(default=None, metadata={"tdx_name": "IsPrivate"})

    #: A value indicating whether this feed entry is a parent for other feed entries.
    is_parent = attr.ib(default=None, metadata={"tdx_name": "IsParent"})

    #: The replies to this feed entry.
    replies = attr.ib(
        default=attr.Factory(list),
        converter=ItemUpdateReply.from_data,
        metadata={"tdx_name": "Replies"},
    )

    #: The number of replies to this feed entry.
    replies_count = attr.ib(default=None, metadata={"tdx_name": "RepliesCount"})

    #: The likes for this feed entry.
    likes = attr.ib(
        default=attr.Factory(list),
        converter=ItemUpdateLike.from_data,
        metadata={"tdx_name": "Likes"},
    )

    #: A value inidcating whether this feed entry is liked by the user.
    ilike = attr.ib(default=None, metadata={"tdx_name": "ILike"})

    #: The number of likes for this feed entry.
    likes_count = attr.ib(default=None, metadata={"tdx_name": "LikesCount"})

    #: The participants. This list consists of the person who is responsible for the
    #: original feed entry as well as any other individuals who have replied to it.
    participants = attr.ib(
        default=attr.Factory(list),
        converter=Participant.from_data,
        metadata={"tdx_name": "Participants"},
    )

    #: The breadcrumbs html. This is not loaded from the database; it is used purely
    #: for the purpose of sending html to the client for rendering breadcrumbs, and
    #: should be popualted by the calling application.
    breadcrumbs_html = attr.ib(default=None, metadata={"tdx_name": "BreadcrumbsHtml"})

    #: A value indicating whether this instance has an attachment.
    has_attachment = attr.ib(default=None, metadata={"tdx_name": "HasAttachment"})

    @property
    def body_text(self):
        # Remove HTML tags
        regex = re.compile("<.*?>")
        clean_text = re.sub(regex, "", self.body)

        # Return HTML decoded text with line breaks removed
        return " ".join(html.unescape(clean_text).split())
