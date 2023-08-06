from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class CreateIntoRegistry:
    """  """

    registry_id: Optional[str] = cast(None, UNSET)
    naming_strategy: Optional[str] = cast(None, UNSET)
    entity_registry_id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        registry_id = self.registry_id
        naming_strategy = self.naming_strategy
        entity_registry_id = self.entity_registry_id

        properties: Dict[str, Any] = dict()

        if registry_id is not UNSET:
            properties["registryId"] = registry_id
        if naming_strategy is not UNSET:
            properties["namingStrategy"] = naming_strategy
        if entity_registry_id is not UNSET:
            properties["entityRegistryId"] = entity_registry_id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CreateIntoRegistry":
        registry_id = d.get("registryId")

        naming_strategy = d.get("namingStrategy")

        entity_registry_id = d.get("entityRegistryId")

        return CreateIntoRegistry(
            registry_id=registry_id,
            naming_strategy=naming_strategy,
            entity_registry_id=entity_registry_id,
        )
