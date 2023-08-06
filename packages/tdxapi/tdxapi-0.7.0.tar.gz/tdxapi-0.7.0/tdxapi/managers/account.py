from typing import Any, List, Optional, Tuple

import attr

from tdxapi.enums.component import Component
from tdxapi.managers import helpers
from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.managers.mixins import TdxCustomAttributeMixin
from tdxapi.models.account import Account
from tdxapi.models.account_search import AccountSearch


@attr.s
class AccountManager(TdxManager, TdxCustomAttributeMixin):
    __tdx_component__ = Component.ACCOUNT

    @tdx_method("GET", "/api/accounts/{id}")
    def get(self, account_id: int) -> Account:
        """Gets an account."""
        account = self.dispatcher.send(
            self.get.method,
            self.get.url.format(id=account_id),
            rclass=Account,
            rlist=False,
            rpartial=False,
        )

        if account:
            account.attributes.match_template(self.attribute_template)

        return account

    @tdx_method("GET", "/api/accounts")
    def all(self) -> List[Account]:
        """Gets a list of all active accounts/departments."""
        return self.dispatcher.send(
            self.all.method,
            self.all.url,
            rclass=Account,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("POST", "/api/accounts/search")
    def search(
        self,
        search_text: Optional[str] = None,
        manager_uids: Optional[List[str]] = None,
        custom_attributes: Optional[List[Tuple[int, Any]]] = None,
        is_active: Optional[bool] = None,
        max_results: Optional[int] = None,
        parent_account_id: Optional[int] = None,
        parent_account_name: Optional[str] = None,
    ) -> List[Account]:
        """Gets a list of all accounts/departments.

        :param search_text: the search text to use.
        :param manager_uids: the UIDs of the department managers to filter on.
        :param custom_attributes: the custom attributes to filter on.
        :param is_active: the active status to filter on.
        :param max_results: the maximum number of records to return.
        :param parent_account_id: the ID of the parent account to filter on.
        :param parent_account_name: the name of the parent account to filter on.
        """
        params = helpers.format_search_params(AccountSearch, self, locals())

        return self.dispatcher.send(
            self.search.method,
            self.search.url,
            data=params,
            rclass=Account,
            rlist=True,
            rpartial=True,
        )

    def new(self, **kwargs) -> Account:
        """Generate new Account object."""
        return helpers.new_model(Account, self, **kwargs)

    def save(self, account: Account, force: Optional[bool] = False) -> None:
        """Create or update an Account."""
        helpers.save_model(account, self, force)

    @tdx_method("POST", "/api/accounts")
    def _create(self, account: Account) -> Account:
        """Creates a new account."""
        return self.dispatcher.send(
            self._create.method,
            self._create.url,
            data=account,
            rclass=Account,
            rlist=False,
            rpartial=False,
        )

    @tdx_method("PUT", "/api/accounts/{id}")
    def _update(self, account: Account) -> Account:
        """Edits the account specified by the account ID."""
        return self.dispatcher.send(
            self._update.method,
            self._update.url.format(id=account.id),
            data=account,
            rclass=Account,
            rlist=False,
            rpartial=False,
        )
