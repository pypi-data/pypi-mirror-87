import datetime
from typing import Any, Dict, Optional, cast

import attr
from dateutil.parser import isoparse

from ..models.archive_record import ArchiveRecord
from ..models.assay_result_schema import AssayResultSchema
from ..models.user_summary import UserSummary
from ..types import UNSET


@attr.s(auto_attribs=True)
class AssayResult:
    """  """

    id: str
    schema: AssayResultSchema
    fields: Dict[Any, Any]
    project_id: Optional[str] = cast(None, UNSET)
    created_at: Optional[datetime.datetime] = cast(None, UNSET)
    creator: Optional[UserSummary] = cast(None, UNSET)
    entry_id: Optional[str] = cast(None, UNSET)
    is_reviewed: Optional[bool] = cast(None, UNSET)
    field_validation: Optional[Dict[Any, Any]] = cast(None, UNSET)
    validation_status: Optional[str] = cast(None, UNSET)
    validation_comment: Optional[str] = cast(None, UNSET)
    archive_record: Optional[ArchiveRecord] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        schema = self.schema.to_dict()

        fields = self.fields

        project_id = self.project_id
        if self.created_at is UNSET:
            created_at = UNSET
        else:
            created_at = self.created_at.isoformat() if self.created_at else None

        if self.creator is UNSET:
            creator = UNSET
        else:
            creator = self.creator.to_dict() if self.creator else None

        entry_id = self.entry_id
        is_reviewed = self.is_reviewed
        if self.field_validation is UNSET:
            field_validation = UNSET
        else:
            field_validation = self.field_validation if self.field_validation else None

        validation_status = self.validation_status
        validation_comment = self.validation_comment
        if self.archive_record is UNSET:
            archive_record = UNSET
        else:
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        properties: Dict[str, Any] = dict()

        properties["id"] = id
        properties["schema"] = schema
        properties["fields"] = fields
        if project_id is not UNSET:
            properties["projectId"] = project_id
        if created_at is not UNSET:
            properties["createdAt"] = created_at
        if creator is not UNSET:
            properties["creator"] = creator
        if entry_id is not UNSET:
            properties["entryId"] = entry_id
        if is_reviewed is not UNSET:
            properties["isReviewed"] = is_reviewed
        if field_validation is not UNSET:
            properties["fieldValidation"] = field_validation
        if validation_status is not UNSET:
            properties["validationStatus"] = validation_status
        if validation_comment is not UNSET:
            properties["validationComment"] = validation_comment
        if archive_record is not UNSET:
            properties["archiveRecord"] = archive_record
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AssayResult":
        id = d["id"]

        schema = AssayResultSchema.from_dict(d["schema"])

        fields = d["fields"]

        project_id = d.get("projectId")

        created_at = None
        if d.get("createdAt") is not None:
            created_at = isoparse(cast(str, d.get("createdAt")))

        creator = None
        if d.get("creator") is not None:
            creator = UserSummary.from_dict(cast(Dict[str, Any], d.get("creator")))

        entry_id = d.get("entryId")

        is_reviewed = d.get("isReviewed")

        field_validation = None
        if d.get("fieldValidation") is not None:
            field_validation = d.get("fieldValidation")

        validation_status = d.get("validationStatus")

        validation_comment = d.get("validationComment")

        archive_record = None
        if d.get("archiveRecord") is not None:
            archive_record = ArchiveRecord.from_dict(cast(Dict[str, Any], d.get("archiveRecord")))

        return AssayResult(
            id=id,
            schema=schema,
            fields=fields,
            project_id=project_id,
            created_at=created_at,
            creator=creator,
            entry_id=entry_id,
            is_reviewed=is_reviewed,
            field_validation=field_validation,
            validation_status=validation_status,
            validation_comment=validation_comment,
            archive_record=archive_record,
        )
