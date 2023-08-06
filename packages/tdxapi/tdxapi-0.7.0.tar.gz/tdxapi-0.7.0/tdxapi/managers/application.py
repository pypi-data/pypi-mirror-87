from typing import List

import attr

from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.models.application import Application


@attr.s
class ApplicationManager(TdxManager):
    def get(self, app_id: int) -> Application:
        """Gets an Application."""
        for app in self.all():
            if app.id == app_id:
                return app

    @tdx_method("GET", "/api/applications")
    def all(self) -> List[Application]:
        """Gets all the applications for an organization."""
        return self.dispatcher.send(
            self.all.method,
            self.all.url,
            rclass=Application,
            rlist=True,
            rpartial=True,
        )
