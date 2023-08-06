from typing import Any, Dict, List

import attr

from ..models.schema import Schema


@attr.s(auto_attribs=True)
class PaginatedLocationSchemaList:
    """  """

    next_token: str
    location_schemas: List[Schema]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        location_schemas = []
        for location_schemas_item_data in self.location_schemas:
            location_schemas_item = location_schemas_item_data.to_dict()

            location_schemas.append(location_schemas_item)

        properties: Dict[str, Any] = dict()

        properties["nextToken"] = next_token
        properties["locationSchemas"] = location_schemas
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PaginatedLocationSchemaList":
        next_token = d["nextToken"]

        location_schemas = []
        for location_schemas_item_data in d["locationSchemas"]:
            location_schemas_item = Schema.from_dict(location_schemas_item_data)

            location_schemas.append(location_schemas_item)

        return PaginatedLocationSchemaList(
            next_token=next_token,
            location_schemas=location_schemas,
        )
