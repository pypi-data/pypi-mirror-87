from typing import Any, Dict, List

import attr

from ..models.plate import Plate


@attr.s(auto_attribs=True)
class PlateList:
    """  """

    next_token: str
    plates: List[Plate]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        plates = []
        for plates_item_data in self.plates:
            plates_item = plates_item_data.to_dict()

            plates.append(plates_item)

        properties: Dict[str, Any] = dict()

        properties["nextToken"] = next_token
        properties["plates"] = plates
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PlateList":
        next_token = d["nextToken"]

        plates = []
        for plates_item_data in d["plates"]:
            plates_item = Plate.from_dict(plates_item_data)

            plates.append(plates_item)

        return PlateList(
            next_token=next_token,
            plates=plates,
        )
