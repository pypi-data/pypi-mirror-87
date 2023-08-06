from typing import List

import attr

from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.managers.mixins import TdxAppMixin
from tdxapi.models.ticket_type import TicketType


@attr.s
class TicketTypeManager(TdxManager, TdxAppMixin):
    @tdx_method("GET", "/api/{appId}/tickets/types")
    def all(self) -> List[TicketType]:
        """Gets all active ticket types."""
        return self.dispatcher.send(
            self.all.method,
            self.all.url.format(appId=self.app_id),
            rclass=TicketType,
            rlist=True,
            rpartial=False,
        )
