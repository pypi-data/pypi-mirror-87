from typing import Any, Dict, List, Optional, cast

import attr

from ..models.custom_entity import CustomEntity
from ..types import UNSET


@attr.s(auto_attribs=True)
class CustomEntities:
    """  """

    custom_entities: Optional[List[CustomEntity]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.custom_entities is None:
            custom_entities = None
        elif self.custom_entities is UNSET:
            custom_entities = UNSET
        else:
            custom_entities = []
            for custom_entities_item_data in self.custom_entities:
                custom_entities_item = custom_entities_item_data.to_dict()

                custom_entities.append(custom_entities_item)

        properties: Dict[str, Any] = dict()

        if custom_entities is not UNSET:
            properties["customEntities"] = custom_entities
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CustomEntities":
        custom_entities = []
        for custom_entities_item_data in d.get("customEntities") or []:
            custom_entities_item = CustomEntity.from_dict(custom_entities_item_data)

            custom_entities.append(custom_entities_item)

        return CustomEntities(
            custom_entities=custom_entities,
        )
