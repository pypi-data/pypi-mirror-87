from typing import Any, Dict, List

import attr

from ..models.reason import Reason


@attr.s(auto_attribs=True)
class AaSequenceArchiveRequest:
    """The request body for archiving AA sequences."""

    reason: Reason
    aa_sequence_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason.value

        aa_sequence_ids = self.aa_sequence_ids

        properties: Dict[str, Any] = dict()

        properties["reason"] = reason
        properties["aaSequenceIds"] = aa_sequence_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AaSequenceArchiveRequest":
        reason = Reason(d["reason"])

        aa_sequence_ids = d["aaSequenceIds"]

        return AaSequenceArchiveRequest(
            reason=reason,
            aa_sequence_ids=aa_sequence_ids,
        )
