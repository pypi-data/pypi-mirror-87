from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class Folder:
    """  """

    id: Optional[str] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    parent_folder_id: Optional[str] = cast(None, UNSET)
    project_id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        parent_folder_id = self.parent_folder_id
        project_id = self.project_id

        properties: Dict[str, Any] = dict()

        if id is not UNSET:
            properties["id"] = id
        if name is not UNSET:
            properties["name"] = name
        if parent_folder_id is not UNSET:
            properties["parentFolderId"] = parent_folder_id
        if project_id is not UNSET:
            properties["projectId"] = project_id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Folder":
        id = d.get("id")

        name = d.get("name")

        parent_folder_id = d.get("parentFolderId")

        project_id = d.get("projectId")

        return Folder(
            id=id,
            name=name,
            parent_folder_id=parent_folder_id,
            project_id=project_id,
        )
