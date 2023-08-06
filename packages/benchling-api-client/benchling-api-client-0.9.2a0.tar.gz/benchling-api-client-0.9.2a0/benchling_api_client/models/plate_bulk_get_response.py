from typing import Any, Dict, List

import attr

from ..models.plate import Plate


@attr.s(auto_attribs=True)
class PlateBulkGetResponse:
    """  """

    plates: List[Plate]

    def to_dict(self) -> Dict[str, Any]:
        plates = []
        for plates_item_data in self.plates:
            plates_item = plates_item_data.to_dict()

            plates.append(plates_item)

        properties: Dict[str, Any] = dict()

        properties["plates"] = plates
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PlateBulkGetResponse":
        plates = []
        for plates_item_data in d["plates"]:
            plates_item = Plate.from_dict(plates_item_data)

            plates.append(plates_item)

        return PlateBulkGetResponse(
            plates=plates,
        )
