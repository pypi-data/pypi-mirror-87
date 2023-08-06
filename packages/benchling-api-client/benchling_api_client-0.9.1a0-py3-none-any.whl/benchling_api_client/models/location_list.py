from typing import Any, Dict, List

import attr

from ..models.location import Location


@attr.s(auto_attribs=True)
class LocationList:
    """  """

    locations: List[Location]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        locations = []
        for locations_item_data in self.locations:
            locations_item = locations_item_data.to_dict()

            locations.append(locations_item)

        next_token = self.next_token

        properties: Dict[str, Any] = dict()

        properties["locations"] = locations
        properties["nextToken"] = next_token
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "LocationList":
        locations = []
        for locations_item_data in d["locations"]:
            locations_item = Location.from_dict(locations_item_data)

            locations.append(locations_item)

        next_token = d["nextToken"]

        return LocationList(
            locations=locations,
            next_token=next_token,
        )
