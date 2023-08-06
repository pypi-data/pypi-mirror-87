from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class TeamSummary:
    """  """

    name: Optional[str] = cast(None, UNSET)
    handle: Optional[str] = cast(None, UNSET)
    id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        handle = self.handle
        id = self.id

        properties: Dict[str, Any] = dict()

        if name is not UNSET:
            properties["name"] = name
        if handle is not UNSET:
            properties["handle"] = handle
        if id is not UNSET:
            properties["id"] = id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "TeamSummary":
        name = d.get("name")

        handle = d.get("handle")

        id = d.get("id")

        return TeamSummary(
            name=name,
            handle=handle,
            id=id,
        )
