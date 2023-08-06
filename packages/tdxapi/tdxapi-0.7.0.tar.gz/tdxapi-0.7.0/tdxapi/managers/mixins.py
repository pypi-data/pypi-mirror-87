import attr

from tdxapi.models.custom_attribute_list import CustomAttributeList


@attr.s
class TdxAppMixin(object):
    app_id = attr.ib()


@attr.s
class TdxCustomAttributeMixin(object):
    """Add custom attribute functions to manager object.

    Class being extended requires:
        - A class variable __tdx_component__
    """

    _attribute_template = attr.ib(default=None, repr=False)

    @property
    def attribute_template(self) -> CustomAttributeList:
        if self._attribute_template is None:
            from tdxapi.managers.custom_attribute import CustomAttributeManager

            cam = CustomAttributeManager(self.dispatcher)

            self._attribute_template = cam.get_by_component(
                self.__class__.__tdx_component__, app_id=getattr(self, "app_id", 0)
            )

        return self._attribute_template
