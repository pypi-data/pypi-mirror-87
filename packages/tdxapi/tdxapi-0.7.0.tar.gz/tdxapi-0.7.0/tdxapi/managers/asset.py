from datetime import datetime
from typing import Any, List, Optional, Tuple

import attr

from tdxapi.enums.component import Component
from tdxapi.managers import helpers
from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.managers.mixins import TdxAppMixin, TdxCustomAttributeMixin
from tdxapi.models.asset import Asset
from tdxapi.models.asset_search import AssetSearch
from tdxapi.models.attachment import Attachment
from tdxapi.models.feed_entry import FeedEntry
from tdxapi.models.item_update import ItemUpdate
from tdxapi.models.resource_item import ResourceItem


@attr.s
class AssetManager(TdxManager, TdxAppMixin, TdxCustomAttributeMixin):
    __tdx_component__ = Component.ASSET

    @tdx_method("GET", "/api/{appId}/assets/{id}")
    def get(self, asset_id: int) -> Asset:
        """Gets an asset."""
        asset = self.dispatcher.send(
            self.get.method,
            self.get.url.format(appId=self.app_id, id=asset_id),
            rclass=Asset,
            rlist=False,
            rpartial=False,
        )

        if asset:
            asset.attributes.match_template(self.attribute_template)

        return asset

    @tdx_method("POST", "/api/{appId}/assets/search")
    def search(
        self,
        serial_like: Optional[str] = None,
        external_ids: Optional[List[str]] = None,
        search_text: Optional[str] = None,
        custom_attributes: Optional[List[Tuple[int, Any]]] = None,
        product_model_ids: Optional[List[int]] = None,
        supplier_ids: Optional[List[int]] = None,
        manufacturer_ids: Optional[List[int]] = None,
        location_ids: Optional[List[int]] = None,
        room_id: Optional[int] = None,
        owning_department_ids: Optional[List[int]] = None,
        owning_department_ids_past: Optional[List[int]] = None,
        requesting_department_ids: Optional[List[int]] = None,
        using_department_ids: Optional[List[int]] = None,
        owning_customer_ids: Optional[List[str]] = None,
        owning_customer_ids_past: Optional[List[str]] = None,
        requesting_customer_ids: Optional[List[str]] = None,
        using_customer_ids: Optional[List[str]] = None,
        maintenance_schedule_ids: Optional[List[int]] = None,
        expected_replacement_date_from: Optional[datetime] = None,
        expected_replacement_date_to: Optional[datetime] = None,
        acquisition_date_from: Optional[datetime] = None,
        acquisition_date_to: Optional[datetime] = None,
        purchase_cost_from: Optional[float] = None,
        purchase_cost_to: Optional[float] = None,
        contract_provider_id: Optional[int] = None,
        contract_ids: Optional[List[int]] = None,
        exclude_contract_ids: Optional[List[int]] = None,
        contract_end_date_from: Optional[datetime] = None,
        contract_end_date_to: Optional[datetime] = None,
        status_ids: Optional[List[int]] = None,
        status_ids_past: Optional[List[int]] = None,
        saved_search_id: Optional[int] = None,
        form_ids: Optional[List[int]] = None,
        ticket_ids: Optional[List[int]] = None,
        exclude_ticket_ids: Optional[List[int]] = None,
        parent_ids: Optional[List[int]] = None,
        only_parent_assets: Optional[bool] = None,
        is_in_service: Optional[bool] = None,
        max_results: Optional[int] = None,
    ) -> List[Asset]:
        """Gets a list of assets.

        :param serial_like: the text to perform a LIKE search on for the asset serial
            number and tag.
        :param external_ids: the external IDs to filter on. Only assets that have one of
            these external ID values will be included.
        :param search_text: the search text to filter on. If this is set, this will sort
            the results by their text relevancy.
        :param custom_attributes: the custom attributes to filter on.
        :param product_model_ids: the product model IDs to filter on. Only assets that
            are one of these product models will be included.
        :param supplier_ids: the supplier IDs to filter on. Only assets that are
            supplied by one of these vendors will be included.
        :param manufacturer_ids: the manufacturer IDs to filter on. Only assets that are
            manufactured by one of these vendors will be included.
        :param location_ids: the location IDs to filter on. Only assets that are at one
            of these locations will be included.
        :param room_id: the room ID to filter on. Only assets that are located in this
            room will be included.
        :param owning_department_ids: the owning account/department IDs to filter on.
            Only assets that are currently owned by one of these accounts will be
            included.
        :param owning_department_ids_past: the past owning account/department IDs to
            filter on. Only assets that have been historically owned by one or more of
            these accounts will be included.
        :param requesting_department_ids: the requested account/department IDs to filter
            on. Only assets that are listed as requested by one of these accounts will
            be included.
        :param using_department_ids: the using account/department IDs to filter on. Only
            assets that are currently used by one or more of these accounts will be
            included.
        :param owning_customer_ids: the owner IDs to filter on. Only assets that are
            currently owned by one of these people will be included.
        :param owning_customer_ids_past: the past owner IDs to filter on. Only assets
            that have been historically owned by one or more of these people will be included.
        :param requesting_customer_ids: the requestor IDs to filter on. Only assets that
            are listed as requested by one of these people will be included.
        :param using_customer_ids: the using person IDs to filter on. Only assets that
            are currently used by one or more of these people will be included.
        :param maintenance_schedule_ids: the maintenance window IDs to filter on. Only
            assets that have one of these maintenance windows will be included.
        :param expected_replacement_date_from: the minimum expected replacement date to
            filter on.
        :param expected_replacement_date_to: the maximum expected replacement date to
            filter on.
        :param acquisition_date_from: the minimum acquisition date to filter on.
        :param acquisition_date_to: the maximum acquisition date to filter on.
        :param purchase_cost_from: the minimum purchase cost to filter on.
        :param purchase_cost_to: the maximum purchase cost to filter on.
        :param contract_provider_id: the contract provider to filter on. Only assets
            that belong to at least one contract provided by this vendor will be included.
        :param contract_ids: the contract IDs to filter on. Only assets that belong to
            one or more of these contracts will be included.
        :param exclude_contract_ids: the contract IDs to exclude on. Only assets that do
            NOT belong to any of these contracts will be included.
        :param contract_end_date_from: the minimum contract end date to filter on.
        :param contract_end_date_to: the maximum contract end date to filter on.
        :param status_ids: the current status IDs to filter on. Only assets that
            currently have one of these statuses will be included.
        :param status_ids_past: the past status IDs to filter on. Only assets that have
            had one of these statuses will be included.
        :param saved_search_id: the ID of the saved search this search is associated
            with
        :param form_ids: the form IDs to filter on. Only assets that use one or more of
            these forms will be included.
        :param ticket_ids: the ticket IDs to filter on. Only assets that are associated
            with one or more of these tickets will be included.
        :param exclude_ticket_ids: the ticket IDs to exclude on. Only assets that are
            NOT associated with any of these tickets will be included.
        :param parent_ids: the parent asset IDs to filter on. Only assets that have one
            of these listed as a parent will be included.
        :param only_parent_assets: a value indicating whether only assets that are
            parents should be included.
        :param is_in_service: the "in service" status to filter on (based on the out of
            service flag of each asset's status).
        :param max_results: the maximum number of records to return.
        """
        params = helpers.format_search_params(AssetSearch, self, locals())

        return self.dispatcher.send(
            self.search.method,
            self.search.url.format(appId=self.app_id),
            data=params,
            rclass=Asset,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("POST", "/api/{appId}/assets/{id}/feed")
    def add_feed_entry(
        self, comments: str, asset_id: int, notify: Optional[List[str]] = None
    ) -> ItemUpdate:
        """Add a comment to an asset."""
        return self.dispatcher.send(
            self.add_feed_entry.method,
            self.add_feed_entry.url.format(appId=self.app_id, id=asset_id),
            data=FeedEntry(comments=comments, notify=helpers.build_notify_list(notify)),
            rclass=ItemUpdate,
            rlist=False,
            rpartial=True,
        )

    @tdx_method("GET", "/api/{appId}/assets/{id}/feed")
    def get_feed_entries(self, asset_id: int) -> List[ItemUpdate]:
        """Gets the feed entries for an asset."""
        return self.dispatcher.send(
            self.get_feed_entries.method,
            self.get_feed_entries.url.format(appId=self.app_id, id=asset_id),
            rclass=ItemUpdate,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("POST", "/api/{appId}/assets/{id}/users/{resourceID}")
    def add_resource(self, resource_id: str, asset_id: int) -> ResourceItem:
        """Adds a resource to asset."""
        return self.dispatcher.send(
            self.add_resource.method,
            self.add_resource.url.format(
                appId=self.app_id, id=asset_id, resourceID=resource_id
            ),
            rclass=ResourceItem,
            rlist=False,
            rpartial=True,
        )

    @tdx_method("DELETE", "/api/{appId}/assets/{assetId}/users/{resourceID}")
    def remove_resource(self, resource_id: str, asset_id: int) -> None:
        """Removes a resource from an asset."""
        self.dispatcher.send(
            self.remove_resource.method,
            self.remove_resource.url.format(
                appId=self.app_id, assetId=asset_id, resourceID=resource_id
            ),
        )

    @tdx_method("GET", "/api/{appId}/assets/{id}/users")
    def get_resources(self, asset_id: int) -> List[ResourceItem]:
        """Gets the asset resources."""
        return self.dispatcher.send(
            self.get_resources.method,
            self.get_resources.url.format(appId=self.app_id, id=asset_id),
            rclass=ResourceItem,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("POST", "/api/{appId}/assets/{id}/tickets/{ticketId}")
    def add_to_ticket(self, ticket_id: int, asset_id: int) -> None:
        """Adds an asset to a ticket."""
        self.dispatcher.send(
            self.add_to_ticket.method,
            self.add_to_ticket.url.format(
                appId=self.app_id, id=asset_id, ticketId=ticket_id
            ),
        )

    @tdx_method("DELETE", "/api/{appId}/assets/{id}/tickets/{ticketID}")
    def remove_from_ticket(self, ticket_id: int, asset_id: int) -> None:
        """Removes a ticket from an asset."""
        self.dispatcher.send(
            self.remove_from_ticket.method,
            self.remove_from_ticket.url.format(
                appId=self.app_id, id=asset_id, ticketID=ticket_id
            ),
        )

    @tdx_method("POST", "/api/{appId}/assets/{id}/attachments")
    def add_attachment(
        self,
        filepath: str,
        asset_id: int,
        filename: Optional[str] = None,
        mimetype: Optional[str] = None,
    ) -> Attachment:
        """Uploads an attachment to an asset."""
        return self.dispatcher.send(
            self.add_attachment.method,
            self.add_attachment.url.format(appId=self.app_id, id=asset_id),
            file=filepath,
            filename=filename,
            mimetype=mimetype,
            rclass=Attachment,
            rlist=False,
            rpartial=True,
        )

    def new(self, **kwargs) -> Asset:
        """Generate new Asset object."""
        return helpers.new_model(Asset, self, **kwargs)

    def save(self, asset: Asset, force: Optional[bool] = False) -> None:
        """Create or update an Asset."""
        helpers.save_model(asset, self, force)

    @tdx_method("POST", "/api/{appId}/assets")
    def _create(self, asset: Asset) -> Asset:
        """Creates an asset."""
        return self.dispatcher.send(
            self._create.method,
            self._create.url.format(appId=self.app_id),
            data=asset,
            rclass=Asset,
            rlist=False,
            rpartial=False,
        )

    @tdx_method("POST", "/api/{appId}/assets/{id}")
    def _update(self, asset: Asset) -> Asset:
        """Edits an existing asset."""
        return self.dispatcher.send(
            self._update.method,
            self._update.url.format(appId=self.app_id, id=asset.id),
            data=asset,
            rclass=Asset,
            rlist=False,
            rpartial=False,
        )
