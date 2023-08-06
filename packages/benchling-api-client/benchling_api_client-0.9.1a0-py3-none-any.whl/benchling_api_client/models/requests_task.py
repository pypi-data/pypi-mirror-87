from typing import Any, Dict, List, Optional, cast

import attr

from ..models.schema_summary import SchemaSummary
from ..types import UNSET


@attr.s(auto_attribs=True)
class RequestsTask:
    """A request task."""

    schema: Optional[SchemaSummary] = cast(None, UNSET)
    id: Optional[str] = cast(None, UNSET)
    fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    sample_group_ids: Optional[List[str]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.schema is UNSET:
            schema = UNSET
        else:
            schema = self.schema.to_dict() if self.schema else None

        id = self.id
        if self.fields is UNSET:
            fields = UNSET
        else:
            fields = self.fields if self.fields else None

        if self.sample_group_ids is None:
            sample_group_ids = None
        elif self.sample_group_ids is UNSET:
            sample_group_ids = UNSET
        else:
            sample_group_ids = self.sample_group_ids

        properties: Dict[str, Any] = dict()

        if schema is not UNSET:
            properties["schema"] = schema
        if id is not UNSET:
            properties["id"] = id
        if fields is not UNSET:
            properties["fields"] = fields
        if sample_group_ids is not UNSET:
            properties["sampleGroupIds"] = sample_group_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RequestsTask":
        schema = None
        if d.get("schema") is not None:
            schema = SchemaSummary.from_dict(cast(Dict[str, Any], d.get("schema")))

        id = d.get("id")

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        sample_group_ids = d.get("sampleGroupIds")

        return RequestsTask(
            schema=schema,
            id=id,
            fields=fields,
            sample_group_ids=sample_group_ids,
        )
