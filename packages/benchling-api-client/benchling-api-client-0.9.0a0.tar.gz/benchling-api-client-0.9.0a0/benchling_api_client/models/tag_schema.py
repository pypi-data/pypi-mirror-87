from typing import Any, Dict, List, Optional, cast

import attr

from ..models.schema_field import SchemaField
from ..types import UNSET


@attr.s(auto_attribs=True)
class TagSchema:
    """  """

    constraint: Optional[Dict[Any, Any]] = cast(None, UNSET)
    containable_type: Optional[str] = cast(None, UNSET)
    id: Optional[str] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    field_definitions: Optional[List[SchemaField]] = cast(None, UNSET)
    type: Optional[str] = cast(None, UNSET)
    prefix: Optional[str] = cast(None, UNSET)
    registry_id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.constraint is UNSET:
            constraint = UNSET
        else:
            constraint = self.constraint if self.constraint else None

        containable_type = self.containable_type
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

        if constraint is not UNSET:
            properties["constraint"] = constraint
        if containable_type is not UNSET:
            properties["containableType"] = containable_type
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
    def from_dict(d: Dict[str, Any]) -> "TagSchema":
        constraint = None
        if d.get("constraint") is not None:
            constraint = d.get("constraint")

        containable_type = d.get("containableType")

        id = d.get("id")

        name = d.get("name")

        field_definitions = []
        for field_definitions_item_data in d.get("fieldDefinitions") or []:
            field_definitions_item = SchemaField.from_dict(field_definitions_item_data)

            field_definitions.append(field_definitions_item)

        type = d.get("type")

        prefix = d.get("prefix")

        registry_id = d.get("registryId")

        return TagSchema(
            constraint=constraint,
            containable_type=containable_type,
            id=id,
            name=name,
            field_definitions=field_definitions,
            type=type,
            prefix=prefix,
            registry_id=registry_id,
        )
