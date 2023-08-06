from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class CustomEntityUnarchiveRequest:
    """The request body for unarchiving custom entities."""

    custom_entity_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        custom_entity_ids = self.custom_entity_ids

        properties: Dict[str, Any] = dict()

        properties["customEntityIds"] = custom_entity_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CustomEntityUnarchiveRequest":
        custom_entity_ids = d["customEntityIds"]

        return CustomEntityUnarchiveRequest(
            custom_entity_ids=custom_entity_ids,
        )
