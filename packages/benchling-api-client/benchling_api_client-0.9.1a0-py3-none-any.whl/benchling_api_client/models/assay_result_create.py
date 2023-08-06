from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class AssayResultCreate:
    """  """

    schema_id: str
    fields: Dict[Any, Any]
    id: Optional[str] = cast(None, UNSET)
    project_id: Optional[str] = cast(None, UNSET)
    field_validation: Optional[Dict[Any, Any]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        schema_id = self.schema_id
        fields = self.fields

        id = self.id
        project_id = self.project_id
        if self.field_validation is UNSET:
            field_validation = UNSET
        else:
            field_validation = self.field_validation if self.field_validation else None

        properties: Dict[str, Any] = dict()

        properties["schemaId"] = schema_id
        properties["fields"] = fields
        if id is not UNSET:
            properties["id"] = id
        if project_id is not UNSET:
            properties["projectId"] = project_id
        if field_validation is not UNSET:
            properties["fieldValidation"] = field_validation
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AssayResultCreate":
        schema_id = d["schemaId"]

        fields = d["fields"]

        id = d.get("id")

        project_id = d.get("projectId")

        field_validation = None
        if d.get("fieldValidation") is not None:
            field_validation = d.get("fieldValidation")

        return AssayResultCreate(
            schema_id=schema_id,
            fields=fields,
            id=id,
            project_id=project_id,
            field_validation=field_validation,
        )
