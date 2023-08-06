from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class EntryPatch:
    """  """

    author_ids: Optional[str] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    folder_id: Optional[str] = cast(None, UNSET)
    fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    schema_id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        author_ids = self.author_ids
        name = self.name
        folder_id = self.folder_id
        if self.fields is UNSET:
            fields = UNSET
        else:
            fields = self.fields if self.fields else None

        schema_id = self.schema_id

        properties: Dict[str, Any] = dict()

        if author_ids is not UNSET:
            properties["authorIds"] = author_ids
        if name is not UNSET:
            properties["name"] = name
        if folder_id is not UNSET:
            properties["folderId"] = folder_id
        if fields is not UNSET:
            properties["fields"] = fields
        if schema_id is not UNSET:
            properties["schemaId"] = schema_id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EntryPatch":
        author_ids = d.get("authorIds")

        name = d.get("name")

        folder_id = d.get("folderId")

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        schema_id = d.get("schemaId")

        return EntryPatch(
            author_ids=author_ids,
            name=name,
            folder_id=folder_id,
            fields=fields,
            schema_id=schema_id,
        )
