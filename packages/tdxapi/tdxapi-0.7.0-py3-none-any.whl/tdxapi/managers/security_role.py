from typing import List, Optional

import attr

from tdxapi.enums.license_type import LicenseType
from tdxapi.managers import helpers
from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.models.permission import Permission
from tdxapi.models.security_role import SecurityRole
from tdxapi.models.security_role_search import SecurityRoleSearch


@attr.s
class SecurityRoleManager(TdxManager):
    @tdx_method("GET", "/api/securityroles/{id}")
    def get(self, security_role_id: str) -> SecurityRole:
        """Gets a security role."""
        return self.dispatcher.send(
            self.get.method,
            self.get.url.format(id=security_role_id),
            rclass=SecurityRole,
            rlist=False,
            rpartial=False,
        )

    @tdx_method(
        "GET",
        "/api/securityroles/permissions"
        "?forAppId={forAppId}"
        "&forLicenseType={forLicenseType}"
        "&onlyDefault={onlyDefault}",
    )
    def get_permissions(
        self,
        app_id: Optional[int] = 0,
        license_type: Optional[LicenseType] = None,
        only_default: Optional[bool] = False,
    ) -> List[Permission]:
        """Gets a list of available permissions for the specified application and
        optionally for the specified license type.
        """
        if license_type:
            license_type = license_type.value

        return self.dispatcher.send(
            self.get_permissions.method,
            self.get_permissions.url.format(
                forAppId=app_id, forLicenseType=license_type, onlyDefault=only_default
            ),
            rclass=Permission,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("POST", "/api/securityroles/search")
    def search(
        self,
        name_like: Optional[str] = None,
        app_id: Optional[int] = None,
        license_type: Optional[LicenseType] = None,
    ) -> List[SecurityRole]:
        """Gets a list of security roles.

        :param name_like: the security role name.
        :param app_id: the application ID. Providing a non-zero value will search for
            application-specific security roles, while a value of 0 will search for
            global security roles.
        :param license_type: the license type.
        """
        params = helpers.format_search_params(SecurityRoleSearch, self, locals())

        return self.dispatcher.send(
            self.search.method,
            self.search.url,
            data=params,
            rclass=SecurityRole,
            rlist=True,
            rpartial=True,
        )

    def new(self, **kwargs) -> SecurityRole:
        """Generate new SecurityRole object."""
        return helpers.new_model(SecurityRole, self, **kwargs)

    def save(
        self,
        security_role: SecurityRole,
        force: Optional[bool] = False,
        default_permissions: Optional[bool] = False,
    ) -> None:
        """Create or update a SecurityRole."""
        helpers.save_model(
            security_role, self, force, default_permissions=default_permissions
        )

    @tdx_method(
        "POST", "/api/securityroles?useDefaultPermissions={useDefaultPermissions}"
    )
    def _create(
        self, security_role: SecurityRole, default_permissions: Optional[bool] = False
    ) -> SecurityRole:
        """Creates a security role."""
        return self.dispatcher.send(
            self._create.method,
            self._create.url.format(useDefaultPermissions=default_permissions),
            data=security_role,
            rclass=SecurityRole,
            rlist=False,
            rpartial=False,
        )

    @tdx_method(
        "PUT",
        "/api/securityroles/{id}?useDefaultPermissions={useDefaultPermissions}",
    )
    def _update(
        self, security_role: SecurityRole, default_permissions: Optional[bool] = False
    ) -> SecurityRole:
        """Edits the specified security role."""
        return self.dispatcher.send(
            self._update.method,
            self._update.url.format(
                id=security_role.id, useDefaultPermissions=default_permissions
            ),
            data=security_role,
            rclass=SecurityRole,
            rlist=False,
            rpartial=False,
        )
