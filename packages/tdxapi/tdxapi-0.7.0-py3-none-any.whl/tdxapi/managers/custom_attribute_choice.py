from typing import List, Optional

import attr

from tdxapi.managers import helpers
from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.models.custom_attribute_choice import CustomAttributeChoice


@attr.s
class CustomAttributeChoiceManager(TdxManager):
    def get(self, attribute_choice_id: int, attribute_id: int) -> CustomAttributeChoice:
        """Gets a CustomAttributeChoice."""
        for attribute_choice in self.get_by_attribute(attribute_id):
            if attribute_choice.id == attribute_choice_id:
                return attribute_choice

    @tdx_method("GET", "/api/attributes/{id}/choices")
    def get_by_attribute(self, attribute_id: int) -> List[CustomAttributeChoice]:
        """Gets the choices for the specified custom attribute."""
        return self.dispatcher.send(
            self.get_by_attribute.method,
            self.get_by_attribute.url.format(id=attribute_id),
            rclass=CustomAttributeChoice,
            rlist=True,
            rpartial=True,
        )

    @tdx_method("DELETE", "/api/attributes/{id}/choices/{choiceId}")
    def delete(self, attribute_choice_id: int, attribute_id: int) -> None:
        """Removes the specified choice from the custom attribute."""
        self.dispatcher.send(
            self.delete.method,
            self.delete.url.format(id=attribute_id, choiceId=attribute_choice_id),
        )

    def new(self, **kwargs) -> CustomAttributeChoice:
        """Generate new CustomAttributeChoice object."""
        return helpers.new_model(CustomAttributeChoice, self, **kwargs)

    def save(
        self,
        attribute_choice: CustomAttributeChoice,
        attribute_id: int,
        force: Optional[bool] = False,
    ) -> None:
        """Create or update a CustomAttributeChoice."""
        if not force:
            helpers.save_check(attribute_choice)

        if attribute_choice.id:
            updated_model = self._update(attribute_choice, attribute_id)
        else:
            updated_model = self._create(attribute_choice, attribute_id)

        helpers.update_model(attribute_choice, updated_model)

    @tdx_method("POST", "/api/attributes/{id}/choices")
    def _create(
        self, attribute_choice: CustomAttributeChoice, attribute_id: int
    ) -> CustomAttributeChoice:
        """Adds a new choice to the specified custom attribute."""
        return self.dispatcher.send(
            self._create.method,
            self._create.url.format(id=attribute_id),
            data=attribute_choice,
            rclass=CustomAttributeChoice,
            rlist=False,
            rpartial=False,
        )

    @tdx_method("PUT", "/api/attributes/{id}/choices/{choiceId}")
    def _update(
        self, attribute_choice: CustomAttributeChoice, attribute_id: int
    ) -> CustomAttributeChoice:
        """Edits an existing choice associated with the specified custom attribute."""
        return self.dispatcher.send(
            self._update.method,
            self._update.url.format(id=attribute_id, choiceId=attribute_choice.id),
            data=attribute_choice,
            rclass=CustomAttributeChoice,
            rlist=False,
            rpartial=False,
        )
