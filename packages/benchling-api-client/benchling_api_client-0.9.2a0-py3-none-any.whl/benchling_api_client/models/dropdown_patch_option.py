from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class DropdownPatchOption:
    """  """

    name: str
    id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id

        properties: Dict[str, Any] = dict()

        properties["name"] = name
        if id is not UNSET:
            properties["id"] = id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DropdownPatchOption":
        name = d["name"]

        id = d.get("id")

        return DropdownPatchOption(
            name=name,
            id=id,
        )
