from typing import Any, Dict, Optional

import attr

from ..models.type123456 import Type123456
from ..types import UNSET


@attr.s(auto_attribs=True)
class BlobMultipartCreate:
    """  """

    name: str
    type: Type123456
    mime_type: Optional[str] = "application/octet-stream"

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        type = self.type.value

        mime_type = self.mime_type

        properties: Dict[str, Any] = dict()

        properties["name"] = name
        properties["type"] = type
        if mime_type is not UNSET:
            properties["mimeType"] = mime_type
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BlobMultipartCreate":
        name = d["name"]

        type = Type123456(d["type"])

        mime_type = d.get("mimeType")

        return BlobMultipartCreate(
            name=name,
            type=type,
            mime_type=mime_type,
        )
