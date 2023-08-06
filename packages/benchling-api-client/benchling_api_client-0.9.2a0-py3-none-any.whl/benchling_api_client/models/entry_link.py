from typing import Any, Dict, Optional, cast

import attr

from ..models.type12345 import Type12345
from ..types import UNSET


@attr.s(auto_attribs=True)
class EntryLink:
    """Links are contained within notes to reference resources that live outside of the entry. A link can target an external resource via an http(s):// hyperlink or a Benchling resource via @-mentions and drag-n-drop."""

    id: Optional[str] = cast(None, UNSET)
    type: Optional[Type12345] = cast(None, UNSET)
    web_url: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        if self.type is UNSET:
            type = UNSET
        else:
            type = self.type.value if self.type else None

        web_url = self.web_url

        properties: Dict[str, Any] = dict()

        if id is not UNSET:
            properties["id"] = id
        if type is not UNSET:
            properties["type"] = type
        if web_url is not UNSET:
            properties["webURL"] = web_url
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EntryLink":
        id = d.get("id")

        type = None
        if d.get("type") is not None:
            type = Type12345(d.get("type"))

        web_url = d.get("webURL")

        return EntryLink(
            id=id,
            type=type,
            web_url=web_url,
        )
