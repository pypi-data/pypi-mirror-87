from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class Organization:
    """  """

    handle: Optional[str] = cast(None, UNSET)
    id: Optional[str] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        handle = self.handle
        id = self.id
        name = self.name

        properties: Dict[str, Any] = dict()

        if handle is not UNSET:
            properties["handle"] = handle
        if id is not UNSET:
            properties["id"] = id
        if name is not UNSET:
            properties["name"] = name
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Organization":
        handle = d.get("handle")

        id = d.get("id")

        name = d.get("name")

        return Organization(
            handle=handle,
            id=id,
            name=name,
        )
