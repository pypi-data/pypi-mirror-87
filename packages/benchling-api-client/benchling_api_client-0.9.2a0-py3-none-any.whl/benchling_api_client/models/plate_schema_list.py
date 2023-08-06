from typing import Any, Dict, List

import attr

from ..models.plate_schema import PlateSchema


@attr.s(auto_attribs=True)
class PlateSchemaList:
    """  """

    plate_schemas: List[PlateSchema]

    def to_dict(self) -> Dict[str, Any]:
        plate_schemas = []
        for plate_schemas_item_data in self.plate_schemas:
            plate_schemas_item = plate_schemas_item_data.to_dict()

            plate_schemas.append(plate_schemas_item)

        properties: Dict[str, Any] = dict()

        properties["plateSchemas"] = plate_schemas
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PlateSchemaList":
        plate_schemas = []
        for plate_schemas_item_data in d["plateSchemas"]:
            plate_schemas_item = PlateSchema.from_dict(plate_schemas_item_data)

            plate_schemas.append(plate_schemas_item)

        return PlateSchemaList(
            plate_schemas=plate_schemas,
        )
