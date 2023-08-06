from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class BoxPatch:
    """  """

    name: Optional[str] = cast(None, UNSET)
    fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    parent_storage_id: Optional[str] = cast(None, UNSET)
    project_id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        if self.fields is UNSET:
            fields = UNSET
        else:
            fields = self.fields if self.fields else None

        parent_storage_id = self.parent_storage_id
        project_id = self.project_id

        properties: Dict[str, Any] = dict()

        if name is not UNSET:
            properties["name"] = name
        if fields is not UNSET:
            properties["fields"] = fields
        if parent_storage_id is not UNSET:
            properties["parentStorageId"] = parent_storage_id
        if project_id is not UNSET:
            properties["projectId"] = project_id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BoxPatch":
        name = d.get("name")

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        parent_storage_id = d.get("parentStorageId")

        project_id = d.get("projectId")

        return BoxPatch(
            name=name,
            fields=fields,
            parent_storage_id=parent_storage_id,
            project_id=project_id,
        )
