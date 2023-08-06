from typing import Any, Dict, List, Optional, cast

import attr

from ..models.annotation import Annotation
from ..types import UNSET


@attr.s(auto_attribs=True)
class AaSequenceBaseRequest:
    """  """

    aliases: Optional[List[str]] = cast(None, UNSET)
    amino_acids: Optional[str] = cast(None, UNSET)
    annotations: Optional[List[Annotation]] = cast(None, UNSET)
    custom_fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    folder_id: Optional[str] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    schema_id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
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
    def from_dict(d: Dict[str, Any]) -> "AaSequenceBaseRequest":
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

        return AaSequenceBaseRequest(
            aliases=aliases,
            amino_acids=amino_acids,
            annotations=annotations,
            custom_fields=custom_fields,
            fields=fields,
            folder_id=folder_id,
            name=name,
            schema_id=schema_id,
        )
