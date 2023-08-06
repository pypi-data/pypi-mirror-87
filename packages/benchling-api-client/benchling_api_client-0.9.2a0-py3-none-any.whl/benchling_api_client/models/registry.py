from typing import Any, Dict, Optional, cast

import attr

from ..models.organization import Organization
from ..types import UNSET


@attr.s(auto_attribs=True)
class Registry:
    """  """

    id: Optional[str] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    owner: Optional[Organization] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        if self.owner is UNSET:
            owner = UNSET
        else:
            owner = self.owner.to_dict() if self.owner else None

        properties: Dict[str, Any] = dict()

        if id is not UNSET:
            properties["id"] = id
        if name is not UNSET:
            properties["name"] = name
        if owner is not UNSET:
            properties["owner"] = owner
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Registry":
        id = d.get("id")

        name = d.get("name")

        owner = None
        if d.get("owner") is not None:
            owner = Organization.from_dict(cast(Dict[str, Any], d.get("owner")))

        return Registry(
            id=id,
            name=name,
            owner=owner,
        )
