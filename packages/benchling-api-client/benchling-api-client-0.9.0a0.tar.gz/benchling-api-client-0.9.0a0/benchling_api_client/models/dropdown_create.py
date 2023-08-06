from typing import Any, Dict, List, Optional, cast

import attr

from ..models.dropdown_create_option import DropdownCreateOption
from ..types import UNSET


@attr.s(auto_attribs=True)
class DropdownCreate:
    """  """

    name: str
    options: List[DropdownCreateOption]
    registry_id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        options = []
        for options_item_data in self.options:
            options_item = options_item_data.to_dict()

            options.append(options_item)

        registry_id = self.registry_id

        properties: Dict[str, Any] = dict()

        properties["name"] = name
        properties["options"] = options
        if registry_id is not UNSET:
            properties["registryId"] = registry_id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DropdownCreate":
        name = d["name"]

        options = []
        for options_item_data in d["options"]:
            options_item = DropdownCreateOption.from_dict(options_item_data)

            options.append(options_item)

        registry_id = d.get("registryId")

        return DropdownCreate(
            name=name,
            options=options,
            registry_id=registry_id,
        )
