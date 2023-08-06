from typing import List, Optional

import attr

from tdxapi.managers import helpers
from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.models.group import Group
from tdxapi.models.group_application import GroupApplication
from tdxapi.models.group_member import GroupMember
from tdxapi.models.group_search import GroupSearch


@attr.s
class GroupManager(TdxManager):
    @tdx_method("GET", "/api/groups/{id}")
    def get(self, group_id: int) -> Group:
        """Gets a group."""
        return self.dispatcher.send(
            self.get.method,
            self.get.url.format(id=group_id),
            rclass=Group,
            rlist=False,
            rpartial=False,
        )

    @tdx_method("POST", "/api/groups/search")
    def search(
        self,
        name_like: Optional[str] = None,
        is_active: Optional[bool] = None,
        associated_app_id: Optional[int] = None,
        available_in_app_id: Optional[int] = None,
        available_in_sys_app: Optional[str] = None,
    ):
        """Gets a list of groups.

        :param name_like: The search text to use for LIKE filtering on group name.
        :param is_active: The active status to filter on.
        :param associated_app_id: The associated platform application ID to filter on.
        :param available_in_app_id: The ID of the platform application the group is
            available in.
        :param available_in_sys_app: The system application name the group is available
            in.
        """
        params = helpers.format_search_params(GroupSearch, self, locals())

        return self.dispatcher.send(
            self.search.method,
            self.search.url,
            data=params,
            rclass=Group,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("GET", "/api/groups/{id}/applications")
    def get_apps(self, group_id: int) -> List[GroupApplication]:
        """Gets the applications associated with the specified group."""
        return self.dispatcher.send(
            self.get_apps.method,
            self.get_apps.url.format(id=group_id),
            rclass=GroupApplication,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("POST", "/api/groups/{id}/applications")
    def add_apps(self, app_ids: List[int], group_id: int) -> None:
        """Associates a collection of platform applications with a group."""
        self.dispatcher.send(
            self.add_apps.method,
            self.add_apps.url.format(id=group_id),
            data=app_ids,
        )

    @tdx_method("DELETE", "/api/groups/{id}/applications")
    def remove_apps(self, app_ids: List[int], group_id: int) -> None:
        """Unassociates a collection of platform applications from a group."""
        self.dispatcher.send(
            self.remove_apps.method,
            self.remove_apps.url.format(id=group_id),
            data=app_ids,
        )

    @tdx_method("GET", "/api/groups/{id}/members")
    def get_members(self, group_id: int) -> List[GroupMember]:
        """Gets the users belonging to a group."""
        return self.dispatcher.send(
            self.get_members.method,
            self.get_members.url.format(id=group_id),
            rclass=GroupMember,
            rlist=True,
            rpartial=True,
        )

    @tdx_method(
        "POST",
        "/api/groups/{id}/members"
        "?isPrimary={isPrimary}"
        "&isNotified={isNotified}"
        "&isManager={isManager}",
    )
    def add_members(
        self,
        uids: List[str],
        group_id: int,
        is_primary: Optional[bool] = False,
        is_notified: Optional[bool] = False,
        is_manager: Optional[bool] = False,
    ) -> None:
        """Adds a collection of users to a group.

        Users that did not exist in the group beforehand will have their settings
        set to the specified values. Existing users will not have their settings
        overwritten.
        """
        self.dispatcher.send(
            self.add_members.method,
            self.add_members.url.format(
                id=group_id,
                isPrimary=is_primary,
                isNotified=is_notified,
                isManager=is_manager,
            ),
            data=uids,
        )

    @tdx_method("DELETE", "/api/groups/{id}/members")
    def remove_members(self, uids: List[str], group_id: int) -> None:
        """Removes a collection of users from a group."""
        self.dispatcher.send(
            self.remove_members.method,
            self.remove_members.url.format(id=group_id),
            data=uids,
        )

    def new(self, **kwargs) -> Group:
        """Generate new Group object."""
        return helpers.new_model(Group, self, **kwargs)

    def save(self, group: Group, force: Optional[bool] = False) -> None:
        """Create or update a Group."""
        return helpers.save_model(group, self, force)

    @tdx_method("POST", "/api/groups")
    def _create(self, group: Group) -> Group:
        """Creates a new group."""
        return self.dispatcher.send(
            self._create.method,
            self._create.url,
            data=group,
            rclass=Group,
            rlist=False,
            rpartial=False,
        )

    @tdx_method("PUT", "/api/groups/{id}")
    def _update(self, group: Group) -> Group:
        """Edits an existing group."""
        return self.dispatcher.send(
            self._update.method,
            self._update.url.format(id=group.id),
            data=group,
            rclass=Group,
            rlist=False,
            rpartial=False,
        )
