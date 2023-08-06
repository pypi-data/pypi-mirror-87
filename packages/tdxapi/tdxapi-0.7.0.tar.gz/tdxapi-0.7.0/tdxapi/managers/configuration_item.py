from typing import Any, List, Optional, Tuple

import attr

from tdxapi.enums.component import Component
from tdxapi.managers import helpers
from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.managers.mixins import TdxAppMixin, TdxCustomAttributeMixin
from tdxapi.models.attachment import Attachment
from tdxapi.models.configuration_item import ConfigurationItem
from tdxapi.models.configuration_item_relationship import ConfigurationItemRelationship
from tdxapi.models.configuration_item_search import ConfigurationItemSearch
from tdxapi.models.feed_entry import FeedEntry
from tdxapi.models.item_update import ItemUpdate
from tdxapi.models.ticket_listing import TicketListing


@attr.s
class ConfigurationItemManager(TdxManager, TdxAppMixin, TdxCustomAttributeMixin):
    __tdx_component__ = Component.CONFIGURATION_ITEM

    @tdx_method("GET", "/api/{appId}/cmdb/{id}")
    def get(self, configuration_item_id: int) -> ConfigurationItem:
        """Gets a configuration item."""
        configuration_item = self.dispatcher.send(
            self.get.method,
            self.get.url.format(appId=self.app_id, id=configuration_item_id),
            rclass=ConfigurationItem,
            rlist=False,
            rpartial=False,
        )

        if configuration_item:
            configuration_item.attributes.match_template(self.attribute_template)

        return configuration_item

    @tdx_method("POST", "/api/{appId}/cmdb/search")
    def search(
        self,
        name_like: Optional[str] = None,
        type_ids: Optional[List[int]] = None,
        custom_attributes: Optional[List[Tuple[int, Any]]] = None,
        maintenance_schedule_ids: Optional[List[int]] = None,
        is_active: Optional[bool] = None,
    ) -> List[ConfigurationItem]:
        """Gets a list of configuration items.

        :param name_like: the name text to filter on.
        :param type_ids: the type IDs to filter on.
        :param custom_attributes: the custom attributes to filter on.
        :param maintenance_schedule_ids: the maintenance window IDs to filter on.
        :param is_active: the active status to filter on.
        """
        params = helpers.format_search_params(ConfigurationItemSearch, self, locals())

        return self.dispatcher.send(
            self.search.method,
            self.search.url.format(appId=self.app_id),
            data=params,
            rclass=ConfigurationItem,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("POST", "/api/{appId}/cmdb/{id}/feed")
    def add_feed_entry(
        self,
        comments: str,
        configuration_item_id: int,
        notify: Optional[List[str]] = None,
    ) -> ItemUpdate:
        """Posts a comment to the configuration item's feed."""
        return self.dispatcher.send(
            self.add_feed_entry.method,
            self.add_feed_entry.url.format(appId=self.app_id, id=configuration_item_id),
            data=FeedEntry(comments=comments, notify=helpers.build_notify_list(notify)),
            rclass=ItemUpdate,
            rlist=False,
            rpartial=True,
        )

    @tdx_method("GET", "/api/{appId}/cmdb/{id}/feed")
    def get_feed_entries(self, configuration_item_id: int) -> List[ItemUpdate]:
        """Gets the feed for the configuration items."""
        return self.dispatcher.send(
            self.get_feed_entries.method,
            self.get_feed_entries.url.foramt(
                appId=self.app_id, id=configuration_item_id
            ),
            rclass=ItemUpdate,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("GET", "/api/{appId}/cmdb/{id}/relationships")
    def get_relationships(
        self, configuration_item_id: int
    ) -> List[ConfigurationItemRelationship]:
        """Gets a configuration item's relationships."""
        return self.dispatcher.send(
            self.get_relationships.method,
            self.get_relationships.url.format(
                appId=self.app_id, id=configuration_item_id
            ),
            rclass=ConfigurationItemRelationship,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("DELETE", "/api/{appId}/cmdb/{id}/relationships/{relationshipId}")
    def remove_relationship(
        self, relationship_id: int, configuration_item_id: int
    ) -> None:
        """Removes a relationship from a configuration item."""
        self.dispatcher.send(
            self.remove_relationship.method,
            self.remove_relationship.url.format(
                appId=self.app_id,
                id=configuration_item_id,
                relationshipId=relationship_id,
            ),
        )

    @tdx_method(
        "PUT",
        "/api/{appId}/cmdb/{id}/relationships"
        "?typeId={typeId}&otherItemId={otherItemId}"
        "&isParent={isParent}&removeExisting={removeExisting}",
    )
    def add_relationship(
        self,
        relationship_type_id: int,
        parent_configuration_item_id: int,
        child_configuration_item_id: int,
        remove_existing: Optional[bool] = False,
    ) -> ConfigurationItemRelationship:
        return self.dispatcher.send(
            self.add_relationship.method,
            self.add_relationship.url.format(
                appId=self.app_id,
                id=parent_configuration_item_id,
                typeId=relationship_type_id,
                otherItemId=child_configuration_item_id,
                isParent=True,
                removeExisting=remove_existing,
            ),
            rclass=ConfigurationItemRelationship,
            rlist=False,
            rpartial=True,
        )

    @tdx_method("GET", "/api/{appId}/cmdb/{id}/tickets")
    def get_tickets(self, configuration_item_id: int) -> List[TicketListing]:
        """Gets the tickets related to a configuration item."""
        return self.dispatcher.send(
            self.get_tickets.method,
            self.get_tickets.url.format(appId=self.app_id, id=configuration_item_id),
            rclass=TicketListing,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("POST", "/api/{appId}/cmdb/{id}/attachments")
    def add_attachment(
        self,
        filepath: str,
        configuration_item_id: int,
        filename: Optional[str] = None,
        mimetype: Optional[str] = None,
    ) -> Attachment:
        """Uploads an attachment to a configuration item.

        The file should be included as part of the submission's form data.
        """
        return self.dispatcher.send(
            self.add_attachment.method,
            self.add_attachment.url.format(appId=self.app_id, id=configuration_item_id),
            file=filepath,
            filename=filename,
            mimetype=mimetype,
            rclass=Attachment,
            rlist=False,
            rpartial=True,
        )

    def new(self, **kwargs) -> ConfigurationItem:
        """Generate new ConfigurationItem object."""
        return helpers.new_model(ConfigurationItem, self, **kwargs)

    def save(
        self, configuration_item: ConfigurationItem, force: Optional[bool] = False
    ) -> None:
        """Create or update a ConfigurationItem."""
        helpers.save_model(configuration_item, self, force)

    @tdx_method("POST", "/api/{appId}/cmdb")
    def _create(self, configuration_item: ConfigurationItem) -> ConfigurationItem:
        """Creates a configuration item."""
        return self.dispatcher.send(
            self._create.method,
            self._create.url.format(appId=self.app_id),
            data=configuration_item,
            rclass=ConfigurationItem,
            rlist=False,
            rpartial=False,
        )

    @tdx_method("PUT", "/api/{appId}/cmdb/{id}")
    def _update(self, configuration_item: ConfigurationItem) -> ConfigurationItem:
        """Edits the specified configuration item."""
        return self.dispatcher.send(
            self._update.method,
            self._update.url.format(appId=self.app_id, id=configuration_item.id),
            data=configuration_item,
            rclass=ConfigurationItem,
            rlist=False,
            rpartial=False,
        )
