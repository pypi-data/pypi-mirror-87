from typing import Any, Dict, List

import attr

from ..models.automation_output_processor import AutomationOutputProcessor


@attr.s(auto_attribs=True)
class AutomationFileOutputList:
    """  """

    automation_output_processors: List[AutomationOutputProcessor]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        automation_output_processors = []
        for automation_output_processors_item_data in self.automation_output_processors:
            automation_output_processors_item = automation_output_processors_item_data.to_dict()

            automation_output_processors.append(automation_output_processors_item)

        next_token = self.next_token

        properties: Dict[str, Any] = dict()

        properties["automationOutputProcessors"] = automation_output_processors
        properties["nextToken"] = next_token
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AutomationFileOutputList":
        automation_output_processors = []
        for automation_output_processors_item_data in d["automationOutputProcessors"]:
            automation_output_processors_item = AutomationOutputProcessor.from_dict(
                automation_output_processors_item_data
            )

            automation_output_processors.append(automation_output_processors_item)

        next_token = d["nextToken"]

        return AutomationFileOutputList(
            automation_output_processors=automation_output_processors,
            next_token=next_token,
        )
