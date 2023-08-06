from typing import Any, Dict, List, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class LocationArchivalChange:
    """IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of locations along with any IDs of locations, boxes, plates, containers that were archived."""

    location_ids: Optional[List[str]] = cast(None, UNSET)
    box_ids: Optional[List[str]] = cast(None, UNSET)
    plate_ids: Optional[List[str]] = cast(None, UNSET)
    container_ids: Optional[List[str]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.location_ids is None:
            location_ids = None
        elif self.location_ids is UNSET:
            location_ids = UNSET
        else:
            location_ids = self.location_ids

        if self.box_ids is None:
            box_ids = None
        elif self.box_ids is UNSET:
            box_ids = UNSET
        else:
            box_ids = self.box_ids

        if self.plate_ids is None:
            plate_ids = None
        elif self.plate_ids is UNSET:
            plate_ids = UNSET
        else:
            plate_ids = self.plate_ids

        if self.container_ids is None:
            container_ids = None
        elif self.container_ids is UNSET:
            container_ids = UNSET
        else:
            container_ids = self.container_ids

        properties: Dict[str, Any] = dict()

        if location_ids is not UNSET:
            properties["locationIds"] = location_ids
        if box_ids is not UNSET:
            properties["boxIds"] = box_ids
        if plate_ids is not UNSET:
            properties["plateIds"] = plate_ids
        if container_ids is not UNSET:
            properties["containerIds"] = container_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "LocationArchivalChange":
        location_ids = d.get("locationIds")

        box_ids = d.get("boxIds")

        plate_ids = d.get("plateIds")

        container_ids = d.get("containerIds")

        return LocationArchivalChange(
            location_ids=location_ids,
            box_ids=box_ids,
            plate_ids=plate_ids,
            container_ids=container_ids,
        )
