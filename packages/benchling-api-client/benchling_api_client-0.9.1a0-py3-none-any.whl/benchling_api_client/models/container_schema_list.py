from typing import Any, Dict, List

import attr

from ..models.schema import Schema


@attr.s(auto_attribs=True)
class ContainerSchemaList:
    """  """

    container_schemas: List[Schema]

    def to_dict(self) -> Dict[str, Any]:
        container_schemas = []
        for container_schemas_item_data in self.container_schemas:
            container_schemas_item = container_schemas_item_data.to_dict()

            container_schemas.append(container_schemas_item)

        properties: Dict[str, Any] = dict()

        properties["containerSchemas"] = container_schemas
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ContainerSchemaList":
        container_schemas = []
        for container_schemas_item_data in d["containerSchemas"]:
            container_schemas_item = Schema.from_dict(container_schemas_item_data)

            container_schemas.append(container_schemas_item)

        return ContainerSchemaList(
            container_schemas=container_schemas,
        )
