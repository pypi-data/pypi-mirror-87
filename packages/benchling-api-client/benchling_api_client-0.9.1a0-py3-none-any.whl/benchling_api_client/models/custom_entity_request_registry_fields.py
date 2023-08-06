from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class CustomEntityRequestRegistryFields:
    """  """

    entity_registry_id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        entity_registry_id = self.entity_registry_id

        properties: Dict[str, Any] = dict()

        if entity_registry_id is not UNSET:
            properties["entityRegistryId"] = entity_registry_id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CustomEntityRequestRegistryFields":
        entity_registry_id = d.get("entityRegistryId")

        return CustomEntityRequestRegistryFields(
            entity_registry_id=entity_registry_id,
        )
