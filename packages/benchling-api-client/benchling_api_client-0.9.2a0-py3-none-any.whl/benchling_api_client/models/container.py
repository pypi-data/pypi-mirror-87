import datetime
from typing import Any, Dict, List, Optional, cast

import attr
from dateutil.parser import isoparse

from ..models.archive_record import ArchiveRecord
from ..models.checkout_record import CheckoutRecord
from ..models.container_content import ContainerContent
from ..models.measurement import Measurement
from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary
from ..types import UNSET


@attr.s(auto_attribs=True)
class Container:
    """  """

    id: str
    name: str
    barcode: str
    checkout_record: CheckoutRecord
    contents: List[ContainerContent]
    created_at: datetime.datetime
    creator: UserSummary
    fields: Dict[Any, Any]
    modified_at: datetime.datetime
    parent_storage_id: str
    parent_storage_schema: SchemaSummary
    project_id: Optional[str]
    schema: SchemaSummary
    volume: Measurement
    web_url: str
    archive_record: Optional[ArchiveRecord] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        barcode = self.barcode
        checkout_record = self.checkout_record.to_dict()

        contents = []
        for contents_item_data in self.contents:
            contents_item = contents_item_data.to_dict()

            contents.append(contents_item)

        created_at = self.created_at.isoformat()

        creator = self.creator.to_dict()

        fields = self.fields

        modified_at = self.modified_at.isoformat()

        parent_storage_id = self.parent_storage_id
        parent_storage_schema = self.parent_storage_schema.to_dict()

        project_id = self.project_id
        schema = self.schema.to_dict()

        volume = self.volume.to_dict()

        web_url = self.web_url
        if self.archive_record is UNSET:
            archive_record = UNSET
        else:
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        properties: Dict[str, Any] = dict()

        properties["id"] = id
        properties["name"] = name
        properties["barcode"] = barcode
        properties["checkoutRecord"] = checkout_record
        properties["contents"] = contents
        properties["createdAt"] = created_at
        properties["creator"] = creator
        properties["fields"] = fields
        properties["modifiedAt"] = modified_at
        properties["parentStorageId"] = parent_storage_id
        properties["parentStorageSchema"] = parent_storage_schema
        properties["projectId"] = project_id
        properties["schema"] = schema
        properties["volume"] = volume
        properties["webURL"] = web_url
        if archive_record is not UNSET:
            properties["archiveRecord"] = archive_record
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Container":
        id = d["id"]

        name = d["name"]

        barcode = d["barcode"]

        checkout_record = CheckoutRecord.from_dict(d["checkoutRecord"])

        contents = []
        for contents_item_data in d["contents"]:
            contents_item = ContainerContent.from_dict(contents_item_data)

            contents.append(contents_item)

        created_at = isoparse(d["createdAt"])

        creator = UserSummary.from_dict(d["creator"])

        fields = d["fields"]

        modified_at = isoparse(d["modifiedAt"])

        parent_storage_id = d["parentStorageId"]

        parent_storage_schema = SchemaSummary.from_dict(d["parentStorageSchema"])

        project_id = d["projectId"]

        schema = SchemaSummary.from_dict(d["schema"])

        volume = Measurement.from_dict(d["volume"])

        web_url = d["webURL"]

        archive_record = None
        if d.get("archiveRecord") is not None:
            archive_record = ArchiveRecord.from_dict(cast(Dict[str, Any], d.get("archiveRecord")))

        return Container(
            id=id,
            name=name,
            barcode=barcode,
            checkout_record=checkout_record,
            contents=contents,
            created_at=created_at,
            creator=creator,
            fields=fields,
            modified_at=modified_at,
            parent_storage_id=parent_storage_id,
            parent_storage_schema=parent_storage_schema,
            project_id=project_id,
            schema=schema,
            volume=volume,
            web_url=web_url,
            archive_record=archive_record,
        )
