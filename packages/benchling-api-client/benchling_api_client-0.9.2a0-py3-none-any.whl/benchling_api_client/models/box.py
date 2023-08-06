import datetime
from typing import Any, Dict, Optional, cast

import attr
from dateutil.parser import isoparse

from ..models.archive_record import ArchiveRecord
from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary
from ..types import UNSET


@attr.s(auto_attribs=True)
class Box:
    """  """

    archive_record: Optional[ArchiveRecord] = cast(None, UNSET)
    barcode: Optional[str] = cast(None, UNSET)
    created_at: Optional[datetime.datetime] = cast(None, UNSET)
    creator: Optional[UserSummary] = cast(None, UNSET)
    fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    id: Optional[str] = cast(None, UNSET)
    modified_at: Optional[datetime.datetime] = cast(None, UNSET)
    size: Optional[int] = cast(None, UNSET)
    filled_positions: Optional[int] = cast(None, UNSET)
    empty_positions: Optional[int] = cast(None, UNSET)
    empty_containers: Optional[int] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    parent_storage_id: Optional[str] = cast(None, UNSET)
    project_id: Optional[str] = cast(None, UNSET)
    schema: Optional[SchemaSummary] = cast(None, UNSET)
    web_url: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.archive_record is UNSET:
            archive_record = UNSET
        else:
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        barcode = self.barcode
        if self.created_at is UNSET:
            created_at = UNSET
        else:
            created_at = self.created_at.isoformat() if self.created_at else None

        if self.creator is UNSET:
            creator = UNSET
        else:
            creator = self.creator.to_dict() if self.creator else None

        if self.fields is UNSET:
            fields = UNSET
        else:
            fields = self.fields if self.fields else None

        id = self.id
        if self.modified_at is UNSET:
            modified_at = UNSET
        else:
            modified_at = self.modified_at.isoformat() if self.modified_at else None

        size = self.size
        filled_positions = self.filled_positions
        empty_positions = self.empty_positions
        empty_containers = self.empty_containers
        name = self.name
        parent_storage_id = self.parent_storage_id
        project_id = self.project_id
        if self.schema is UNSET:
            schema = UNSET
        else:
            schema = self.schema.to_dict() if self.schema else None

        web_url = self.web_url

        properties: Dict[str, Any] = dict()

        if archive_record is not UNSET:
            properties["archiveRecord"] = archive_record
        if barcode is not UNSET:
            properties["barcode"] = barcode
        if created_at is not UNSET:
            properties["createdAt"] = created_at
        if creator is not UNSET:
            properties["creator"] = creator
        if fields is not UNSET:
            properties["fields"] = fields
        if id is not UNSET:
            properties["id"] = id
        if modified_at is not UNSET:
            properties["modifiedAt"] = modified_at
        if size is not UNSET:
            properties["size"] = size
        if filled_positions is not UNSET:
            properties["filledPositions"] = filled_positions
        if empty_positions is not UNSET:
            properties["emptyPositions"] = empty_positions
        if empty_containers is not UNSET:
            properties["emptyContainers"] = empty_containers
        if name is not UNSET:
            properties["name"] = name
        if parent_storage_id is not UNSET:
            properties["parentStorageId"] = parent_storage_id
        if project_id is not UNSET:
            properties["projectId"] = project_id
        if schema is not UNSET:
            properties["schema"] = schema
        if web_url is not UNSET:
            properties["webURL"] = web_url
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Box":
        archive_record = None
        if d.get("archiveRecord") is not None:
            archive_record = ArchiveRecord.from_dict(cast(Dict[str, Any], d.get("archiveRecord")))

        barcode = d.get("barcode")

        created_at = None
        if d.get("createdAt") is not None:
            created_at = isoparse(cast(str, d.get("createdAt")))

        creator = None
        if d.get("creator") is not None:
            creator = UserSummary.from_dict(cast(Dict[str, Any], d.get("creator")))

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        id = d.get("id")

        modified_at = None
        if d.get("modifiedAt") is not None:
            modified_at = isoparse(cast(str, d.get("modifiedAt")))

        size = d.get("size")

        filled_positions = d.get("filledPositions")

        empty_positions = d.get("emptyPositions")

        empty_containers = d.get("emptyContainers")

        name = d.get("name")

        parent_storage_id = d.get("parentStorageId")

        project_id = d.get("projectId")

        schema = None
        if d.get("schema") is not None:
            schema = SchemaSummary.from_dict(cast(Dict[str, Any], d.get("schema")))

        web_url = d.get("webURL")

        return Box(
            archive_record=archive_record,
            barcode=barcode,
            created_at=created_at,
            creator=creator,
            fields=fields,
            id=id,
            modified_at=modified_at,
            size=size,
            filled_positions=filled_positions,
            empty_positions=empty_positions,
            empty_containers=empty_containers,
            name=name,
            parent_storage_id=parent_storage_id,
            project_id=project_id,
            schema=schema,
            web_url=web_url,
        )
