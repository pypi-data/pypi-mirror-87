from typing import Any, Dict, List

import attr

from ..models.batch_schema import BatchSchema


@attr.s(auto_attribs=True)
class PaginatedBatchSchemaList:
    """  """

    next_token: str
    batch_schemas: List[BatchSchema]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        batch_schemas = []
        for batch_schemas_item_data in self.batch_schemas:
            batch_schemas_item = batch_schemas_item_data.to_dict()

            batch_schemas.append(batch_schemas_item)

        properties: Dict[str, Any] = dict()

        properties["nextToken"] = next_token
        properties["batchSchemas"] = batch_schemas
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PaginatedBatchSchemaList":
        next_token = d["nextToken"]

        batch_schemas = []
        for batch_schemas_item_data in d["batchSchemas"]:
            batch_schemas_item = BatchSchema.from_dict(batch_schemas_item_data)

            batch_schemas.append(batch_schemas_item)

        return PaginatedBatchSchemaList(
            next_token=next_token,
            batch_schemas=batch_schemas,
        )
