from typing import List, Optional

import attr

from tdxapi.managers import helpers
from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.managers.mixins import TdxAppMixin
from tdxapi.models.product_type import ProductType
from tdxapi.models.product_type_search import ProductTypeSearch


@attr.s
class ProductTypeManager(TdxManager, TdxAppMixin):
    @tdx_method("GET", "/api/{appId}/assets/models/types/{id}")
    def get(self, product_type_id: int) -> ProductType:
        """Gets a product type."""
        return self.dispatcher.send(
            self.get.method,
            self.get.url.format(appId=self.app_id, id=product_type_id),
            rclass=ProductType,
            rlist=False,
            rpartial=False,
        )

    @tdx_method("GET", "/api/{appId}/assets/models/types")
    def all(self) -> List[ProductType]:
        """Gets a list of all product types."""
        return self.dispatcher.send(
            self.all.method,
            self.all.url.format(appId=self.app_id),
            rclass=ProductType,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("POST", "/api/{appId}/assets/models/types/search")
    def search(
        self,
        search_text: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_top_level: Optional[bool] = None,
        parent_product_type_id: Optional[int] = None,
    ) -> List[ProductType]:
        """Gets a list of product types.

        :param search_text: the search text to filter on. If this is set, this will sort
            the results by their text relevancy.
        :param is_active: the active status to filter on.
        :param is_top_level: a value indicating whether only top-level product types
            should be included.
        :param parent_product_type_id: the parent product type ID to filter on. If this
            is set, only direct children of this type will be included.
        """
        params = helpers.format_search_params(ProductTypeSearch, self, locals())

        return self.dispatcher.send(
            self.search.method,
            self.search.url.format(appId=self.app_id),
            data=params,
            rclass=ProductType,
            rlist=True,
            rpartial=True,
        )

    def new(self, **kwargs) -> ProductType:
        """Generate new ProductType object."""
        return helpers.new_model(ProductType, self, **kwargs)

    def save(
        self,
        product_type: ProductType,
        on_update_cascade_status: Optional[bool] = False,
        force: Optional[bool] = False,
    ) -> None:
        """Create or update a ProductType.

        cascade_status only applies to ProductType updates.
        """
        if not force:
            helpers.save_check(product_type)

        if product_type.id:
            updated_model = self._update(
                product_type, cascade_status=on_update_cascade_status
            )
        else:
            updated_model = self._create(product_type)

        helpers.update_model(product_type, updated_model)

    @tdx_method("POST", "/api/{appId}/assets/models/types")
    def _create(self, product_type: ProductType) -> ProductType:
        """Creates a new product type."""
        return self.dispatcher.send(
            self._create.method,
            self._create.url.format(appId=self.app_id),
            data=product_type,
            rclass=ProductType,
            rlist=False,
            rpartial=False,
        )

    @tdx_method(
        "PUT",
        "/api/{appId}/assets/models/types/{id}"
        "?cascadeActiveStatus={cascadeActiveStatus}",
    )
    def _update(
        self, product_type: ProductType, cascade_status: Optional[bool] = False
    ) -> ProductType:
        """Edits a product type."""
        return self.dispatcher.send(
            self._update.method,
            self._update.url.format(
                appId=self.app_id,
                id=product_type.id,
                cascadeActiveStatus=cascade_status,
            ),
            data=product_type,
            rclass=ProductType,
            rlist=False,
            rpartial=False,
        )
