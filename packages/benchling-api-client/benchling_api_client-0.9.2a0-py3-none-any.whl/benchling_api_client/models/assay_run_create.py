from typing import Any, Dict, Optional, cast

import attr

from ..models.validation_status1 import ValidationStatus1
from ..types import UNSET


@attr.s(auto_attribs=True)
class AssayRunCreate:
    """  """

    schema_id: str
    fields: Dict[Any, Any]
    id: Optional[str] = cast(None, UNSET)
    project_id: Optional[str] = cast(None, UNSET)
    validation_status: Optional[ValidationStatus1] = cast(None, UNSET)
    validation_comment: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        schema_id = self.schema_id
        fields = self.fields

        id = self.id
        project_id = self.project_id
        if self.validation_status is UNSET:
            validation_status = UNSET
        else:
            validation_status = self.validation_status.value if self.validation_status else None

        validation_comment = self.validation_comment

        properties: Dict[str, Any] = dict()

        properties["schemaId"] = schema_id
        properties["fields"] = fields
        if id is not UNSET:
            properties["id"] = id
        if project_id is not UNSET:
            properties["projectId"] = project_id
        if validation_status is not UNSET:
            properties["validationStatus"] = validation_status
        if validation_comment is not UNSET:
            properties["validationComment"] = validation_comment
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AssayRunCreate":
        schema_id = d["schemaId"]

        fields = d["fields"]

        id = d.get("id")

        project_id = d.get("projectId")

        validation_status = None
        if d.get("validationStatus") is not None:
            validation_status = ValidationStatus1(d.get("validationStatus"))

        validation_comment = d.get("validationComment")

        return AssayRunCreate(
            schema_id=schema_id,
            fields=fields,
            id=id,
            project_id=project_id,
            validation_status=validation_status,
            validation_comment=validation_comment,
        )
