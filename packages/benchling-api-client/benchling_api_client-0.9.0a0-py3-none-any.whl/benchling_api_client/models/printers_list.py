from typing import Any, Dict, List

import attr

from ..models.printer import Printer


@attr.s(auto_attribs=True)
class PrintersList:
    """  """

    label_printers: List[Printer]

    def to_dict(self) -> Dict[str, Any]:
        label_printers = []
        for label_printers_item_data in self.label_printers:
            label_printers_item = label_printers_item_data.to_dict()

            label_printers.append(label_printers_item)

        properties: Dict[str, Any] = dict()

        properties["labelPrinters"] = label_printers
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PrintersList":
        label_printers = []
        for label_printers_item_data in d["labelPrinters"]:
            label_printers_item = Printer.from_dict(label_printers_item_data)

            label_printers.append(label_printers_item)

        return PrintersList(
            label_printers=label_printers,
        )
