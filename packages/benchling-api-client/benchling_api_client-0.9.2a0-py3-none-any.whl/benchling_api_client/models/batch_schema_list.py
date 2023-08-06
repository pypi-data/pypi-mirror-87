from typing import Any, Dict, List

import attr

from ..models.batch_schema import BatchSchema


@attr.s(auto_attribs=True)
class BatchSchemaList:
    """  """

    batch_schemas: List[BatchSchema]

    def to_dict(self) -> Dict[str, Any]:
        batch_schemas = []
        for batch_schemas_item_data in self.batch_schemas:
            batch_schemas_item = batch_schemas_item_data.to_dict()

            batch_schemas.append(batch_schemas_item)

        properties: Dict[str, Any] = dict()

        properties["batchSchemas"] = batch_schemas
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BatchSchemaList":
        batch_schemas = []
        for batch_schemas_item_data in d["batchSchemas"]:
            batch_schemas_item = BatchSchema.from_dict(batch_schemas_item_data)

            batch_schemas.append(batch_schemas_item)

        return BatchSchemaList(
            batch_schemas=batch_schemas,
        )
