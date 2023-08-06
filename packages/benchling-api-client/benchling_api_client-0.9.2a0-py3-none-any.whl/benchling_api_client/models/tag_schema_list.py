from typing import Any, Dict, List

import attr

from ..models.tag_schema import TagSchema


@attr.s(auto_attribs=True)
class TagSchemaList:
    """  """

    entity_schemas: List[TagSchema]

    def to_dict(self) -> Dict[str, Any]:
        entity_schemas = []
        for entity_schemas_item_data in self.entity_schemas:
            entity_schemas_item = entity_schemas_item_data.to_dict()

            entity_schemas.append(entity_schemas_item)

        properties: Dict[str, Any] = dict()

        properties["entitySchemas"] = entity_schemas
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "TagSchemaList":
        entity_schemas = []
        for entity_schemas_item_data in d["entitySchemas"]:
            entity_schemas_item = TagSchema.from_dict(entity_schemas_item_data)

            entity_schemas.append(entity_schemas_item)

        return TagSchemaList(
            entity_schemas=entity_schemas,
        )
