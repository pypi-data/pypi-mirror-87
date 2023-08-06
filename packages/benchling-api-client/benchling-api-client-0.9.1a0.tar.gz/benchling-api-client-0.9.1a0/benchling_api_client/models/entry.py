import datetime
from typing import Any, Dict, List, Optional, cast

import attr
from dateutil.parser import isoparse

from ..models.archive_record import ArchiveRecord
from ..models.entry_day import EntryDay
from ..models.entry_schema import EntrySchema
from ..models.fields import Fields
from ..models.user_summary import UserSummary
from ..types import UNSET


@attr.s(auto_attribs=True)
class Entry:
    """  """

    id: Optional[str] = cast(None, UNSET)
    archive_record: Optional[ArchiveRecord] = cast(None, UNSET)
    authors: Optional[List[UserSummary]] = cast(None, UNSET)
    created_at: Optional[datetime.datetime] = cast(None, UNSET)
    creator: Optional[UserSummary] = cast(None, UNSET)
    custom_fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    days: Optional[List[EntryDay]] = cast(None, UNSET)
    display_id: Optional[str] = cast(None, UNSET)
    fields: Optional[Fields] = cast(None, UNSET)
    folder_id: Optional[str] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    modified_at: Optional[str] = cast(None, UNSET)
    review_record: Optional[Dict[Any, Any]] = cast(None, UNSET)
    schema: Optional[EntrySchema] = cast(None, UNSET)
    web_url: Optional[str] = cast(None, UNSET)
    api_url: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
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

        if self.creator is UNSET:
            creator = UNSET
        else:
            creator = self.creator.to_dict() if self.creator else None

        if self.custom_fields is UNSET:
            custom_fields = UNSET
        else:
            custom_fields = self.custom_fields if self.custom_fields else None

        if self.days is None:
            days = None
        elif self.days is UNSET:
            days = UNSET
        else:
            days = []
            for days_item_data in self.days:
                days_item = days_item_data.to_dict()

                days.append(days_item)

        display_id = self.display_id
        if self.fields is UNSET:
            fields = UNSET
        else:
            fields = self.fields.to_dict() if self.fields else None

        folder_id = self.folder_id
        name = self.name
        modified_at = self.modified_at
        if self.review_record is UNSET:
            review_record = UNSET
        else:
            review_record = self.review_record if self.review_record else None

        if self.schema is UNSET:
            schema = UNSET
        else:
            schema = self.schema.to_dict() if self.schema else None

        web_url = self.web_url
        api_url = self.api_url

        properties: Dict[str, Any] = dict()

        if id is not UNSET:
            properties["id"] = id
        if archive_record is not UNSET:
            properties["archiveRecord"] = archive_record
        if authors is not UNSET:
            properties["authors"] = authors
        if created_at is not UNSET:
            properties["createdAt"] = created_at
        if creator is not UNSET:
            properties["creator"] = creator
        if custom_fields is not UNSET:
            properties["customFields"] = custom_fields
        if days is not UNSET:
            properties["days"] = days
        if display_id is not UNSET:
            properties["displayId"] = display_id
        if fields is not UNSET:
            properties["fields"] = fields
        if folder_id is not UNSET:
            properties["folderId"] = folder_id
        if name is not UNSET:
            properties["name"] = name
        if modified_at is not UNSET:
            properties["modifiedAt"] = modified_at
        if review_record is not UNSET:
            properties["reviewRecord"] = review_record
        if schema is not UNSET:
            properties["schema"] = schema
        if web_url is not UNSET:
            properties["webURL"] = web_url
        if api_url is not UNSET:
            properties["apiURL"] = api_url
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Entry":
        id = d.get("id")

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

        creator = None
        if d.get("creator") is not None:
            creator = UserSummary.from_dict(cast(Dict[str, Any], d.get("creator")))

        custom_fields = None
        if d.get("customFields") is not None:
            custom_fields = d.get("customFields")

        days = []
        for days_item_data in d.get("days") or []:
            days_item = EntryDay.from_dict(days_item_data)

            days.append(days_item)

        display_id = d.get("displayId")

        fields = None
        if d.get("fields") is not None:
            fields = Fields.from_dict(cast(Dict[str, Any], d.get("fields")))

        folder_id = d.get("folderId")

        name = d.get("name")

        modified_at = d.get("modifiedAt")

        review_record = None
        if d.get("reviewRecord") is not None:
            review_record = d.get("reviewRecord")

        schema = None
        if d.get("schema") is not None:
            schema = EntrySchema.from_dict(cast(Dict[str, Any], d.get("schema")))

        web_url = d.get("webURL")

        api_url = d.get("apiURL")

        return Entry(
            id=id,
            archive_record=archive_record,
            authors=authors,
            created_at=created_at,
            creator=creator,
            custom_fields=custom_fields,
            days=days,
            display_id=display_id,
            fields=fields,
            folder_id=folder_id,
            name=name,
            modified_at=modified_at,
            review_record=review_record,
            schema=schema,
            web_url=web_url,
            api_url=api_url,
        )
