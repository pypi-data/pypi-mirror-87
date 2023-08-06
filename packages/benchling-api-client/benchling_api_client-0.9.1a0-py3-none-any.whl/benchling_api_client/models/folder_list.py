from typing import Any, Dict, List

import attr

from ..models.folder import Folder


@attr.s(auto_attribs=True)
class FolderList:
    """  """

    next_token: str
    folders: List[Folder]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        folders = []
        for folders_item_data in self.folders:
            folders_item = folders_item_data.to_dict()

            folders.append(folders_item)

        properties: Dict[str, Any] = dict()

        properties["nextToken"] = next_token
        properties["folders"] = folders
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FolderList":
        next_token = d["nextToken"]

        folders = []
        for folders_item_data in d["folders"]:
            folders_item = Folder.from_dict(folders_item_data)

            folders.append(folders_item)

        return FolderList(
            next_token=next_token,
            folders=folders,
        )
