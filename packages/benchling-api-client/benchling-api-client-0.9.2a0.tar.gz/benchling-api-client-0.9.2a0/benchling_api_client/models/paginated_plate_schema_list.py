from typing import Any, Dict, List

import attr

from ..models.plate_schema import PlateSchema


@attr.s(auto_attribs=True)
class PaginatedPlateSchemaList:
    """  """

    next_token: str
    plate_schemas: List[PlateSchema]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        plate_schemas = []
        for plate_schemas_item_data in self.plate_schemas:
            plate_schemas_item = plate_schemas_item_data.to_dict()

            plate_schemas.append(plate_schemas_item)

        properties: Dict[str, Any] = dict()

        properties["nextToken"] = next_token
        properties["plateSchemas"] = plate_schemas
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PaginatedPlateSchemaList":
        next_token = d["nextToken"]

        plate_schemas = []
        for plate_schemas_item_data in d["plateSchemas"]:
            plate_schemas_item = PlateSchema.from_dict(plate_schemas_item_data)

            plate_schemas.append(plate_schemas_item)

        return PaginatedPlateSchemaList(
            next_token=next_token,
            plate_schemas=plate_schemas,
        )
