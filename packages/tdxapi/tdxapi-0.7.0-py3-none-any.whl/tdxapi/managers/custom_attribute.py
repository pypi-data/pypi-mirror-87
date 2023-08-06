from typing import Optional

import attr

from tdxapi.enums.component import Component
from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.models.custom_attribute import CustomAttribute
from tdxapi.models.custom_attribute_list import CustomAttributeList


@attr.s
class CustomAttributeManager(TdxManager):
    @tdx_method(
        "GET",
        "/api/attributes/custom"
        "?componentId={componentId}&associatedTypeId={associatedTypeId}&appId={appId}",
    )
    def get_by_component(
        self,
        component: Component,
        app_id: Optional[int] = 0,
        associated_type_id: Optional[int] = 0,
    ) -> CustomAttributeList:
        """Gets the custom attributes for the specified component."""
        return CustomAttributeList(
            self.dispatcher.send(
                self.get_by_component.method,
                self.get_by_component.url.format(
                    componentId=component.value,
                    associatedTypeId=associated_type_id,
                    appId=app_id,
                ),
                rclass=CustomAttribute,
                rlist=True,
                rpartial=True,
            )
        )
