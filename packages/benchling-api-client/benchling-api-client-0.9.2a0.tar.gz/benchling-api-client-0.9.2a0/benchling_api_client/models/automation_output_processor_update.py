from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class AutomationOutputProcessorUpdate:
    """  """

    file_id: str

    def to_dict(self) -> Dict[str, Any]:
        file_id = self.file_id

        properties: Dict[str, Any] = dict()

        properties["fileId"] = file_id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AutomationOutputProcessorUpdate":
        file_id = d["fileId"]

        return AutomationOutputProcessorUpdate(
            file_id=file_id,
        )
