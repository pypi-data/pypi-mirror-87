from typing import Any, Dict, List, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class CustomEntityPatch:
    """  """

    entity_registry_id: Optional[str] = cast(None, UNSET)
    author_ids: Optional[List[str]] = cast(None, UNSET)
    aliases: Optional[List[str]] = cast(None, UNSET)
    custom_fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    folder_id: Optional[str] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    schema_id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        entity_registry_id = self.entity_registry_id
        if self.author_ids is None:
            author_ids = None
        elif self.author_ids is UNSET:
            author_ids = UNSET
        else:
            author_ids = self.author_ids

        if self.aliases is None:
            aliases = None
        elif self.aliases is UNSET:
            aliases = UNSET
        else:
            aliases = self.aliases

        if self.custom_fields is UNSET:
            custom_fields = UNSET
        else:
            custom_fields = self.custom_fields if self.custom_fields else None

        if self.fields is UNSET:
            fields = UNSET
        else:
            fields = self.fields if self.fields else None

        folder_id = self.folder_id
        name = self.name
        schema_id = self.schema_id

        properties: Dict[str, Any] = dict()

        if entity_registry_id is not UNSET:
            properties["entityRegistryId"] = entity_registry_id
        if author_ids is not UNSET:
            properties["authorIds"] = author_ids
        if aliases is not UNSET:
            properties["aliases"] = aliases
        if custom_fields is not UNSET:
            properties["customFields"] = custom_fields
        if fields is not UNSET:
            properties["fields"] = fields
        if folder_id is not UNSET:
            properties["folderId"] = folder_id
        if name is not UNSET:
            properties["name"] = name
        if schema_id is not UNSET:
            properties["schemaId"] = schema_id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CustomEntityPatch":
        entity_registry_id = d.get("entityRegistryId")

        author_ids = d.get("authorIds")

        aliases = d.get("aliases")

        custom_fields = None
        if d.get("customFields") is not None:
            custom_fields = d.get("customFields")

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        folder_id = d.get("folderId")

        name = d.get("name")

        schema_id = d.get("schemaId")

        return CustomEntityPatch(
            entity_registry_id=entity_registry_id,
            author_ids=author_ids,
            aliases=aliases,
            custom_fields=custom_fields,
            fields=fields,
            folder_id=folder_id,
            name=name,
            schema_id=schema_id,
        )
