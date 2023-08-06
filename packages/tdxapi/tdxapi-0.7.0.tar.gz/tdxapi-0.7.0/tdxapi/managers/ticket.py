from datetime import datetime
from typing import Any, List, Optional, Tuple

import attr

from tdxapi.enums.component import Component
from tdxapi.enums.sla_start_basis import SlaStartBasis
from tdxapi.enums.status_class import StatusClass
from tdxapi.enums.ticket_class import TicketClass
from tdxapi.enums.unmet_constraint_search_type import UnmetConstraintSearchType
from tdxapi.managers import helpers
from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.managers.mixins import TdxAppMixin, TdxCustomAttributeMixin
from tdxapi.models.attachment import Attachment
from tdxapi.models.configuration_item import ConfigurationItem
from tdxapi.models.item_update import ItemUpdate
from tdxapi.models.sla_assignment_options import SlaAssignmentOptions
from tdxapi.models.sla_removal_options import SlaRemovalOptions
from tdxapi.models.ticket import Ticket
from tdxapi.models.ticket_feed_entry import TicketFeedEntry
from tdxapi.models.ticket_search import TicketSearch
from tdxapi.models.user import User


@attr.s
class TicketManager(TdxManager, TdxAppMixin, TdxCustomAttributeMixin):
    __tdx_component__ = Component.TICKET

    @tdx_method("GET", "/api/{appId}/tickets/{id}")
    def get(self, ticket_id: int) -> Ticket:
        """Gets a ticket."""
        ticket = self.dispatcher.send(
            self.get.method,
            self.get.url.format(appId=self.app_id, id=ticket_id),
            rclass=Ticket,
            rlist=False,
            rpartial=False,
        )

        if ticket:
            ticket.attributes.match_template(self.attribute_template)

        return ticket

    @tdx_method("POST", "/api/{appId}/tickets/search")
    def search(
        self,
        ticket_classifications: Optional[List[TicketClass]] = None,
        max_results: Optional[int] = None,
        ticket_id: Optional[int] = None,
        parent_ticket_id: Optional[int] = None,
        search_text: Optional[str] = None,
        status_ids: Optional[List[int]] = None,
        past_status_ids: Optional[List[int]] = None,
        status_classes: Optional[List[StatusClass]] = None,
        priority_ids: Optional[List[int]] = None,
        urgency_ids: Optional[List[int]] = None,
        impact_ids: Optional[List[int]] = None,
        account_ids: Optional[List[int]] = None,
        type_ids: Optional[List[int]] = None,
        source_ids: Optional[List[int]] = None,
        updated_date_from: Optional[datetime] = None,
        updated_date_to: Optional[datetime] = None,
        updated_by_uid: Optional[str] = None,
        modified_date_from: Optional[datetime] = None,
        modified_date_to: Optional[datetime] = None,
        modified_by_uid: Optional[str] = None,
        start_date_from: Optional[datetime] = None,
        start_date_to: Optional[datetime] = None,
        end_date_from: Optional[datetime] = None,
        end_date_to: Optional[datetime] = None,
        responded_date_from: Optional[datetime] = None,
        responded_date_to: Optional[datetime] = None,
        responded_by_uid: Optional[str] = None,
        closed_date_from: Optional[datetime] = None,
        closed_date_to: Optional[datetime] = None,
        closed_by_uid: Optional[str] = None,
        respond_by_date_from: Optional[datetime] = None,
        respond_by_date_to: Optional[datetime] = None,
        close_by_date_from: Optional[datetime] = None,
        close_by_date_to: Optional[datetime] = None,
        created_date_from: Optional[datetime] = None,
        created_date_to: Optional[datetime] = None,
        created_by_uid: Optional[str] = None,
        days_old_from: Optional[int] = None,
        days_old_to: Optional[int] = None,
        responsibility_uids: Optional[List[str]] = None,
        responsibility_group_ids: Optional[List[int]] = None,
        responsibility_completed_task: Optional[bool] = None,
        primary_responsibility_uids: Optional[List[str]] = None,
        primary_responsibility_group_ids: Optional[List[int]] = None,
        sla_ids: Optional[List[int]] = None,
        sla_violated: Optional[bool] = None,
        sla_unmet_constraints: Optional[List[UnmetConstraintSearchType]] = None,
        article_ids: Optional[List[int]] = None,
        is_assigned: Optional[bool] = None,
        converted_to_task: Optional[bool] = None,
        reviewer_uid: Optional[str] = None,
        requestor_uids: Optional[List[str]] = None,
        requestor_name_like: Optional[str] = None,
        requestor_email_like: Optional[str] = None,
        requestor_phone_like: Optional[str] = None,
        configuration_item_ids: Optional[List[int]] = None,
        exclude_configuration_item_ids: Optional[List[int]] = None,
        is_on_hold: Optional[bool] = None,
        goes_off_hold_from: Optional[datetime] = None,
        goes_off_hold_to: Optional[datetime] = None,
        location_ids: Optional[List[int]] = None,
        location_room_ids: Optional[List[int]] = None,
        service_ids: Optional[List[int]] = None,
        custom_attributes: Optional[List[Tuple[int, Any]]] = None,
        has_reference_code: Optional[bool] = None,
    ) -> List[Ticket]:
        """Gets a list of tickets.

        :param ticket_classifications: The ticket classifications to filter on.
        :param max_results: The maximum number of results to return.
        :param ticket_id: The ticket ID to filter on.
        :param parent_ticket_id: The parent ticket ID to filter on.
        :param search_text: The search text to filter on.
        :param status_ids: The status IDs to filter on.
        :param past_status_ids: The historical status IDs to filter on.
        :param status_classes: The status class IDs to filter on.
        :param priority_ids: The priority IDs to filter on.
        :param urgency_ids: The urgency IDs to filter on.
        :param impact_ids: The impact IDs to filter on.
        :param account_ids: The account/department IDs to filter on.
        :param type_ids: The ticket type IDs to filter on.
        :param source_ids: The source IDs to filter on.
        :param updated_date_from: The minimum updated date to filter on.
        :param updated_date_to: The maximum updated date to filter on.
        :param updated_by_uid: The UID of the updating user to filter on.
        :param modified_date_from: The minimum last modified date to filter on.
        :param modified_date_to: The maximum last modified date to filter on.
        :param modified_by_uid: The UID of the last modifying user to filter on.
        :param start_date_from: The minimum start date to filter on.
        :param start_date_to: The maximum start date to filter on.
        :param end_date_from: The minimum end date to filter on.
        :param end_date_to: The maximum end date to filter on.
        :param responded_date_from: The minimum responded date to filter on.
        :param responded_date_to: The maximum responded date to filter on.
        :param responded_by_uid: The UID of the responding user to filter on.
        :param closed_date_from: The minimum closed date to filter on.
        :param closed_date_to: The maximum closed date to filter on.
        :param closed_by_uid: The UID of the closing person to filter on.
        :param respond_by_date_from: The minimum SLA "Respond By" deadline to filter on.
        :param respond_by_date_to: The maximum SLA "Respond By" deadline to filter on.
        :param close_by_date_from: The minimum SLA "Resolve By" deadline to filter on.
        :param close_by_date_to: The maximum SLA "Resolve By" deadline to filter on.
        :param created_date_from: The minimum created date to filter on.
        :param created_date_to: The maximum created date to filter on.
        :param created_by_uid: The UID of the creating user to filter on.
        :param days_old_from: The minimum age to filter on.
        :param days_old_to: The maximum age to filter on.
        :param responsibility_uids: The UIDs of the responsible users to filter on.
        :param responsibility_group_ids: The IDs of the responsible groups to filter on.
        :param responsibility_completed_task: The filter to use for responsibility_uids
            and responsibility_group_ids with regards to ticket tasks.
        :param primary_responsibility_uids: The UIDs of the primarily-responsible users
            to filter on.
        :param primary_responsibility_group_ids: The IDs of the primarily-responsible
            groups to filter on.
        :param sla_ids: The SLA IDs to filter on.
        :param sla_violated: The SLA violation status to filter on.
        :param sla_unmet_constraints: The unmet SLA deadlines to filter on.
        :param article_ids: The associated Knowledge Base article IDs to filter on.
        :param is_assigned: The assignment status to filter on.
        :param converted_to_task: The task conversion status to filter on.
        :param reviewer_uid: The UID of the reviewing user to filter on.
        :param requestor_uids: The requestor UIDs to filter on.
        :param requestor_name_like: The text to perform a LIKE search on the requestor's
            full name.
        :param requestor_email_like: The text to perform a LIKE search on the
            requestor's email address.
        :param requestor_phone_like: The text to perform a LIKE search on the
            requestor's phone number.
        :param configuration_item_ids: The IDs of the associated configuration items to
            filter on. To be included in the search results, a ticket must be associated
            with one or more of the listed CIs.
        :param exclude_configuration_item_ids: The IDs of the associated CIs to exclude
            on. To be included in the search results, a ticket must NOT be associated
            with any of the listed CIs.
        :param is_on_hold: The "On Hold" status to filter on.
        :param goes_off_hold_from: The minimum "Goes Off Hold" date to filter on.
        :param goes_off_hold_to: The maximum "Goes Off Hold" date to filter on.
        :param location_ids: The associated location IDs to filter on.
        :param location_room_ids: The associated location room IDs to filter on.
        :param service_ids: The associated service IDs to filter on.
        :param custom_attributes: The associated custom attributes to filter on.
        :param has_reference_code: Whether the returned tickets should have a reference
            code.
        """
        params = helpers.format_search_params(TicketSearch, self, locals())

        return self.dispatcher.send(
            self.search.method,
            self.search.url.format(appId=self.app_id),
            data=params,
            rclass=Ticket,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("GET", "/api/{appId}/tickets/{id}/assets")
    def get_configuration_items(self, ticket_id: int) -> List[ConfigurationItem]:
        """Gets the collection of configuration items associated with a ticket."""
        return self.dispatcher.send(
            self.get_configuration_items.method,
            self.get_configuration_items.url.format(appId=self.app_id, id=ticket_id),
            rclass=ConfigurationItem,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("DELETE", "/api/{appId}/tickets/{id}/assets/{assetId}")
    def remove_asset(self, asset_id: int, ticket_id: int) -> None:
        """Removes an asset from ticket."""
        self.dispatcher.send(
            self.remove_asset.method,
            self.remove_asset.url.format(
                appId=self.app_id, id=ticket_id, assetId=asset_id
            ),
        )

    @tdx_method("POST", "/api/{appId}/tickets/{id}/assets/{assetId}")
    def add_asset(self, asset_id: int, ticket_id: int) -> None:
        """Adds an asset to ticket."""
        self.dispatcher.send(
            self.add_asset.method,
            self.add_asset.url.format(
                appId=self.app_id, id=ticket_id, assetId=asset_id
            ),
        )

    @tdx_method("POST", "/api/{appId}/tickets/{id}/attachments")
    def add_attachment(
        self,
        filepath: str,
        ticket_id: int,
        filename: Optional[str] = None,
        mimetype: Optional[str] = None,
    ) -> Attachment:
        """Uploads an attachment to a ticket."""
        return self.dispatcher.send(
            self.add_attachment.method,
            self.add_attachment.url.format(appId=self.app_id, id=ticket_id),
            file=filepath,
            filename=filename,
            mimetype=mimetype,
            rclass=Attachment,
            rlist=False,
            rpartial=True,
        )

    @tdx_method("POST", "/api/{appId}/tickets/{id}/children")
    def add_children(self, ticket_ids: List[int], parent_ticket_id: int) -> None:
        """Adds the specified tickets as children to the specified parent ticket."""
        self.dispatcher.send(
            self.add_children.method,
            self.add_children.url.format(appId=self.app_id, id=parent_ticket_id),
            data=ticket_ids,
        )

    @tdx_method(
        "PUT",
        "/api/{appId}/tickets/{id}/classification"
        "?newClassificationId={newClassificationId}",
    )
    def change_classification(
        self, classification: TicketClass, ticket_id: int
    ) -> Ticket:
        """Changes a ticket's classification."""
        return self.dispatcher.send(
            self.change_classification.method,
            self.change_classification.url.format(
                appId=self.app_id,
                id=ticket_id,
                newClassificationId=classification.value,
            ),
            rclass=Ticket,
            rlist=False,
            rpartial=True,
        )

    @tdx_method("GET", "/api/{appId}/tickets/{id}/contacts")
    def get_contacts(self, ticket_id: int) -> List[User]:
        """Gets the ticket contacts."""
        return self.dispatcher.send(
            self.get_contacts.method,
            self.get_contacts.url.format(appId=self.app_id, id=ticket_id),
            rclass=User,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("DELETE", "/api/{appId}/tickets/{id}/contacts/{contactUid}")
    def remove_contact(self, contact_uid: str, ticket_id: int) -> None:
        """Removes a contact from ticket."""
        self.dispatcher.send(
            self.remove_contact.method,
            self.remove_contact.url.format(
                appId=self.app_id, id=ticket_id, contactUid=contact_uid
            ),
        )

    @tdx_method("POST", "/api/{appId}/tickets/{id}/contacts/{contactUid}")
    def add_contact(self, contact_uid: str, ticket_id: int) -> None:
        """Adds a contact to ticket."""
        self.dispatcher.send(
            self.add_contact.method,
            self.add_contact.url.format(
                appId=self.app_id, id=ticket_id, contactUid=contact_uid
            ),
        )

    @tdx_method("GET", "/api/{appId}/tickets/{id}/feed")
    def get_feed_entries(self, ticket_id: int) -> List[ItemUpdate]:
        """Gets the feed entries for a ticket."""
        return self.dispatcher.send(
            self.get_feed_entries.method,
            self.get_feed_entries.url.format(appId=self.app_id, id=ticket_id),
            rclass=ItemUpdate,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("POST", "/api/{appId}/tickets/{id}/feed")
    def add_feed_entry(
        self,
        comments: str,
        ticket_id: int,
        new_status_id: Optional[int] = None,
        is_private: Optional[bool] = True,
        notify: Optional[List[str]] = None,
    ) -> ItemUpdate:
        """Add a feed entry to ticket."""
        return self.dispatcher.send(
            self.add_feed_entry.method,
            self.add_feed_entry.url.format(appId=self.app_id, id=ticket_id),
            data=TicketFeedEntry(
                comments=comments,
                new_status_id=new_status_id,
                is_private=is_private,
                notify=helpers.build_notify_list(notify),
            ),
            rclass=ItemUpdate,
            rlist=False,
            rpartial=True,
        )

    def add_sla(
        self,
        new_sla_id: int,
        ticket_id: int,
        comments: Optional[str] = None,
        start_basis: Optional[SlaStartBasis] = SlaStartBasis.CURRENT_DATE_TIME,
        should_cascade: Optional[bool] = None,
        notify: Optional[List[str]] = None,
    ) -> Ticket:
        """Adds a service level agreement (SLA) to a ticket."""
        return self.change_sla(
            new_sla_id=new_sla_id,
            ticket_id=ticket_id,
            comments=comments,
            start_basis=start_basis,
            should_cascade=should_cascade,
            notify=notify,
        )

    @tdx_method("PUT", "/api/{appId}/tickets/{id}/sla")
    def change_sla(
        self,
        new_sla_id: int,
        ticket_id: int,
        comments: Optional[str] = None,
        start_basis: Optional[SlaStartBasis] = SlaStartBasis.CURRENT_DATE_TIME,
        should_cascade: Optional[bool] = None,
        notify: Optional[List[str]] = None,
    ) -> Ticket:
        """Sets or change the ticket's current service level agreement (SLA)."""
        return self.dispatcher.send(
            self.change_sla.method,
            self.change_sla.url.format(appId=self.app_id, id=ticket_id),
            data=SlaAssignmentOptions(
                new_sla_id=new_sla_id,
                comments=comments,
                start_basis=start_basis,
                should_cascade=should_cascade,
                notify=helpers.build_notify_list(notify),
            ),
            rclass=Ticket,
            rlist=False,
            rpartial=True,
        )

    @tdx_method("PUT", "/api/{appId}/tickets/{id}/sla/delete")
    def remove_sla(
        self,
        ticket_id: int,
        comments: Optional[str] = None,
        should_cascade: Optional[bool] = None,
        notify: Optional[List[str]] = None,
    ) -> Ticket:
        """Removes the ticket's current service level agreement (SLA)."""
        return self.dispatcher.send(
            self.remove_sla.method,
            self.remove_sla.url.format(appId=self.app_id, id=ticket_id),
            data=SlaRemovalOptions(
                comments=comments,
                should_cascade=should_cascade,
                notify=helpers.build_notify_list(notify),
            ),
            rclass=Ticket,
            rlist=False,
            rpartial=True,
        )

    def new(self, **kwargs) -> Ticket:
        """Generate new Ticket object."""
        return helpers.new_model(Ticket, self, **kwargs)

    def save(
        self,
        ticket: Ticket,
        on_create_notify_reviewer: Optional[bool] = False,
        on_create_notify_requestor: Optional[bool] = False,
        on_create_notify_responsible: Optional[bool] = False,
        on_create_allow_requestor_creation: Optional[bool] = False,
        on_update_notify_new_responsible: Optional[bool] = False,
        force: Optional[bool] = False,
    ) -> None:
        """Create or update a Ticket."""
        if not force:
            helpers.save_check(ticket)

        if ticket.id:
            updated_model = self._update(
                ticket, notify_new_responsible=on_update_notify_new_responsible
            )
        else:
            updated_model = self._create(
                ticket,
                notify_reviewer=on_create_notify_reviewer,
                notify_requestor=on_create_notify_requestor,
                notify_responsible=on_create_notify_responsible,
                allow_requestor_creation=on_create_allow_requestor_creation,
            )

        helpers.update_model(ticket, updated_model)

    @tdx_method(
        "POST",
        "/api/{appId}/tickets"
        "?EnableNotifyReviewer={EnableNotifyReviewer}"
        "&NotifyRequestor={NotifyRequestor}"
        "&NotifyResponsible={NotifyResponsible}"
        "&AllowRequestorCreation={AllowRequestorCreation}",
    )
    def _create(
        self,
        ticket: Ticket,
        notify_reviewer: Optional[bool] = False,
        notify_requestor: Optional[bool] = False,
        notify_responsible: Optional[bool] = False,
        allow_requestor_creation: Optional[bool] = False,
    ) -> Ticket:
        """Creates a Ticket"""
        return self.dispatcher.send(
            self._create.method,
            self._create.url.format(
                appId=self.app_id,
                EnableNotifyReviewer=notify_reviewer,
                NotifyRequestor=notify_requestor,
                NotifyResponsible=notify_responsible,
                AllowRequestorCreation=allow_requestor_creation,
            ),
            data=ticket,
            rclass=Ticket,
            rlist=False,
            rpartial=False,
        )

    @tdx_method(
        "POST", "/api/{appId}/tickets/{id}?notifyNewResponsible={notifyNewResponsible}"
    )
    def _update(
        self, ticket: Ticket, notify_new_responsible: Optional[bool] = False
    ) -> Ticket:
        """Edits an existing ticket."""
        return self.dispatcher.send(
            self._update.method,
            self._update.url.format(
                appId=self.app_id,
                id=ticket.id,
                notifyNewResponsible=notify_new_responsible,
            ),
            data=ticket,
            rclass=Ticket,
            rlist=False,
            rpartial=False,
        )
