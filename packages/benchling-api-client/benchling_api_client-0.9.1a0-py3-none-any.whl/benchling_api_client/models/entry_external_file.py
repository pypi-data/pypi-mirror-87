from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class EntryExternalFile:
    """The ExternalFile resource stores metadata about the file. The actual original file can be downloaded by using the 'downloadURL' property."""

    id: Optional[str] = cast(None, UNSET)
    download_url: Optional[str] = cast(None, UNSET)
    expires_at: Optional[int] = cast(None, UNSET)
    size: Optional[int] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        download_url = self.download_url
        expires_at = self.expires_at
        size = self.size

        properties: Dict[str, Any] = dict()

        if id is not UNSET:
            properties["id"] = id
        if download_url is not UNSET:
            properties["downloadURL"] = download_url
        if expires_at is not UNSET:
            properties["expiresAt"] = expires_at
        if size is not UNSET:
            properties["size"] = size
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EntryExternalFile":
        id = d.get("id")

        download_url = d.get("downloadURL")

        expires_at = d.get("expiresAt")

        size = d.get("size")

        return EntryExternalFile(
            id=id,
            download_url=download_url,
            expires_at=expires_at,
            size=size,
        )
