from typing import Any, Dict, List

import attr

from ..models.custom_entity import CustomEntity


@attr.s(auto_attribs=True)
class CustomEntityList:
    """  """

    custom_entities: List[CustomEntity]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        custom_entities = []
        for custom_entities_item_data in self.custom_entities:
            custom_entities_item = custom_entities_item_data.to_dict()

            custom_entities.append(custom_entities_item)

        next_token = self.next_token

        properties: Dict[str, Any] = dict()

        properties["customEntities"] = custom_entities
        properties["nextToken"] = next_token
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CustomEntityList":
        custom_entities = []
        for custom_entities_item_data in d["customEntities"]:
            custom_entities_item = CustomEntity.from_dict(custom_entities_item_data)

            custom_entities.append(custom_entities_item)

        next_token = d["nextToken"]

        return CustomEntityList(
            custom_entities=custom_entities,
            next_token=next_token,
        )
