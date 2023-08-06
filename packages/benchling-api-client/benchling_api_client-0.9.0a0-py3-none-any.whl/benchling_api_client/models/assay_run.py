from typing import Any, Dict, Optional, cast

import attr

from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary
from ..types import UNSET


@attr.s(auto_attribs=True)
class AssayRun:
    """  """

    id: Optional[str] = cast(None, UNSET)
    project_id: Optional[str] = cast(None, UNSET)
    created_at: Optional[str] = cast(None, UNSET)
    creator: Optional[UserSummary] = cast(None, UNSET)
    schema: Optional[SchemaSummary] = cast(None, UNSET)
    fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    entry_id: Optional[str] = cast(None, UNSET)
    is_reviewed: Optional[bool] = cast(None, UNSET)
    validation_schema: Optional[str] = cast(None, UNSET)
    validation_comment: Optional[str] = cast(None, UNSET)
    api_url: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        project_id = self.project_id
        created_at = self.created_at
        if self.creator is UNSET:
            creator = UNSET
        else:
            creator = self.creator.to_dict() if self.creator else None

        if self.schema is UNSET:
            schema = UNSET
        else:
            schema = self.schema.to_dict() if self.schema else None

        if self.fields is UNSET:
            fields = UNSET
        else:
            fields = self.fields if self.fields else None

        entry_id = self.entry_id
        is_reviewed = self.is_reviewed
        validation_schema = self.validation_schema
        validation_comment = self.validation_comment
        api_url = self.api_url

        properties: Dict[str, Any] = dict()

        if id is not UNSET:
            properties["id"] = id
        if project_id is not UNSET:
            properties["projectId"] = project_id
        if created_at is not UNSET:
            properties["createdAt"] = created_at
        if creator is not UNSET:
            properties["creator"] = creator
        if schema is not UNSET:
            properties["schema"] = schema
        if fields is not UNSET:
            properties["fields"] = fields
        if entry_id is not UNSET:
            properties["entryId"] = entry_id
        if is_reviewed is not UNSET:
            properties["isReviewed"] = is_reviewed
        if validation_schema is not UNSET:
            properties["validationSchema"] = validation_schema
        if validation_comment is not UNSET:
            properties["validationComment"] = validation_comment
        if api_url is not UNSET:
            properties["apiURL"] = api_url
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AssayRun":
        id = d.get("id")

        project_id = d.get("projectId")

        created_at = d.get("createdAt")

        creator = None
        if d.get("creator") is not None:
            creator = UserSummary.from_dict(cast(Dict[str, Any], d.get("creator")))

        schema = None
        if d.get("schema") is not None:
            schema = SchemaSummary.from_dict(cast(Dict[str, Any], d.get("schema")))

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        entry_id = d.get("entryId")

        is_reviewed = d.get("isReviewed")

        validation_schema = d.get("validationSchema")

        validation_comment = d.get("validationComment")

        api_url = d.get("apiURL")

        return AssayRun(
            id=id,
            project_id=project_id,
            created_at=created_at,
            creator=creator,
            schema=schema,
            fields=fields,
            entry_id=entry_id,
            is_reviewed=is_reviewed,
            validation_schema=validation_schema,
            validation_comment=validation_comment,
            api_url=api_url,
        )
