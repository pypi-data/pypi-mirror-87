from typing import List, Optional

import attr

from tdxapi.managers import helpers
from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.managers.mixins import TdxAppMixin
from tdxapi.models.configuration_item_type import ConfigurationItemType
from tdxapi.models.configuration_item_type_search import ConfigurationItemTypeSearch


@attr.s
class ConfigurationItemTypeManager(TdxManager, TdxAppMixin):
    @tdx_method("GET", "/api/{appId}/cmdb/types/{id}")
    def get(self, configuration_item_type_id: int) -> ConfigurationItemType:
        """Gets a configuration item type."""
        return self.dispatcher.send(
            self.get.method,
            self.get.url.format(appId=self.app_id, id=configuration_item_type_id),
            rclass=ConfigurationItemType,
            rlist=False,
            rpartial=False,
        )

    @tdx_method("GET", "/api/{appId}/cmdb/types")
    def all(self) -> List[ConfigurationItemType]:
        """Gets a list of all active configuration item types.

        This will include system-defined configuration item types.
        """
        return self.dispatcher.send(
            self.all.method,
            self.all.url.format(appId=self.app_id),
            rclass=ConfigurationItemType,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("POST", "/api/{appId}/cmdb/types/search")
    def search(
        self,
        search_text: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_system_defined: Optional[bool] = None,
    ) -> List[ConfigurationItemType]:
        """Gets a list of configuration item types.

        :param search_text: the search text to filter on. If this is set, this will
            sort the results by their text relevancy.
        :param is_active: the active status to filter on.
        :param is_system_defined: a value indicating whether or not
            system-defined types will be returned.
        """
        params = helpers.format_search_params(
            ConfigurationItemTypeSearch, self, locals()
        )

        # search parameter name was reversed to match up with attribute name
        if params.is_system_defined is not None:
            params.is_system_defined = not params.is_system_defined

        return self.dispatcher.send(
            self.search.method,
            self.search.url.format(appId=self.app_id),
            data=params,
            rclass=ConfigurationItemType,
            rlist=True,
            rpartial=True,
        )

    def new(self, **kwargs) -> ConfigurationItemType:
        """Generate new ConfigurationItemType object."""
        return helpers.new_model(ConfigurationItemType, self, **kwargs)

    def save(
        self,
        configuration_item_type: ConfigurationItemType,
        force: Optional[bool] = False,
    ) -> None:
        """Create or update a ConfigurationItemType."""
        helpers.save_model(configuration_item_type, self, force)

    @tdx_method("POST", "/api/{appId}/cmdb/types")
    def _create(
        self, configuration_item_type: ConfigurationItemType
    ) -> ConfigurationItemType:
        """Creates a configuration item type."""
        return self.dispatcher.send(
            self._create.method,
            self._create.url.format(appId=self.app_id),
            data=configuration_item_type,
            rclass=ConfigurationItemType,
            rlist=False,
            rpartial=False,
        )

    @tdx_method("PUT", "/api/{appId}/cmdb/types/{id}")
    def _update(
        self, configuration_item_type: ConfigurationItemType
    ) -> ConfigurationItemType:
        """Edits an existing configuration item type."""
        return self.dispatcher.send(
            self._update.method,
            self._update.url.format(appId=self.app_id, id=configuration_item_type.id),
            data=configuration_item_type,
            rclass=ConfigurationItemType,
            rlist=False,
            rpartial=False,
        )
