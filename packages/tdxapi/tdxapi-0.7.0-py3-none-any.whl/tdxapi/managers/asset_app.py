from datetime import datetime
from typing import List, Optional

import attr

from tdxapi.managers.asset import AssetManager
from tdxapi.managers.asset_status import AssetStatusManager
from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.managers.configuration_item import ConfigurationItemManager
from tdxapi.managers.configuration_item_type import ConfigurationItemTypeManager
from tdxapi.managers.configuration_relationship_type import (
    ConfigurationRelationshipTypeManager,
)
from tdxapi.managers.mixins import TdxAppMixin
from tdxapi.managers.product_model import ProductModelManager
from tdxapi.managers.product_type import ProductTypeManager
from tdxapi.managers.vendor import VendorManager
from tdxapi.models.form import Form
from tdxapi.models.item_updates_page import ItemUpdatesPage


@attr.s
class AssetApplication(TdxManager, TdxAppMixin):
    def __attrs_post_init__(self):
        self.assets = AssetManager(self.dispatcher, self.app_id)
        self.cis = ConfigurationItemManager(self.dispatcher, self.app_id)
        self.ci_types = ConfigurationItemTypeManager(self.dispatcher, self.app_id)
        self.ci_relationship_types = ConfigurationRelationshipTypeManager(
            self.dispatcher, self.app_id
        )
        self.product_models = ProductModelManager(self.dispatcher, self.app_id)
        self.product_types = ProductTypeManager(self.dispatcher, self.app_id)
        self.statuses = AssetStatusManager(self.dispatcher, self.app_id)
        self.vendors = VendorManager(self.dispatcher, self.app_id)

    @tdx_method(
        "GET",
        "/api/{appId}/assets/feed"
        "?DateFrom={DateFrom}&DateTo={DateTo}"
        "&ReplyCount={ReplyCount}&ReturnCount={ReturnCount}",
    )
    def get_feed_page(
        self,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        reply_count: Optional[int] = None,
        return_count: Optional[int] = None,
    ) -> ItemUpdatesPage:
        """Gets feed items for an asset application feed matching the specified search.

        :param date_from: the maximum (latest) last-updated date to filter on. This is
            not inclusive of the date. .
        :param date_to: the minimum (earliest) last-updated date to filter on. This is
            not inclusive of the date.
        :param reply_count: the number of replies per feed entry. Must be in the range
            0-100, and will default to 3.
        :param return_count: the number of feed entries returned by the search. Must
            be in the range 1-100, and will default to 25.
        """
        return self.dispatcher.send(
            self.get_feed_page.method,
            self.get_feed_page.url.format(
                appId=self.app_id,
                DateFrom=date_from,
                DateTo=date_to,
                ReplyCount=reply_count,
                ReturnCount=return_count,
            ),
            rclass=ItemUpdatesPage,
            rlist=False,
            rpartial=True,
        )

    @tdx_method("GET", "/api/{appId}/assets/forms")
    def get_asset_forms(self) -> List[Form]:
        """Gets all active asset forms for the specified application."""
        return self.dispatcher.send(
            self.get_asset_forms.method,
            self.get_asset_forms.url.format(appId=self.app_id),
            rclass=Form,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("GET", "/api/{appId}/cmdb/forms")
    def get_ci_forms(self) -> List[Form]:
        """Gets all active configuration item forms for the specified application."""
        return self.dispatcher.send(
            self.get_ci_forms.method,
            self.get_ci_forms.url.format(appId=self.app_id),
            rclass=Form,
            rlist=True,
            rpartial=True,
        )
