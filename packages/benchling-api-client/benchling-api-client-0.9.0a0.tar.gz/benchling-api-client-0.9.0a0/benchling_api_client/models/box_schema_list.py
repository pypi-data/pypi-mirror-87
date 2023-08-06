from typing import Any, Dict, List

import attr

from ..models.box_schema import BoxSchema


@attr.s(auto_attribs=True)
class BoxSchemaList:
    """  """

    box_schemas: List[BoxSchema]

    def to_dict(self) -> Dict[str, Any]:
        box_schemas = []
        for box_schemas_item_data in self.box_schemas:
            box_schemas_item = box_schemas_item_data.to_dict()

            box_schemas.append(box_schemas_item)

        properties: Dict[str, Any] = dict()

        properties["boxSchemas"] = box_schemas
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BoxSchemaList":
        box_schemas = []
        for box_schemas_item_data in d["boxSchemas"]:
            box_schemas_item = BoxSchema.from_dict(box_schemas_item_data)

            box_schemas.append(box_schemas_item)

        return BoxSchemaList(
            box_schemas=box_schemas,
        )
