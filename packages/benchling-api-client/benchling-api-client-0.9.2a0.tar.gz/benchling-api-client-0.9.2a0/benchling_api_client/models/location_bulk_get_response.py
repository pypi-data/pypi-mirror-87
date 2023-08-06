from typing import Any, Dict, List

import attr

from ..models.location import Location


@attr.s(auto_attribs=True)
class LocationBulkGetResponse:
    """  """

    locations: List[Location]

    def to_dict(self) -> Dict[str, Any]:
        locations = []
        for locations_item_data in self.locations:
            locations_item = locations_item_data.to_dict()

            locations.append(locations_item)

        properties: Dict[str, Any] = dict()

        properties["locations"] = locations
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "LocationBulkGetResponse":
        locations = []
        for locations_item_data in d["locations"]:
            locations_item = Location.from_dict(locations_item_data)

            locations.append(locations_item)

        return LocationBulkGetResponse(
            locations=locations,
        )
