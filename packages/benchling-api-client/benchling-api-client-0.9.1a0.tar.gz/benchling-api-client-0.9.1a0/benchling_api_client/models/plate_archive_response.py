from typing import Any, Dict, List, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class PlateArchiveResponse:
    """IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of plates along with any IDs of containers that were archived / unarchived."""

    plate_ids: Optional[List[str]] = cast(None, UNSET)
    container_ids: Optional[List[str]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
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

        if plate_ids is not UNSET:
            properties["plateIds"] = plate_ids
        if container_ids is not UNSET:
            properties["containerIds"] = container_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PlateArchiveResponse":
        plate_ids = d.get("plateIds")

        container_ids = d.get("containerIds")

        return PlateArchiveResponse(
            plate_ids=plate_ids,
            container_ids=container_ids,
        )
