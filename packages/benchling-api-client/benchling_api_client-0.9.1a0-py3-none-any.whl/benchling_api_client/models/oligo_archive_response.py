from typing import Any, Dict, List, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class OligoArchiveResponse:
    """IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of Oligos along with any IDs of batches that were archived / unarchived."""

    oligo_ids: Optional[List[str]] = cast(None, UNSET)
    batch_ids: Optional[List[str]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.oligo_ids is None:
            oligo_ids = None
        elif self.oligo_ids is UNSET:
            oligo_ids = UNSET
        else:
            oligo_ids = self.oligo_ids

        if self.batch_ids is None:
            batch_ids = None
        elif self.batch_ids is UNSET:
            batch_ids = UNSET
        else:
            batch_ids = self.batch_ids

        properties: Dict[str, Any] = dict()

        if oligo_ids is not UNSET:
            properties["oligoIds"] = oligo_ids
        if batch_ids is not UNSET:
            properties["batchIds"] = batch_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "OligoArchiveResponse":
        oligo_ids = d.get("oligoIds")

        batch_ids = d.get("batchIds")

        return OligoArchiveResponse(
            oligo_ids=oligo_ids,
            batch_ids=batch_ids,
        )
