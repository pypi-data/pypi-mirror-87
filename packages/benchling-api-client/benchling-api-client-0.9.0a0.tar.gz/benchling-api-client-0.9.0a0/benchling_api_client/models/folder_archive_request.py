from typing import Any, Dict, List

import attr

from ..models.reason1 import Reason1


@attr.s(auto_attribs=True)
class FolderArchiveRequest:
    """  """

    reason: Reason1
    folder_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason.value

        folder_ids = self.folder_ids

        properties: Dict[str, Any] = dict()

        properties["reason"] = reason
        properties["folderIds"] = folder_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FolderArchiveRequest":
        reason = Reason1(d["reason"])

        folder_ids = d["folderIds"]

        return FolderArchiveRequest(
            reason=reason,
            folder_ids=folder_ids,
        )
