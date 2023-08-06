from typing import Any, Dict, List, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class EntryUnarchivalResponse:
    """IDs of all items that were unarchived, grouped by resource type. This includes the IDs of entries that were unarchived."""

    entry_ids: Optional[List[str]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.entry_ids is None:
            entry_ids = None
        elif self.entry_ids is UNSET:
            entry_ids = UNSET
        else:
            entry_ids = self.entry_ids

        properties: Dict[str, Any] = dict()

        if entry_ids is not UNSET:
            properties["entryIds"] = entry_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EntryUnarchivalResponse":
        entry_ids = d.get("entryIds")

        return EntryUnarchivalResponse(
            entry_ids=entry_ids,
        )
