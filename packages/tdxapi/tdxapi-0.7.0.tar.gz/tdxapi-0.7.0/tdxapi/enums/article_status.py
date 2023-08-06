from enum import Enum


class ArticleStatus(Enum):
    """Describes the different article statuses."""

    __tdx_type__ = "TeamDynamix.Api.KnowledgeBase.ArticleStatus"

    #: A "none" status for filtering purposes. Should not be used in normal operations.
    NONE = 0

    #: Used for articles that have not been submitted.
    NOT_SUBMITTED = 1

    #: Used for articles that have been submitted.
    SUBMITTED = 2

    #: Used for articles that have been approved.
    APPROVED = 3

    #: Used for articles that have been rejected.
    REJECTED = 4

    #: Used for articles that have been archived.
    ARCHIVED = 5
