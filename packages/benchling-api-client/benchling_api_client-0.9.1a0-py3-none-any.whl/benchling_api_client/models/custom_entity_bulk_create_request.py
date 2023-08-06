from typing import Any, Dict, List, Optional, cast

import attr

from ..models.naming_strategy import NamingStrategy
from ..types import UNSET


@attr.s(auto_attribs=True)
class CustomEntityBulkCreateRequest:
    """  """

    registry_id: Optional[str] = cast(None, UNSET)
    naming_strategy: Optional[NamingStrategy] = cast(None, UNSET)
    entity_registry_id: Optional[str] = cast(None, UNSET)
    aliases: Optional[List[str]] = cast(None, UNSET)
    custom_fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    folder_id: Optional[str] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    schema_id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        registry_id = self.registry_id
        if self.naming_strategy is UNSET:
            naming_strategy = UNSET
        else:
            naming_strategy = self.naming_strategy.value if self.naming_strategy else None

        entity_registry_id = self.entity_registry_id
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

        if registry_id is not UNSET:
            properties["registryId"] = registry_id
        if naming_strategy is not UNSET:
            properties["namingStrategy"] = naming_strategy
        if entity_registry_id is not UNSET:
            properties["entityRegistryId"] = entity_registry_id
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
    def from_dict(d: Dict[str, Any]) -> "CustomEntityBulkCreateRequest":
        registry_id = d.get("registryId")

        naming_strategy = None
        if d.get("namingStrategy") is not None:
            naming_strategy = NamingStrategy(d.get("namingStrategy"))

        entity_registry_id = d.get("entityRegistryId")

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

        return CustomEntityBulkCreateRequest(
            registry_id=registry_id,
            naming_strategy=naming_strategy,
            entity_registry_id=entity_registry_id,
            aliases=aliases,
            custom_fields=custom_fields,
            fields=fields,
            folder_id=folder_id,
            name=name,
            schema_id=schema_id,
        )
