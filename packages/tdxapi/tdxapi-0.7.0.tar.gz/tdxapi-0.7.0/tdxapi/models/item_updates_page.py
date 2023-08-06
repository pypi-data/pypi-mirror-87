import attr

from tdxapi.models.bases import TdxModel
from tdxapi.models.converters import to_datetime
from tdxapi.models.item_update import ItemUpdate


@attr.s(kw_only=True)
class ItemUpdatesPage(TdxModel):
    __tdx_type__ = "TeamDynamix.Api.Feed.ItemUpdatesPage"

    #: The entries in the feed page.
    entries = attr.ib(
        default=attr.Factory(list),
        converter=ItemUpdate.from_data,
        metadata={"tdx_name": "Entries"},
    )

    #: The current data/time.
    as_of_date = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "AsOfDate"}
    )

    #: The date of first item omitted from the feed list, if present.
    next_date_to = attr.ib(
        default=None, converter=to_datetime, metadata={"tdx_name": "NextDateTo"}
    )
