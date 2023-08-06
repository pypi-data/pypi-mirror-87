from typing import List

import attr

from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.managers.mixins import TdxAppMixin
from tdxapi.models.priority import Priority


@attr.s
class PriorityManager(TdxManager, TdxAppMixin):
    @tdx_method("GET", "/api/{appId}/tickets/priorities")
    def all(self) -> List[Priority]:
        """Gets all active ticket priorities."""
        return self.dispatcher.send(
            self.all.method,
            self.all.url.format(appId=self.app_id),
            rclass=Priority,
            rlist=True,
            rpartial=False,
        )
