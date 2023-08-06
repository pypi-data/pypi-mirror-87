from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class CreateFolder:
    """  """

    name: str
    parent_folder_id: str

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        parent_folder_id = self.parent_folder_id

        properties: Dict[str, Any] = dict()

        properties["name"] = name
        properties["parentFolderId"] = parent_folder_id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CreateFolder":
        name = d["name"]

        parent_folder_id = d["parentFolderId"]

        return CreateFolder(
            name=name,
            parent_folder_id=parent_folder_id,
        )
