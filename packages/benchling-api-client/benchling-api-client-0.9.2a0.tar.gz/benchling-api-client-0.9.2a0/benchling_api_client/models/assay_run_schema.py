from typing import Any, Dict, List, Optional, cast

import attr

from ..models.schema_field import SchemaField
from ..models.type import Type
from ..types import UNSET


@attr.s(auto_attribs=True)
class AssayRunSchema:
    """  """

    id: Optional[str] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    field_definitions: Optional[List[SchemaField]] = cast(None, UNSET)
    type: Optional[Type] = cast(None, UNSET)
    system_name: Optional[str] = cast(None, UNSET)
    derived_from: Optional[str] = cast(None, UNSET)
    automation_input_file_configs: Optional[List[Dict[Any, Any]]] = cast(None, UNSET)
    automation_output_file_configs: Optional[List[Dict[Any, Any]]] = cast(None, UNSET)
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
        if self.automation_input_file_configs is None:
            automation_input_file_configs = None
        elif self.automation_input_file_configs is UNSET:
            automation_input_file_configs = UNSET
        else:
            automation_input_file_configs = []
            for automation_input_file_configs_item_data in self.automation_input_file_configs:
                automation_input_file_configs_item = automation_input_file_configs_item_data

                automation_input_file_configs.append(automation_input_file_configs_item)

        if self.automation_output_file_configs is None:
            automation_output_file_configs = None
        elif self.automation_output_file_configs is UNSET:
            automation_output_file_configs = UNSET
        else:
            automation_output_file_configs = []
            for automation_output_file_configs_item_data in self.automation_output_file_configs:
                automation_output_file_configs_item = automation_output_file_configs_item_data

                automation_output_file_configs.append(automation_output_file_configs_item)

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
        if automation_input_file_configs is not UNSET:
            properties["automationInputFileConfigs"] = automation_input_file_configs
        if automation_output_file_configs is not UNSET:
            properties["automationOutputFileConfigs"] = automation_output_file_configs
        if organization is not UNSET:
            properties["organization"] = organization
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AssayRunSchema":
        id = d.get("id")

        name = d.get("name")

        field_definitions = []
        for field_definitions_item_data in d.get("fieldDefinitions") or []:
            field_definitions_item = SchemaField.from_dict(field_definitions_item_data)

            field_definitions.append(field_definitions_item)

        type = None
        if d.get("type") is not None:
            type = Type(d.get("type"))

        system_name = d.get("systemName")

        derived_from = d.get("derivedFrom")

        automation_input_file_configs = []
        for automation_input_file_configs_item_data in d.get("automationInputFileConfigs") or []:
            automation_input_file_configs_item = automation_input_file_configs_item_data

            automation_input_file_configs.append(automation_input_file_configs_item)

        automation_output_file_configs = []
        for automation_output_file_configs_item_data in d.get("automationOutputFileConfigs") or []:
            automation_output_file_configs_item = automation_output_file_configs_item_data

            automation_output_file_configs.append(automation_output_file_configs_item)

        organization = None
        if d.get("organization") is not None:
            organization = d.get("organization")

        return AssayRunSchema(
            id=id,
            name=name,
            field_definitions=field_definitions,
            type=type,
            system_name=system_name,
            derived_from=derived_from,
            automation_input_file_configs=automation_input_file_configs,
            automation_output_file_configs=automation_output_file_configs,
            organization=organization,
        )
