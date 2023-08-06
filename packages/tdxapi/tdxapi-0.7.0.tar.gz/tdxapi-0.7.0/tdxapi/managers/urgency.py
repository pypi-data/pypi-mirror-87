from typing import List

import attr

from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.managers.mixins import TdxAppMixin
from tdxapi.models.urgency import Urgency


@attr.s
class UrgencyManager(TdxManager, TdxAppMixin):
    @tdx_method("GET", "/api/{appId}/tickets/urgencies")
    def all(self) -> List[Urgency]:
        """Gets all active ticket urgencies."""
        return self.dispatcher.send(
            self.all.method,
            self.all.url.format(appId=self.app_id),
            rclass=Urgency,
            rlist=True,
            rpartial=False,
        )
