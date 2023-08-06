from typing import Any, Dict, List, Optional, cast

import attr

from ..models.annotation import Annotation
from ..models.naming_strategy import NamingStrategy
from ..types import UNSET


@attr.s(auto_attribs=True)
class AaSequenceCreate:
    """  """

    registry_id: Optional[str] = cast(None, UNSET)
    naming_strategy: Optional[NamingStrategy] = cast(None, UNSET)
    entity_registry_id: Optional[str] = cast(None, UNSET)
    author_ids: Optional[List[str]] = cast(None, UNSET)
    aliases: Optional[List[str]] = cast(None, UNSET)
    amino_acids: Optional[str] = cast(None, UNSET)
    annotations: Optional[List[Annotation]] = cast(None, UNSET)
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

        amino_acids = self.amino_acids
        if self.annotations is None:
            annotations = None
        elif self.annotations is UNSET:
            annotations = UNSET
        else:
            annotations = []
            for annotations_item_data in self.annotations:
                annotations_item = annotations_item_data.to_dict()

                annotations.append(annotations_item)

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
        if author_ids is not UNSET:
            properties["authorIds"] = author_ids
        if aliases is not UNSET:
            properties["aliases"] = aliases
        if amino_acids is not UNSET:
            properties["aminoAcids"] = amino_acids
        if annotations is not UNSET:
            properties["annotations"] = annotations
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
    def from_dict(d: Dict[str, Any]) -> "AaSequenceCreate":
        registry_id = d.get("registryId")

        naming_strategy = None
        if d.get("namingStrategy") is not None:
            naming_strategy = NamingStrategy(d.get("namingStrategy"))

        entity_registry_id = d.get("entityRegistryId")

        author_ids = d.get("authorIds")

        aliases = d.get("aliases")

        amino_acids = d.get("aminoAcids")

        annotations = []
        for annotations_item_data in d.get("annotations") or []:
            annotations_item = Annotation.from_dict(annotations_item_data)

            annotations.append(annotations_item)

        custom_fields = None
        if d.get("customFields") is not None:
            custom_fields = d.get("customFields")

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        folder_id = d.get("folderId")

        name = d.get("name")

        schema_id = d.get("schemaId")

        return AaSequenceCreate(
            registry_id=registry_id,
            naming_strategy=naming_strategy,
            entity_registry_id=entity_registry_id,
            author_ids=author_ids,
            aliases=aliases,
            amino_acids=amino_acids,
            annotations=annotations,
            custom_fields=custom_fields,
            fields=fields,
            folder_id=folder_id,
            name=name,
            schema_id=schema_id,
        )
