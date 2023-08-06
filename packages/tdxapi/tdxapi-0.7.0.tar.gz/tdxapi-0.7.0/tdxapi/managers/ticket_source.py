from typing import List

import attr

from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.managers.mixins import TdxAppMixin
from tdxapi.models.ticket_source import TicketSource


@attr.s
class TicketSourceManager(TdxManager, TdxAppMixin):
    @tdx_method("GET", "/api/{appId}/tickets/sources")
    def all(self) -> List[TicketSource]:
        """Gets all active ticket sources."""
        return self.dispatcher.send(
            self.all.method,
            self.all.url.format(appId=self.app_id),
            rclass=TicketSource,
            rlist=True,
            rpartial=False,
        )
