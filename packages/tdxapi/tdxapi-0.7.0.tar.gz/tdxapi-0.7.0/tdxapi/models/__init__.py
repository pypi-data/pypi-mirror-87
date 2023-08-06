# flake8: noqa
import json
from datetime import datetime
from enum import Enum

import attr
from dateutil import tz

from tdxapi.models.account import Account
from tdxapi.models.account_search import AccountSearch
from tdxapi.models.application import Application
from tdxapi.models.asset import Asset
from tdxapi.models.asset_search import AssetSearch
from tdxapi.models.asset_status import AssetStatus
from tdxapi.models.asset_status_search import AssetStatusSearch
from tdxapi.models.attachment import Attachment
from tdxapi.models.bases import TdxModel
from tdxapi.models.chart_setting import ChartSetting
from tdxapi.models.configuration_item import ConfigurationItem
from tdxapi.models.configuration_item_relationship import ConfigurationItemRelationship
from tdxapi.models.configuration_item_search import ConfigurationItemSearch
from tdxapi.models.configuration_item_type import ConfigurationItemType
from tdxapi.models.configuration_item_type_search import ConfigurationItemTypeSearch
from tdxapi.models.configuration_relationship_type import ConfigurationRelationshipType
from tdxapi.models.configuration_relationship_type_search import (
    ConfigurationRelationshipTypeSearch,
)
from tdxapi.models.contact_information import ContactInformation
from tdxapi.models.custom_attribute import CustomAttribute
from tdxapi.models.custom_attribute_choice import CustomAttributeChoice
from tdxapi.models.custom_attribute_list import CustomAttributeList
from tdxapi.models.display_column import DisplayColumn
from tdxapi.models.eligible_assignment import EligibleAssignment
from tdxapi.models.feed_entry import FeedEntry
from tdxapi.models.form import Form
from tdxapi.models.functional_role import FunctionalRole
from tdxapi.models.functional_role_search import FunctionalRoleSearch
from tdxapi.models.group import Group
from tdxapi.models.group_application import GroupApplication
from tdxapi.models.group_member import GroupMember
from tdxapi.models.impact import Impact
from tdxapi.models.item_update import ItemUpdate
from tdxapi.models.item_update_like import ItemUpdateLike
from tdxapi.models.item_update_reply import ItemUpdateReply
from tdxapi.models.item_updates_page import ItemUpdatesPage
from tdxapi.models.order_by_column import OrderByColumn
from tdxapi.models.participant import Participant
from tdxapi.models.permission import Permission
from tdxapi.models.priority import Priority
from tdxapi.models.product_model import ProductModel
from tdxapi.models.product_model_search import ProductModelSearch
from tdxapi.models.product_type import ProductType
from tdxapi.models.product_type_search import ProductTypeSearch
from tdxapi.models.report import Report
from tdxapi.models.report_info import ReportInfo
from tdxapi.models.report_search import ReportSearch
from tdxapi.models.resource_item import ResourceItem
from tdxapi.models.resource_pool import ResourcePool
from tdxapi.models.resource_pool_search import ResourcePoolSearch
from tdxapi.models.security_role import SecurityRole
from tdxapi.models.security_role_search import SecurityRoleSearch
from tdxapi.models.sla_assignment_options import SlaAssignmentOptions
from tdxapi.models.sla_removal_options import SlaRemovalOptions
from tdxapi.models.ticket import Ticket
from tdxapi.models.ticket_feed_entry import TicketFeedEntry
from tdxapi.models.ticket_listing import TicketListing
from tdxapi.models.ticket_search import TicketSearch
from tdxapi.models.ticket_source import TicketSource
from tdxapi.models.ticket_status import TicketStatus
from tdxapi.models.ticket_status_search import TicketStatusSearch
from tdxapi.models.ticket_task import TicketTask
from tdxapi.models.ticket_task_feed_entry import TicketTaskFeedEntry
from tdxapi.models.ticket_type import TicketType
from tdxapi.models.urgency import Urgency
from tdxapi.models.user import User
from tdxapi.models.user_application import UserApplication
from tdxapi.models.vendor import Vendor
from tdxapi.models.vendor_search import VendorSearch


class TdxModelEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, TdxModel):
            data = {}

            # Special formatting for CustomAttribute values
            if isinstance(o, CustomAttribute) and isinstance(o.value, (list, tuple)):
                # Convert list of ids to the api format i.e. [123, 456] -> "123,456"
                o.value = ",".join(str(v) for v in o.value)

            for field in [f for f in attr.fields(o.__class__) if f.repr]:
                value = getattr(o, field.name)
                data[field.metadata["tdx_name"]] = value

            return data

        elif isinstance(o, datetime):
            # If datetime object is timezone unaware convert to local timezone
            if o.tzinfo is None:
                o = o.replace(tzinfo=tz.tzlocal())

            return o.isoformat()

        elif isinstance(o, Enum):
            return o.value

        return json.JSONEncoder.default(self, o)
