from typing import Any, Dict, List, Optional, cast

import attr

from ..models.schema_field import SchemaField
from ..types import UNSET


@attr.s(auto_attribs=True)
class BoxSchema:
    """  """

    height: Optional[float] = cast(None, UNSET)
    width: Optional[float] = cast(None, UNSET)
    container_schema: Optional[Dict[Any, Any]] = cast(None, UNSET)
    id: Optional[str] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    field_definitions: Optional[List[SchemaField]] = cast(None, UNSET)
    type: Optional[str] = cast(None, UNSET)
    prefix: Optional[str] = cast(None, UNSET)
    registry_id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        height = self.height
        width = self.width
        if self.container_schema is UNSET:
            container_schema = UNSET
        else:
            container_schema = self.container_schema if self.container_schema else None

        id = self.id
        name = self.name
        if self.field_definitions is None:
            field_definitions = None
        elif self.field_definitions is UNSET:
            field_definitions = UNSET
        else:
            field_definitions = []
            for field_definitions_item_data in self.field_definitions:
                field_definitions_item = field_definitions_item_data.to_dict()

                field_definitions.append(field_definitions_item)

        type = self.type
        prefix = self.prefix
        registry_id = self.registry_id

        properties: Dict[str, Any] = dict()

        if height is not UNSET:
            properties["height"] = height
        if width is not UNSET:
            properties["width"] = width
        if container_schema is not UNSET:
            properties["containerSchema"] = container_schema
        if id is not UNSET:
            properties["id"] = id
        if name is not UNSET:
            properties["name"] = name
        if field_definitions is not UNSET:
            properties["fieldDefinitions"] = field_definitions
        if type is not UNSET:
            properties["type"] = type
        if prefix is not UNSET:
            properties["prefix"] = prefix
        if registry_id is not UNSET:
            properties["registryId"] = registry_id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BoxSchema":
        height = d.get("height")

        width = d.get("width")

        container_schema = None
        if d.get("containerSchema") is not None:
            container_schema = d.get("containerSchema")

        id = d.get("id")

        name = d.get("name")

        field_definitions = []
        for field_definitions_item_data in d.get("fieldDefinitions") or []:
            field_definitions_item = SchemaField.from_dict(field_definitions_item_data)

            field_definitions.append(field_definitions_item)

        type = d.get("type")

        prefix = d.get("prefix")

        registry_id = d.get("registryId")

        return BoxSchema(
            height=height,
            width=width,
            container_schema=container_schema,
            id=id,
            name=name,
            field_definitions=field_definitions,
            type=type,
            prefix=prefix,
            registry_id=registry_id,
        )
