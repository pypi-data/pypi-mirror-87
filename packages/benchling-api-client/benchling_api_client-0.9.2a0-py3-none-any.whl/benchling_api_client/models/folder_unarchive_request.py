from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class FolderUnarchiveRequest:
    """  """

    folder_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        folder_ids = self.folder_ids

        properties: Dict[str, Any] = dict()

        properties["folderIds"] = folder_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FolderUnarchiveRequest":
        folder_ids = d["folderIds"]

        return FolderUnarchiveRequest(
            folder_ids=folder_ids,
        )
