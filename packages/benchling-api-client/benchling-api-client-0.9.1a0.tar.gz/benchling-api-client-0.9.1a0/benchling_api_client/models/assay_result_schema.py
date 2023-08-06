from typing import Any, Dict, List, Optional, cast

import attr

from ..models.schema_field import SchemaField
from ..models.type1 import Type1
from ..types import UNSET


@attr.s(auto_attribs=True)
class AssayResultSchema:
    """  """

    id: Optional[str] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    field_definitions: Optional[List[SchemaField]] = cast(None, UNSET)
    type: Optional[Type1] = cast(None, UNSET)
    system_name: Optional[str] = cast(None, UNSET)
    derived_from: Optional[str] = cast(None, UNSET)
    organization: Optional[Dict[Any, Any]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
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

        if self.type is UNSET:
            type = UNSET
        else:
            type = self.type.value if self.type else None

        system_name = self.system_name
        derived_from = self.derived_from
        if self.organization is UNSET:
            organization = UNSET
        else:
            organization = self.organization if self.organization else None

        properties: Dict[str, Any] = dict()

        if id is not UNSET:
            properties["id"] = id
        if name is not UNSET:
            properties["name"] = name
        if field_definitions is not UNSET:
            properties["fieldDefinitions"] = field_definitions
        if type is not UNSET:
            properties["type"] = type
        if system_name is not UNSET:
            properties["systemName"] = system_name
        if derived_from is not UNSET:
            properties["derivedFrom"] = derived_from
        if organization is not UNSET:
            properties["organization"] = organization
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AssayResultSchema":
        id = d.get("id")

        name = d.get("name")

        field_definitions = []
        for field_definitions_item_data in d.get("fieldDefinitions") or []:
            field_definitions_item = SchemaField.from_dict(field_definitions_item_data)

            field_definitions.append(field_definitions_item)

        type = None
        if d.get("type") is not None:
            type = Type1(d.get("type"))

        system_name = d.get("systemName")

        derived_from = d.get("derivedFrom")

        organization = None
        if d.get("organization") is not None:
            organization = d.get("organization")

        return AssayResultSchema(
            id=id,
            name=name,
            field_definitions=field_definitions,
            type=type,
            system_name=system_name,
            derived_from=derived_from,
            organization=organization,
        )
