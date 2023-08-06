from typing import Any, Dict, List

import attr

from ..models.automation_input_generator import AutomationInputGenerator


@attr.s(auto_attribs=True)
class AutomationFileInputList:
    """  """

    automation_input_generators: List[AutomationInputGenerator]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        automation_input_generators = []
        for automation_input_generators_item_data in self.automation_input_generators:
            automation_input_generators_item = automation_input_generators_item_data.to_dict()

            automation_input_generators.append(automation_input_generators_item)

        next_token = self.next_token

        properties: Dict[str, Any] = dict()

        properties["automationInputGenerators"] = automation_input_generators
        properties["nextToken"] = next_token
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AutomationFileInputList":
        automation_input_generators = []
        for automation_input_generators_item_data in d["automationInputGenerators"]:
            automation_input_generators_item = AutomationInputGenerator.from_dict(automation_input_generators_item_data)

            automation_input_generators.append(automation_input_generators_item)

        next_token = d["nextToken"]

        return AutomationFileInputList(
            automation_input_generators=automation_input_generators,
            next_token=next_token,
        )
