from typing import List

import attr

from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.managers.mixins import TdxAppMixin
from tdxapi.models.impact import Impact


@attr.s
class ImpactManager(TdxManager, TdxAppMixin):
    @tdx_method("GET", "/api/{appId}/tickets/impacts")
    def all(self) -> List[Impact]:
        """Gets all active ticket impacts."""
        return self.dispatcher.send(
            self.all.method,
            self.all.url.format(appId=self.app_id),
            rclass=Impact,
            rlist=True,
            rpartial=False,
        )
