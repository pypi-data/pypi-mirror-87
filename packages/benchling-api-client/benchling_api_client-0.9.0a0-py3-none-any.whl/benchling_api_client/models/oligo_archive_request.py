from typing import Any, Dict, List

import attr

from ..models.reason import Reason


@attr.s(auto_attribs=True)
class OligoArchiveRequest:
    """The request body for archiving Oligos."""

    reason: Reason
    oligo_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason.value

        oligo_ids = self.oligo_ids

        properties: Dict[str, Any] = dict()

        properties["reason"] = reason
        properties["oligoIds"] = oligo_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "OligoArchiveRequest":
        reason = Reason(d["reason"])

        oligo_ids = d["oligoIds"]

        return OligoArchiveRequest(
            reason=reason,
            oligo_ids=oligo_ids,
        )
