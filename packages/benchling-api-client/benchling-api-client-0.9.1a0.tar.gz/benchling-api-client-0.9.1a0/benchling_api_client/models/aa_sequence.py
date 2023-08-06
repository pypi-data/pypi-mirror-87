import datetime
from typing import Any, Dict, List, Optional, cast

import attr
from dateutil.parser import isoparse

from ..models.annotation import Annotation
from ..models.archive_record import ArchiveRecord
from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary
from ..types import UNSET


@attr.s(auto_attribs=True)
class AaSequence:
    """  """

    aliases: Optional[List[str]] = cast(None, UNSET)
    amino_acids: Optional[str] = cast(None, UNSET)
    annotations: Optional[List[Annotation]] = cast(None, UNSET)
    archive_record: Optional[ArchiveRecord] = cast(None, UNSET)
    created_at: Optional[datetime.datetime] = cast(None, UNSET)
    creator: Optional[UserSummary] = cast(None, UNSET)
    custom_fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    entity_registry_id: Optional[str] = cast(None, UNSET)
    fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    folder_id: Optional[str] = cast(None, UNSET)
    id: Optional[str] = cast(None, UNSET)
    length: Optional[int] = cast(None, UNSET)
    modified_at: Optional[datetime.datetime] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    registry_id: Optional[str] = cast(None, UNSET)
    schema: Optional[SchemaSummary] = cast(None, UNSET)
    web_url: Optional[str] = cast(None, UNSET)
    api_url: Optional[str] = cast(None, UNSET)

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

        if self.archive_record is UNSET:
            archive_record = UNSET
        else:
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        if self.created_at is UNSET:
            created_at = UNSET
        else:
            created_at = self.created_at.isoformat() if self.created_at else None

        if self.creator is UNSET:
            creator = UNSET
        else:
            creator = self.creator.to_dict() if self.creator else None

        if self.custom_fields is UNSET:
            custom_fields = UNSET
        else:
            custom_fields = self.custom_fields if self.custom_fields else None

        entity_registry_id = self.entity_registry_id
        if self.fields is UNSET:
            fields = UNSET
        else:
            fields = self.fields if self.fields else None

        folder_id = self.folder_id
        id = self.id
        length = self.length
        if self.modified_at is UNSET:
            modified_at = UNSET
        else:
            modified_at = self.modified_at.isoformat() if self.modified_at else None

        name = self.name
        registry_id = self.registry_id
        if self.schema is UNSET:
            schema = UNSET
        else:
            schema = self.schema.to_dict() if self.schema else None

        web_url = self.web_url
        api_url = self.api_url

        properties: Dict[str, Any] = dict()

        if aliases is not UNSET:
            properties["aliases"] = aliases
        if amino_acids is not UNSET:
            properties["aminoAcids"] = amino_acids
        if annotations is not UNSET:
            properties["annotations"] = annotations
        if archive_record is not UNSET:
            properties["archiveRecord"] = archive_record
        if created_at is not UNSET:
            properties["createdAt"] = created_at
        if creator is not UNSET:
            properties["creator"] = creator
        if custom_fields is not UNSET:
            properties["customFields"] = custom_fields
        if entity_registry_id is not UNSET:
            properties["entityRegistryId"] = entity_registry_id
        if fields is not UNSET:
            properties["fields"] = fields
        if folder_id is not UNSET:
            properties["folderId"] = folder_id
        if id is not UNSET:
            properties["id"] = id
        if length is not UNSET:
            properties["length"] = length
        if modified_at is not UNSET:
            properties["modifiedAt"] = modified_at
        if name is not UNSET:
            properties["name"] = name
        if registry_id is not UNSET:
            properties["registryId"] = registry_id
        if schema is not UNSET:
            properties["schema"] = schema
        if web_url is not UNSET:
            properties["webURL"] = web_url
        if api_url is not UNSET:
            properties["apiURL"] = api_url
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AaSequence":
        aliases = d.get("aliases")

        amino_acids = d.get("aminoAcids")

        annotations = []
        for annotations_item_data in d.get("annotations") or []:
            annotations_item = Annotation.from_dict(annotations_item_data)

            annotations.append(annotations_item)

        archive_record = None
        if d.get("archiveRecord") is not None:
            archive_record = ArchiveRecord.from_dict(cast(Dict[str, Any], d.get("archiveRecord")))

        created_at = None
        if d.get("createdAt") is not None:
            created_at = isoparse(cast(str, d.get("createdAt")))

        creator = None
        if d.get("creator") is not None:
            creator = UserSummary.from_dict(cast(Dict[str, Any], d.get("creator")))

        custom_fields = None
        if d.get("customFields") is not None:
            custom_fields = d.get("customFields")

        entity_registry_id = d.get("entityRegistryId")

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        folder_id = d.get("folderId")

        id = d.get("id")

        length = d.get("length")

        modified_at = None
        if d.get("modifiedAt") is not None:
            modified_at = isoparse(cast(str, d.get("modifiedAt")))

        name = d.get("name")

        registry_id = d.get("registryId")

        schema = None
        if d.get("schema") is not None:
            schema = SchemaSummary.from_dict(cast(Dict[str, Any], d.get("schema")))

        web_url = d.get("webURL")

        api_url = d.get("apiURL")

        return AaSequence(
            aliases=aliases,
            amino_acids=amino_acids,
            annotations=annotations,
            archive_record=archive_record,
            created_at=created_at,
            creator=creator,
            custom_fields=custom_fields,
            entity_registry_id=entity_registry_id,
            fields=fields,
            folder_id=folder_id,
            id=id,
            length=length,
            modified_at=modified_at,
            name=name,
            registry_id=registry_id,
            schema=schema,
            web_url=web_url,
            api_url=api_url,
        )
