import datetime
from typing import Any, Dict, List, Optional, cast

import attr
from dateutil.parser import isoparse

from ..models.container_content import ContainerContent
from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary
from ..types import UNSET


@attr.s(auto_attribs=True)
class Well:
    """  """

    barcode: Optional[str] = cast(None, UNSET)
    contents: Optional[List[ContainerContent]] = cast(None, UNSET)
    created_at: Optional[datetime.datetime] = cast(None, UNSET)
    creator: Optional[UserSummary] = cast(None, UNSET)
    fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    id: Optional[str] = cast(None, UNSET)
    modified_at: Optional[datetime.datetime] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    parent_storage_id: Optional[str] = cast(None, UNSET)
    parent_storage_schema: Optional[SchemaSummary] = cast(None, UNSET)
    project_id: Optional[str] = cast(None, UNSET)
    schema: Optional[SchemaSummary] = cast(None, UNSET)
    volume: Optional[Dict[Any, Any]] = cast(None, UNSET)
    web_url: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        barcode = self.barcode
        if self.contents is None:
            contents = None
        elif self.contents is UNSET:
            contents = UNSET
        else:
            contents = []
            for contents_item_data in self.contents:
                contents_item = contents_item_data.to_dict()

                contents.append(contents_item)

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

        name = self.name
        parent_storage_id = self.parent_storage_id
        if self.parent_storage_schema is UNSET:
            parent_storage_schema = UNSET
        else:
            parent_storage_schema = self.parent_storage_schema.to_dict() if self.parent_storage_schema else None

        project_id = self.project_id
        if self.schema is UNSET:
            schema = UNSET
        else:
            schema = self.schema.to_dict() if self.schema else None

        if self.volume is UNSET:
            volume = UNSET
        else:
            volume = self.volume if self.volume else None

        web_url = self.web_url

        properties: Dict[str, Any] = dict()

        if barcode is not UNSET:
            properties["barcode"] = barcode
        if contents is not UNSET:
            properties["contents"] = contents
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
        if name is not UNSET:
            properties["name"] = name
        if parent_storage_id is not UNSET:
            properties["parentStorageId"] = parent_storage_id
        if parent_storage_schema is not UNSET:
            properties["parentStorageSchema"] = parent_storage_schema
        if project_id is not UNSET:
            properties["projectId"] = project_id
        if schema is not UNSET:
            properties["schema"] = schema
        if volume is not UNSET:
            properties["volume"] = volume
        if web_url is not UNSET:
            properties["webURL"] = web_url
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Well":
        barcode = d.get("barcode")

        contents = []
        for contents_item_data in d.get("contents") or []:
            contents_item = ContainerContent.from_dict(contents_item_data)

            contents.append(contents_item)

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

        name = d.get("name")

        parent_storage_id = d.get("parentStorageId")

        parent_storage_schema = None
        if d.get("parentStorageSchema") is not None:
            parent_storage_schema = SchemaSummary.from_dict(cast(Dict[str, Any], d.get("parentStorageSchema")))

        project_id = d.get("projectId")

        schema = None
        if d.get("schema") is not None:
            schema = SchemaSummary.from_dict(cast(Dict[str, Any], d.get("schema")))

        volume = None
        if d.get("volume") is not None:
            volume = d.get("volume")

        web_url = d.get("webURL")

        return Well(
            barcode=barcode,
            contents=contents,
            created_at=created_at,
            creator=creator,
            fields=fields,
            id=id,
            modified_at=modified_at,
            name=name,
            parent_storage_id=parent_storage_id,
            parent_storage_schema=parent_storage_schema,
            project_id=project_id,
            schema=schema,
            volume=volume,
            web_url=web_url,
        )
