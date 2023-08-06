import datetime
from typing import Any, Dict, List, Optional, cast

import attr
from dateutil.parser import isoparse

from ..models.archive_record import ArchiveRecord
from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary
from ..types import UNSET


@attr.s(auto_attribs=True)
class Entity:
    """  """

    aliases: Optional[List[str]] = cast(None, UNSET)
    archive_record: Optional[ArchiveRecord] = cast(None, UNSET)
    authors: Optional[List[UserSummary]] = cast(None, UNSET)
    created_at: Optional[datetime.datetime] = cast(None, UNSET)
    custom_fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    entity_registry_id: Optional[str] = cast(None, UNSET)
    fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    folder_id: Optional[str] = cast(None, UNSET)
    id: Optional[str] = cast(None, UNSET)
    modified_at: Optional[datetime.datetime] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    registry_id: Optional[str] = cast(None, UNSET)
    schema: Optional[SchemaSummary] = cast(None, UNSET)
    web_url: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.aliases is None:
            aliases = None
        elif self.aliases is UNSET:
            aliases = UNSET
        else:
            aliases = self.aliases

        if self.archive_record is UNSET:
            archive_record = UNSET
        else:
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        if self.authors is None:
            authors = None
        elif self.authors is UNSET:
            authors = UNSET
        else:
            authors = []
            for authors_item_data in self.authors:
                authors_item = authors_item_data.to_dict()

                authors.append(authors_item)

        if self.created_at is UNSET:
            created_at = UNSET
        else:
            created_at = self.created_at.isoformat() if self.created_at else None

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

        properties: Dict[str, Any] = dict()

        if aliases is not UNSET:
            properties["aliases"] = aliases
        if archive_record is not UNSET:
            properties["archiveRecord"] = archive_record
        if authors is not UNSET:
            properties["authors"] = authors
        if created_at is not UNSET:
            properties["createdAt"] = created_at
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
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Entity":
        aliases = d.get("aliases")

        archive_record = None
        if d.get("archiveRecord") is not None:
            archive_record = ArchiveRecord.from_dict(cast(Dict[str, Any], d.get("archiveRecord")))

        authors = []
        for authors_item_data in d.get("authors") or []:
            authors_item = UserSummary.from_dict(authors_item_data)

            authors.append(authors_item)

        created_at = None
        if d.get("createdAt") is not None:
            created_at = isoparse(cast(str, d.get("createdAt")))

        custom_fields = None
        if d.get("customFields") is not None:
            custom_fields = d.get("customFields")

        entity_registry_id = d.get("entityRegistryId")

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        folder_id = d.get("folderId")

        id = d.get("id")

        modified_at = None
        if d.get("modifiedAt") is not None:
            modified_at = isoparse(cast(str, d.get("modifiedAt")))

        name = d.get("name")

        registry_id = d.get("registryId")

        schema = None
        if d.get("schema") is not None:
            schema = SchemaSummary.from_dict(cast(Dict[str, Any], d.get("schema")))

        web_url = d.get("webURL")

        return Entity(
            aliases=aliases,
            archive_record=archive_record,
            authors=authors,
            created_at=created_at,
            custom_fields=custom_fields,
            entity_registry_id=entity_registry_id,
            fields=fields,
            folder_id=folder_id,
            id=id,
            modified_at=modified_at,
            name=name,
            registry_id=registry_id,
            schema=schema,
            web_url=web_url,
        )
