from typing import Any, Dict, List, Optional, cast

import attr

from ..models.annotation import Annotation
from ..models.naming_strategy import NamingStrategy
from ..models.primer import Primer
from ..models.translation import Translation
from ..types import UNSET


@attr.s(auto_attribs=True)
class DnaSequenceBulkCreate:
    """  """

    registry_id: Optional[str] = cast(None, UNSET)
    naming_strategy: Optional[NamingStrategy] = cast(None, UNSET)
    entity_registry_id: Optional[str] = cast(None, UNSET)
    aliases: Optional[List[str]] = cast(None, UNSET)
    annotations: Optional[List[Annotation]] = cast(None, UNSET)
    bases: Optional[str] = cast(None, UNSET)
    custom_fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    folder_id: Optional[str] = cast(None, UNSET)
    is_circular: Optional[bool] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    primers: Optional[List[Primer]] = cast(None, UNSET)
    schema_id: Optional[str] = cast(None, UNSET)
    translations: Optional[List[Translation]] = cast(None, UNSET)

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

        if self.annotations is None:
            annotations = None
        elif self.annotations is UNSET:
            annotations = UNSET
        else:
            annotations = []
            for annotations_item_data in self.annotations:
                annotations_item = annotations_item_data.to_dict()

                annotations.append(annotations_item)

        bases = self.bases
        if self.custom_fields is UNSET:
            custom_fields = UNSET
        else:
            custom_fields = self.custom_fields if self.custom_fields else None

        if self.fields is UNSET:
            fields = UNSET
        else:
            fields = self.fields if self.fields else None

        folder_id = self.folder_id
        is_circular = self.is_circular
        name = self.name
        if self.primers is None:
            primers = None
        elif self.primers is UNSET:
            primers = UNSET
        else:
            primers = []
            for primers_item_data in self.primers:
                primers_item = primers_item_data.to_dict()

                primers.append(primers_item)

        schema_id = self.schema_id
        if self.translations is None:
            translations = None
        elif self.translations is UNSET:
            translations = UNSET
        else:
            translations = []
            for translations_item_data in self.translations:
                translations_item = translations_item_data.to_dict()

                translations.append(translations_item)

        properties: Dict[str, Any] = dict()

        if registry_id is not UNSET:
            properties["registryId"] = registry_id
        if naming_strategy is not UNSET:
            properties["namingStrategy"] = naming_strategy
        if entity_registry_id is not UNSET:
            properties["entityRegistryId"] = entity_registry_id
        if aliases is not UNSET:
            properties["aliases"] = aliases
        if annotations is not UNSET:
            properties["annotations"] = annotations
        if bases is not UNSET:
            properties["bases"] = bases
        if custom_fields is not UNSET:
            properties["customFields"] = custom_fields
        if fields is not UNSET:
            properties["fields"] = fields
        if folder_id is not UNSET:
            properties["folderId"] = folder_id
        if is_circular is not UNSET:
            properties["isCircular"] = is_circular
        if name is not UNSET:
            properties["name"] = name
        if primers is not UNSET:
            properties["primers"] = primers
        if schema_id is not UNSET:
            properties["schemaId"] = schema_id
        if translations is not UNSET:
            properties["translations"] = translations
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DnaSequenceBulkCreate":
        registry_id = d.get("registryId")

        naming_strategy = None
        if d.get("namingStrategy") is not None:
            naming_strategy = NamingStrategy(d.get("namingStrategy"))

        entity_registry_id = d.get("entityRegistryId")

        aliases = d.get("aliases")

        annotations = []
        for annotations_item_data in d.get("annotations") or []:
            annotations_item = Annotation.from_dict(annotations_item_data)

            annotations.append(annotations_item)

        bases = d.get("bases")

        custom_fields = None
        if d.get("customFields") is not None:
            custom_fields = d.get("customFields")

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        folder_id = d.get("folderId")

        is_circular = d.get("isCircular")

        name = d.get("name")

        primers = []
        for primers_item_data in d.get("primers") or []:
            primers_item = Primer.from_dict(primers_item_data)

            primers.append(primers_item)

        schema_id = d.get("schemaId")

        translations = []
        for translations_item_data in d.get("translations") or []:
            translations_item = Translation.from_dict(translations_item_data)

            translations.append(translations_item)

        return DnaSequenceBulkCreate(
            registry_id=registry_id,
            naming_strategy=naming_strategy,
            entity_registry_id=entity_registry_id,
            aliases=aliases,
            annotations=annotations,
            bases=bases,
            custom_fields=custom_fields,
            fields=fields,
            folder_id=folder_id,
            is_circular=is_circular,
            name=name,
            primers=primers,
            schema_id=schema_id,
            translations=translations,
        )
