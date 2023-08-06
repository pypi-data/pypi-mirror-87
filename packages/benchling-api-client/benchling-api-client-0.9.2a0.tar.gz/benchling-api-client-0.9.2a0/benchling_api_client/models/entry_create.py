from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class EntryCreate:
    """  """

    name: str
    folder_id: str
    author_ids: Optional[str] = cast(None, UNSET)
    entry_template_id: Optional[str] = cast(None, UNSET)
    schema_id: Optional[str] = cast(None, UNSET)
    custom_fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    fields: Optional[Dict[Any, Any]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        folder_id = self.folder_id
        author_ids = self.author_ids
        entry_template_id = self.entry_template_id
        schema_id = self.schema_id
        if self.custom_fields is UNSET:
            custom_fields = UNSET
        else:
            custom_fields = self.custom_fields if self.custom_fields else None

        if self.fields is UNSET:
            fields = UNSET
        else:
            fields = self.fields if self.fields else None

        properties: Dict[str, Any] = dict()

        properties["name"] = name
        properties["folderId"] = folder_id
        if author_ids is not UNSET:
            properties["authorIds"] = author_ids
        if entry_template_id is not UNSET:
            properties["entryTemplateId"] = entry_template_id
        if schema_id is not UNSET:
            properties["schemaId"] = schema_id
        if custom_fields is not UNSET:
            properties["customFields"] = custom_fields
        if fields is not UNSET:
            properties["fields"] = fields
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EntryCreate":
        name = d["name"]

        folder_id = d["folderId"]

        author_ids = d.get("authorIds")

        entry_template_id = d.get("entryTemplateId")

        schema_id = d.get("schemaId")

        custom_fields = None
        if d.get("customFields") is not None:
            custom_fields = d.get("customFields")

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        return EntryCreate(
            name=name,
            folder_id=folder_id,
            author_ids=author_ids,
            entry_template_id=entry_template_id,
            schema_id=schema_id,
            custom_fields=custom_fields,
            fields=fields,
        )
