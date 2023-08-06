from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class DropdownOption:
    """  """

    name: Optional[str] = cast(None, UNSET)
    id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id

        properties: Dict[str, Any] = dict()

        if name is not UNSET:
            properties["name"] = name
        if id is not UNSET:
            properties["id"] = id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DropdownOption":
        name = d.get("name")

        id = d.get("id")

        return DropdownOption(
            name=name,
            id=id,
        )
