from typing import List, Optional

import attr

from tdxapi.managers import helpers
from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.models.resource_pool import ResourcePool
from tdxapi.models.resource_pool_search import ResourcePoolSearch


@attr.s
class ResourcePoolManager(TdxManager):
    def get(self, resource_pool_id: int) -> ResourcePool:
        """Gets a ResourcePool."""
        for resource_pool in self.search():
            if resource_pool.id == resource_pool_id:
                return resource_pool

    @tdx_method("POST", "/api/resourcepools/search")
    def search(
        self,
        name: Optional[str] = None,
        manager_uid: Optional[str] = None,
        is_active: Optional[bool] = None,
        return_item_counts: Optional[bool] = None,
        max_results: Optional[int] = None,
    ) -> List[ResourcePool]:
        """Gets a list of resource pools.

        :param name: the resource pool name to filter on.
        :param manager_uid: the UID of the resource pool manager to filter on.
        :param is_active: the active status to filter on.
        :param return_item_counts: a value indicating whether resource counts should
            be retrieved for each pool. Defaults to false.
        :param max_results: the maximum number of records to return.
        """
        params = helpers.format_search_params(ResourcePoolSearch, self, locals())

        return self.dispatcher.send(
            self.search.method,
            self.search.url,
            data=params,
            rclass=ResourcePool,
            rlist=True,
            rpartial=False,
        )

    def new(self, **kwargs) -> ResourcePool:
        """Generate new ResourcePool object."""
        return helpers.new_model(ResourcePool, self, **kwargs)

    def save(self, resource_pool: ResourcePool, force: Optional[bool] = False) -> None:
        """Create or update a ResourcePool."""
        helpers.save_model(resource_pool, self, force)

    @tdx_method("POST", "/api/resourcepools")
    def _create(self, resource_pool: ResourcePool) -> ResourcePool:
        """Creates a resource pool."""
        return self.dispatcher.send(
            self._create.method,
            self._create.url,
            data=resource_pool,
            rclass=ResourcePool,
            rlist=False,
            rpartial=False,
        )

    @tdx_method("PUT", "/api/resourcepools/{id}")
    def _update(self, resource_pool: ResourcePool) -> ResourcePool:
        """Edits the specified resource pool."""
        return self.dispatcher.send(
            self._update.method,
            self._update.url.format(id=resource_pool.id),
            data=resource_pool,
            rclass=ResourcePool,
            rlist=False,
            rpartial=False,
        )
