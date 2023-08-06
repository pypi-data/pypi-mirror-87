from typing import Any, Dict, List

import attr

from ..models.custom_entity_bulk_update_request import CustomEntityBulkUpdateRequest


@attr.s(auto_attribs=True)
class CustomEntityBulkUpdate:
    """  """

    custom_entities: List[CustomEntityBulkUpdateRequest]

    def to_dict(self) -> Dict[str, Any]:
        custom_entities = []
        for custom_entities_item_data in self.custom_entities:
            custom_entities_item = custom_entities_item_data.to_dict()

            custom_entities.append(custom_entities_item)

        properties: Dict[str, Any] = dict()

        properties["customEntities"] = custom_entities
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CustomEntityBulkUpdate":
        custom_entities = []
        for custom_entities_item_data in d["customEntities"]:
            custom_entities_item = CustomEntityBulkUpdateRequest.from_dict(custom_entities_item_data)

            custom_entities.append(custom_entities_item)

        return CustomEntityBulkUpdate(
            custom_entities=custom_entities,
        )
