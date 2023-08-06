from typing import Any, Dict, List

import attr

from ..models.custom_entity_bulk_create_request import CustomEntityBulkCreateRequest


@attr.s(auto_attribs=True)
class CustomEntityBulkCreate:
    """  """

    custom_entities: List[CustomEntityBulkCreateRequest]

    def to_dict(self) -> Dict[str, Any]:
        custom_entities = []
        for custom_entities_item_data in self.custom_entities:
            custom_entities_item = custom_entities_item_data.to_dict()

            custom_entities.append(custom_entities_item)

        properties: Dict[str, Any] = dict()

        properties["customEntities"] = custom_entities
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CustomEntityBulkCreate":
        custom_entities = []
        for custom_entities_item_data in d["customEntities"]:
            custom_entities_item = CustomEntityBulkCreateRequest.from_dict(custom_entities_item_data)

            custom_entities.append(custom_entities_item)

        return CustomEntityBulkCreate(
            custom_entities=custom_entities,
        )
