from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class LocationUnarchiveRequest:
    """  """

    location_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        location_ids = self.location_ids

        properties: Dict[str, Any] = dict()

        properties["locationIds"] = location_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "LocationUnarchiveRequest":
        location_ids = d["locationIds"]

        return LocationUnarchiveRequest(
            location_ids=location_ids,
        )
