from typing import Any, Dict

import attr

from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary


@attr.s(auto_attribs=True)
class Location:
    """  """

    id: str
    barcode: str
    created_at: str
    creator: UserSummary
    fields: Dict[Any, Any]
    modified_at: str
    name: str
    parent_storage_id: str
    schema: SchemaSummary
    web_url: str

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        barcode = self.barcode
        created_at = self.created_at
        creator = self.creator.to_dict()

        fields = self.fields

        modified_at = self.modified_at
        name = self.name
        parent_storage_id = self.parent_storage_id
        schema = self.schema.to_dict()

        web_url = self.web_url

        properties: Dict[str, Any] = dict()

        properties["id"] = id
        properties["barcode"] = barcode
        properties["createdAt"] = created_at
        properties["creator"] = creator
        properties["fields"] = fields
        properties["modifiedAt"] = modified_at
        properties["name"] = name
        properties["parentStorageId"] = parent_storage_id
        properties["schema"] = schema
        properties["webURL"] = web_url
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Location":
        id = d["id"]

        barcode = d["barcode"]

        created_at = d["createdAt"]

        creator = UserSummary.from_dict(d["creator"])

        fields = d["fields"]

        modified_at = d["modifiedAt"]

        name = d["name"]

        parent_storage_id = d["parentStorageId"]

        schema = SchemaSummary.from_dict(d["schema"])

        web_url = d["webURL"]

        return Location(
            id=id,
            barcode=barcode,
            created_at=created_at,
            creator=creator,
            fields=fields,
            modified_at=modified_at,
            name=name,
            parent_storage_id=parent_storage_id,
            schema=schema,
            web_url=web_url,
        )
