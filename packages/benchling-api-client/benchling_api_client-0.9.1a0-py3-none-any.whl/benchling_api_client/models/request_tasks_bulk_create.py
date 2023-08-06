from typing import Any, Dict, List, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class RequestTasksBulkCreate:
    """  """

    schema_id: str
    fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    sample_group_ids: Optional[List[str]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        schema_id = self.schema_id
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

        properties["schemaId"] = schema_id
        if fields is not UNSET:
            properties["fields"] = fields
        if sample_group_ids is not UNSET:
            properties["sampleGroupIds"] = sample_group_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RequestTasksBulkCreate":
        schema_id = d["schemaId"]

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        sample_group_ids = d.get("sampleGroupIds")

        return RequestTasksBulkCreate(
            schema_id=schema_id,
            fields=fields,
            sample_group_ids=sample_group_ids,
        )
