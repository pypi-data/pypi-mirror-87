from typing import Any, Dict, List, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class BoxArchiveResponse:
    """IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of boxes along with any IDs of containers that were archived / unarchived."""

    box_ids: Optional[List[str]] = cast(None, UNSET)
    container_ids: Optional[List[str]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.box_ids is None:
            box_ids = None
        elif self.box_ids is UNSET:
            box_ids = UNSET
        else:
            box_ids = self.box_ids

        if self.container_ids is None:
            container_ids = None
        elif self.container_ids is UNSET:
            container_ids = UNSET
        else:
            container_ids = self.container_ids

        properties: Dict[str, Any] = dict()

        if box_ids is not UNSET:
            properties["boxIds"] = box_ids
        if container_ids is not UNSET:
            properties["containerIds"] = container_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BoxArchiveResponse":
        box_ids = d.get("boxIds")

        container_ids = d.get("containerIds")

        return BoxArchiveResponse(
            box_ids=box_ids,
            container_ids=container_ids,
        )
