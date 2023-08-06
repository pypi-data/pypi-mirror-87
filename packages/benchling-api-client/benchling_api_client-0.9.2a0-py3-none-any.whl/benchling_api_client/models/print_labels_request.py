from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class PrintLabelsRequest:
    """  """

    container_ids: List[str]
    label_template_id: str
    printer_id: str

    def to_dict(self) -> Dict[str, Any]:
        container_ids = self.container_ids

        label_template_id = self.label_template_id
        printer_id = self.printer_id

        properties: Dict[str, Any] = dict()

        properties["containerIds"] = container_ids
        properties["labelTemplateId"] = label_template_id
        properties["printerId"] = printer_id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PrintLabelsRequest":
        container_ids = d["containerIds"]

        label_template_id = d["labelTemplateId"]

        printer_id = d["printerId"]

        return PrintLabelsRequest(
            container_ids=container_ids,
            label_template_id=label_template_id,
            printer_id=printer_id,
        )
