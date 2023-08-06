from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class Barcodes:
    """  """

    barcodes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        barcodes = self.barcodes

        properties: Dict[str, Any] = dict()

        properties["barcodes"] = barcodes
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Barcodes":
        barcodes = d["barcodes"]

        return Barcodes(
            barcodes=barcodes,
        )
