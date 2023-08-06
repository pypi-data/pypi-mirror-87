from typing import Any, Optional

import attr

from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.models.attachment import Attachment


@attr.s
class AttachmentManager(TdxManager):
    @tdx_method("GET", "/api/attachments/{id}")
    def get(
        self, attachment_id: str, with_content: Optional[bool] = False
    ) -> Attachment:
        """Gets an attachment."""
        attachment = self.dispatcher.send(
            self.get.method,
            self.get.url.format(id=attachment_id),
            rclass=Attachment,
            rlist=False,
            rpartial=False,
        )

        if attachment and with_content:
            attachment.content = self.get_content(attachment_id)

        return attachment

    @tdx_method("GET", "/api/attachments/{id}/content")
    def get_content(self, attachment_id: str) -> Any:
        """Gets the contents of an attachment."""
        return self.dispatcher.send(
            self.get_content.method, self.get_content.url.format(id=attachment_id)
        )

    @tdx_method("DELETE", "/api/attachments/{id}")
    def delete(self, attachment_id: str) -> None:
        """Deletes an attachment."""
        self.dispatcher.send(
            self.delete.method,
            self.delete.url.format(id=attachment_id),
        )
