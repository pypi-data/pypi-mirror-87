from typing import Any, Dict, List, Optional, cast

import attr

from ..models.schema_field import SchemaField
from ..models.type12 import Type12
from ..types import UNSET


@attr.s(auto_attribs=True)
class RequestSchema:
    """  """

    id: Optional[str] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    field_definitions: Optional[List[SchemaField]] = cast(None, UNSET)
    type: Optional[Type12] = cast(None, UNSET)
    system_name: Optional[str] = cast(None, UNSET)
    organization: Optional[Dict[Any, Any]] = cast(None, UNSET)
    sql_id: Optional[str] = cast(None, UNSET)
    derived_from: Optional[str] = cast(None, UNSET)

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
        if self.organization is UNSET:
            organization = UNSET
        else:
            organization = self.organization if self.organization else None

        sql_id = self.sql_id
        derived_from = self.derived_from

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
        if organization is not UNSET:
            properties["organization"] = organization
        if sql_id is not UNSET:
            properties["sqlId"] = sql_id
        if derived_from is not UNSET:
            properties["derivedFrom"] = derived_from
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RequestSchema":
        id = d.get("id")

        name = d.get("name")

        field_definitions = []
        for field_definitions_item_data in d.get("fieldDefinitions") or []:
            field_definitions_item = SchemaField.from_dict(field_definitions_item_data)

            field_definitions.append(field_definitions_item)

        type = None
        if d.get("type") is not None:
            type = Type12(d.get("type"))

        system_name = d.get("systemName")

        organization = None
        if d.get("organization") is not None:
            organization = d.get("organization")

        sql_id = d.get("sqlId")

        derived_from = d.get("derivedFrom")

        return RequestSchema(
            id=id,
            name=name,
            field_definitions=field_definitions,
            type=type,
            system_name=system_name,
            organization=organization,
            sql_id=sql_id,
            derived_from=derived_from,
        )
