from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class SchemaSummary:
    """  """

    id: Optional[str] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name

        properties: Dict[str, Any] = dict()

        if id is not UNSET:
            properties["id"] = id
        if name is not UNSET:
            properties["name"] = name
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SchemaSummary":
        id = d.get("id")

        name = d.get("name")

        return SchemaSummary(
            id=id,
            name=name,
        )
