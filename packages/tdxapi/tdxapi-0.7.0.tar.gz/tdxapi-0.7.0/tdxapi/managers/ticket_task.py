from typing import List, Optional

import attr

from tdxapi.managers import helpers
from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.managers.mixins import TdxAppMixin
from tdxapi.models.item_update import ItemUpdate
from tdxapi.models.ticket_task import TicketTask
from tdxapi.models.ticket_task_feed_entry import TicketTaskFeedEntry


@attr.s
class TicketTaskManager(TdxManager, TdxAppMixin):
    @tdx_method("GET", "/api/{appId}/tickets/{ticketId}/tasks/{id}")
    def get(self, ticket_task_id: int, ticket_id: int) -> TicketTask:
        """Gets an individual ticket task on a ticket."""
        return self.dispatcher.send(
            self.get.method,
            self.get.url.format(
                appId=self.app_id, ticketId=ticket_id, id=ticket_task_id
            ),
            rclass=TicketTask,
            rlist=False,
            rpartial=False,
        )

    @tdx_method(
        "GET",
        "/api/{appId}/tickets/{ticketId}/tasks"
        "?isEligiblePredecessor={isEligiblePredecessor}",
    )
    def get_by_ticket(
        self, ticket_id: int, is_eligible_predecessor: Optional[bool] = None
    ) -> List[TicketTask]:
        """Gets a list of tasks currently on a ticket."""
        return self.dispatcher.send(
            self.get_by_ticket.method,
            self.get_by_ticket.url.format(
                appId=self.app_id,
                ticketId=ticket_id,
                isEligiblePredecessor=is_eligible_predecessor,
            ),
            rclass=TicketTask,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("POST", "/api/{appId}/tickets/{ticketId}/tasks/{id}/feed")
    def add_feed_entry(
        self,
        ticket_task_id: int,
        ticket_id: int,
        comments: Optional[str] = None,
        percent_complete: Optional[int] = None,
        is_private: Optional[bool] = True,
        notify: Optional[List[str]] = None,
    ) -> ItemUpdate:
        """Add feed entry to ticket task."""
        if comments is None and percent_complete is None:
            raise ValueError("comments or percent_complete is required")

        return self.dispatcher.send(
            self.add_feed_entry.method,
            self.add_feed_entry.url.format(
                appId=self.app_id, ticketId=ticket_id, id=ticket_task_id
            ),
            data=TicketTaskFeedEntry(
                comments=comments,
                percent_complete=percent_complete,
                is_private=is_private,
                notify=helpers.build_notify_list(notify),
            ),
            rclass=ItemUpdate,
            rlist=False,
            rpartial=True,
        )

    @tdx_method("GET", "/api/{appId}/tickets/{ticketId}/tasks/{id}/feed")
    def get_feed_entries(self, ticket_task_id: int, ticket_id: int) -> List[ItemUpdate]:
        """Gets the feed entries for the ticket task."""
        return self.dispatcher.send(
            self.get_feed_entries.method,
            self.get_feed_entries.url.format(
                appId=self.app_id, ticketId=ticket_id, id=ticket_task_id
            ),
            rclass=ItemUpdate,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("DELETE", "/api/{appId}/tickets/{ticketId}/tasks/{id}")
    def delete(self, ticket_task_id: int, ticket_id: int) -> None:
        """Removes a ticket task from a ticket."""
        self.dispatcher.send(
            self.delete.method,
            self.delete.url.format(
                appId=self.app_id, ticketId=ticket_id, id=ticket_task_id
            ),
        )

    def new(self, **kwargs) -> TicketTask:
        """Generate new TicketTask object."""
        return helpers.new_model(TicketTask, self, **kwargs)

    def save(self, ticket_task: TicketTask, force: Optional[bool] = False) -> None:
        """Create or update a TicketTask."""

        if not ticket_task.ticket_id:
            raise ValueError("ticket_id is required")

        helpers.save_model(ticket_task, self, force)

    @tdx_method("POST", "/api/{appId}/tickets/{ticketId}/tasks")
    def _create(self, ticket_task: TicketTask) -> TicketTask:
        """Creates a new ticket task on a ticket."""
        return self.dispatcher.send(
            self._create.method,
            self._create.url.format(appId=self.app_id, ticketId=ticket_task.ticket_id),
            data=ticket_task,
            rclass=TicketTask,
            rlist=False,
            rpartial=False,
        )

    @tdx_method("PUT", "/api/{appId}/tickets/{ticketId}/tasks/{id}")
    def _update(self, ticket_task: TicketTask):
        """Updates a ticket task with a set of new values."""
        return self.dispatcher.send(
            self._update.method,
            self._update.url.format(
                appId=self.app_id, ticketId=ticket_task.ticket_id, id=ticket_task.id
            ),
            data=ticket_task,
            rclass=TicketTask,
            rlist=False,
            rpartial=False,
        )
