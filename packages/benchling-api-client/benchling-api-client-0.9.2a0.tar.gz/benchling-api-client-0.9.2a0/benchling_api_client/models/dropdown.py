from typing import Any, Dict, List, Optional, cast

import attr

from ..models.dropdown_option import DropdownOption
from ..types import UNSET


@attr.s(auto_attribs=True)
class Dropdown:
    """  """

    name: str
    id: str
    options: Optional[List[DropdownOption]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id
        if self.options is None:
            options = None
        elif self.options is UNSET:
            options = UNSET
        else:
            options = []
            for options_item_data in self.options:
                options_item = options_item_data.to_dict()

                options.append(options_item)

        properties: Dict[str, Any] = dict()

        properties["name"] = name
        properties["id"] = id
        if options is not UNSET:
            properties["options"] = options
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Dropdown":
        name = d["name"]

        id = d["id"]

        options = []
        for options_item_data in d.get("options") or []:
            options_item = DropdownOption.from_dict(options_item_data)

            options.append(options_item)

        return Dropdown(
            name=name,
            id=id,
            options=options,
        )
