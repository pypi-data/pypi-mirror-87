from typing import Any, Dict, List, Optional, cast

import attr

from ..models.schema_field import SchemaField
from ..models.type123 import Type123
from ..types import UNSET


@attr.s(auto_attribs=True)
class EntrySchemaDetailed:
    """  """

    id: Optional[str] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    prefix: Optional[str] = cast(None, UNSET)
    registry_id: Optional[str] = cast(None, UNSET)
    field_definitions: Optional[List[SchemaField]] = cast(None, UNSET)
    type: Optional[Type123] = cast(None, UNSET)
    organization: Optional[Dict[Any, Any]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        prefix = self.prefix
        registry_id = self.registry_id
        if self.field_definitions is None:
            field_definitions = None
        elif self.field_definitions is UNSET:
            field_definitions = UNSET
        else:
            field_definitions = []
            for field_definitions_item_data in self.field_definitions:
                field_definitions_item = field_definitions_item_data.to_dict()

                field_definitions.append(field_definitions_item)

        if self.type is UNSET:
            type = UNSET
        else:
            type = self.type.value if self.type else None

        if self.organization is UNSET:
            organization = UNSET
        else:
            organization = self.organization if self.organization else None

        properties: Dict[str, Any] = dict()

        if id is not UNSET:
            properties["id"] = id
        if name is not UNSET:
            properties["name"] = name
        if prefix is not UNSET:
            properties["prefix"] = prefix
        if registry_id is not UNSET:
            properties["registryId"] = registry_id
        if field_definitions is not UNSET:
            properties["fieldDefinitions"] = field_definitions
        if type is not UNSET:
            properties["type"] = type
        if organization is not UNSET:
            properties["organization"] = organization
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EntrySchemaDetailed":
        id = d.get("id")

        name = d.get("name")

        prefix = d.get("prefix")

        registry_id = d.get("registryId")

        field_definitions = []
        for field_definitions_item_data in d.get("fieldDefinitions") or []:
            field_definitions_item = SchemaField.from_dict(field_definitions_item_data)

            field_definitions.append(field_definitions_item)

        type = None
        if d.get("type") is not None:
            type = Type123(d.get("type"))

        organization = None
        if d.get("organization") is not None:
            organization = d.get("organization")

        return EntrySchemaDetailed(
            id=id,
            name=name,
            prefix=prefix,
            registry_id=registry_id,
            field_definitions=field_definitions,
            type=type,
            organization=organization,
        )
