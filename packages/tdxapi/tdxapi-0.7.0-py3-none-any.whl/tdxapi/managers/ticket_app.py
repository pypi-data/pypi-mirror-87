from datetime import datetime
from typing import List, Optional

import attr

from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.managers.impact import ImpactManager
from tdxapi.managers.mixins import TdxAppMixin
from tdxapi.managers.priority import PriorityManager
from tdxapi.managers.ticket import TicketManager
from tdxapi.managers.ticket_source import TicketSourceManager
from tdxapi.managers.ticket_status import TicketStatusManager
from tdxapi.managers.ticket_task import TicketTaskManager
from tdxapi.managers.ticket_type import TicketTypeManager
from tdxapi.managers.urgency import UrgencyManager
from tdxapi.models.eligible_assignment import EligibleAssignment
from tdxapi.models.form import Form
from tdxapi.models.item_updates_page import ItemUpdatesPage


@attr.s
class TicketApplication(TdxManager, TdxAppMixin):
    def __attrs_post_init__(self):
        self.impacts = ImpactManager(self.dispatcher, self.app_id)
        self.priorities = PriorityManager(self.dispatcher, self.app_id)
        self.sources = TicketSourceManager(self.dispatcher, self.app_id)
        self.statuses = TicketStatusManager(self.dispatcher, self.app_id)
        self.tasks = TicketTaskManager(self.dispatcher, self.app_id)
        self.tickets = TicketManager(self.dispatcher, self.app_id)
        self.types = TicketTypeManager(self.dispatcher, self.app_id)
        self.urgencies = UrgencyManager(self.dispatcher, self.app_id)

    @tdx_method(
        "GET",
        "/api/{appId}/tickets/feed"
        "?DateFrom={DateFrom}"
        "&DateTo={DateTo}"
        "&ReplyCount={ReplyCount}"
        "&ReturnCount={ReturnCount}",
    )
    def get_feed_page(
        self,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        reply_count: Optional[int] = None,
        return_count: Optional[int] = None,
    ) -> ItemUpdatesPage:
        """Gets the feed items for a ticket application matching the specified search.

        :param date_from: the maximum (latest) last-updated date to filter on. This is
            not inclusive of the date. .
        :param date_to: the minimum (earliest) last-updated date to filter on. This is
            not inclusive of the date.
        :param reply_count: the number of replies per feed entry. Must be in the range
            0-100, and will default to 3.
        :param return_count: the number of feed entries returned by the search. Must
            be in the range 1-100, and will default to 25.
        """
        return self.dispatcher.send(
            self.get_feed_page.method,
            self.get_feed_page.url.format(
                appId=self.app_id,
                DateFrom=date_from,
                DateTo=date_to,
                ReplyCount=reply_count,
                ReturnCount=return_count,
            ),
            rclass=ItemUpdatesPage,
            rlist=False,
            rpartial=True,
        )

    @tdx_method("GET", "/api/{appId}/tickets/forms")
    def get_ticket_forms(self) -> List[Form]:
        """Gets all active ticket forms for the specified application."""
        return self.dispatcher.send(
            self.get_ticket_forms.method,
            self.get_ticket_forms.url.format(appId=self.app_id),
            rclass=Form,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("GET", "/api/{appId}/tickets/resources?searchText={searchText}")
    def get_eligible_assignments(self, search_text: str) -> List[EligibleAssignment]:
        """Gets a list of eligible assignments for the ticketing application."""
        return self.dispatcher.send(
            self.get_eligible_assignments.method,
            self.get_eligible_assignments.url.format(
                appId=self.app_id, searchText=search_text
            ),
            rclass=EligibleAssignment,
            rlist=True,
            rpartial=True,
        )
