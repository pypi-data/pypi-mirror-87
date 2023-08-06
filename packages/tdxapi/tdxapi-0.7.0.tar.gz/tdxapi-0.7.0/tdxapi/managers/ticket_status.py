from typing import List, Optional

import attr

from tdxapi.enums.status_class import StatusClass
from tdxapi.managers import helpers
from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.managers.mixins import TdxAppMixin
from tdxapi.models.ticket_status import TicketStatus
from tdxapi.models.ticket_status_search import TicketStatusSearch


@attr.s
class TicketStatusManager(TdxManager, TdxAppMixin):
    @tdx_method("GET", "/api/{appId}/tickets/statuses/{id}")
    def get(self, ticket_status_id: int) -> TicketStatus:
        """Gets a ticket status."""
        return self.dispatcher.send(
            self.get.method,
            self.get.url.format(appId=self.app_id, id=ticket_status_id),
            rclass=TicketStatus,
            rlist=False,
            rpartial=False,
        )

    @tdx_method("GET", "/api/{appId}/tickets/statuses")
    def all(self) -> List[TicketStatus]:
        """Gets all active ticket statuses."""
        return self.dispatcher.send(
            self.all.method,
            self.all.url.format(appId=self.app_id),
            rclass=TicketStatus,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("POST", "/api/{appId}/tickets/statuses/search")
    def search(
        self,
        search_text: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_default: Optional[bool] = None,
        status_class: Optional[StatusClass] = None,
        requires_goes_off_hold: Optional[bool] = None,
    ) -> List[TicketStatus]:
        """Gets a list of ticket statuses.

        :param search_text: the search text to filter on. When set, results will be
            ordered by their text relevancy.
        :param is_active: the active status to filter on.
        :param is_default: the default status to filter on.
        :param status_class: the status class to filter on.
        :param requires_goes_off_hold: the "Requires Goes Off Hold" status to filter on.
        """
        params = helpers.format_search_params(TicketStatusSearch, self, locals())

        return self.dispatcher.send(
            self.search.method,
            self.search.url.format(appId=self.app_id),
            data=params,
            rclass=TicketStatus,
            rlist=True,
            rpartial=True,
        )

    def new(self, **kwargs) -> TicketStatus:
        """Generate new TicketStatus object."""
        return helpers.new_model(TicketStatus, self, **kwargs)

    def save(self, ticket_status: TicketStatus, force: Optional[bool] = False) -> None:
        """Create or update an TicketStatus."""
        helpers.save_model(ticket_status, self, force)

    @tdx_method("POST", "/api/{appId}/tickets/statuses")
    def _create(self, ticket_status: TicketStatus) -> TicketStatus:
        """Creates a ticket status."""
        return self.dispatcher.send(
            self._create.method,
            self._create.url.format(appId=self.app_id),
            data=ticket_status,
            rclass=TicketStatus,
            rlist=False,
            rpartial=False,
        )

    @tdx_method("PUT", "/api/{appId}/tickets/statuses/{id}")
    def _update(self, ticket_status: TicketStatus) -> TicketStatus:
        """Edits an existing ticket status."""
        return self.dispatcher.send(
            self._update.method,
            self._update.url.format(appId=self.app_id, id=ticket_status.id),
            data=ticket_status,
            rclass=TicketStatus,
            rlist=False,
            rpartial=False,
        )
