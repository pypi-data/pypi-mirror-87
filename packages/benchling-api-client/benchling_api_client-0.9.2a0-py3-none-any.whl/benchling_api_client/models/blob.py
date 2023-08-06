from typing import Any, Dict, Optional, cast

import attr

from ..models.type123456 import Type123456
from ..models.upload_status import UploadStatus
from ..types import UNSET


@attr.s(auto_attribs=True)
class Blob:
    """  """

    id: Optional[str] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    type: Optional[Type123456] = cast(None, UNSET)
    mime_type: Optional[str] = cast(None, UNSET)
    upload_status: Optional[UploadStatus] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        if self.type is UNSET:
            type = UNSET
        else:
            type = self.type.value if self.type else None

        mime_type = self.mime_type
        if self.upload_status is UNSET:
            upload_status = UNSET
        else:
            upload_status = self.upload_status.value if self.upload_status else None

        properties: Dict[str, Any] = dict()

        if id is not UNSET:
            properties["id"] = id
        if name is not UNSET:
            properties["name"] = name
        if type is not UNSET:
            properties["type"] = type
        if mime_type is not UNSET:
            properties["mimeType"] = mime_type
        if upload_status is not UNSET:
            properties["uploadStatus"] = upload_status
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Blob":
        id = d.get("id")

        name = d.get("name")

        type = None
        if d.get("type") is not None:
            type = Type123456(d.get("type"))

        mime_type = d.get("mimeType")

        upload_status = None
        if d.get("uploadStatus") is not None:
            upload_status = UploadStatus(d.get("uploadStatus"))

        return Blob(
            id=id,
            name=name,
            type=type,
            mime_type=mime_type,
            upload_status=upload_status,
        )
