from typing import Any, Dict, List, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class CustomEntityArchivalChange:
    """IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of custom entities along with any IDs of batches that were archived (or unarchived)."""

    custom_entity_ids: Optional[List[str]] = cast(None, UNSET)
    batch_ids: Optional[List[str]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.custom_entity_ids is None:
            custom_entity_ids = None
        elif self.custom_entity_ids is UNSET:
            custom_entity_ids = UNSET
        else:
            custom_entity_ids = self.custom_entity_ids

        if self.batch_ids is None:
            batch_ids = None
        elif self.batch_ids is UNSET:
            batch_ids = UNSET
        else:
            batch_ids = self.batch_ids

        properties: Dict[str, Any] = dict()

        if custom_entity_ids is not UNSET:
            properties["customEntityIds"] = custom_entity_ids
        if batch_ids is not UNSET:
            properties["batchIds"] = batch_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CustomEntityArchivalChange":
        custom_entity_ids = d.get("customEntityIds")

        batch_ids = d.get("batchIds")

        return CustomEntityArchivalChange(
            custom_entity_ids=custom_entity_ids,
            batch_ids=batch_ids,
        )
