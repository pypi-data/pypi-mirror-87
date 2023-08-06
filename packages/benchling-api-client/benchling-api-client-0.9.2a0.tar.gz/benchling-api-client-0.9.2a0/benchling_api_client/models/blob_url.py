from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class BlobUrl:
    """  """

    download_url: Optional[str] = cast(None, UNSET)
    expires_at: Optional[int] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        download_url = self.download_url
        expires_at = self.expires_at

        properties: Dict[str, Any] = dict()

        if download_url is not UNSET:
            properties["downloadURL"] = download_url
        if expires_at is not UNSET:
            properties["expiresAt"] = expires_at
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BlobUrl":
        download_url = d.get("downloadURL")

        expires_at = d.get("expiresAt")

        return BlobUrl(
            download_url=download_url,
            expires_at=expires_at,
        )
