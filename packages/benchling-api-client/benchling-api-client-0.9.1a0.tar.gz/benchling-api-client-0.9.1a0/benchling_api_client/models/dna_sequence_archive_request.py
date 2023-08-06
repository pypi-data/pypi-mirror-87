from typing import Any, Dict, List

import attr

from ..models.reason import Reason


@attr.s(auto_attribs=True)
class DnaSequenceArchiveRequest:
    """The request body for archiving DNA sequences."""

    reason: Reason
    dna_sequence_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason.value

        dna_sequence_ids = self.dna_sequence_ids

        properties: Dict[str, Any] = dict()

        properties["reason"] = reason
        properties["dnaSequenceIds"] = dna_sequence_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DnaSequenceArchiveRequest":
        reason = Reason(d["reason"])

        dna_sequence_ids = d["dnaSequenceIds"]

        return DnaSequenceArchiveRequest(
            reason=reason,
            dna_sequence_ids=dna_sequence_ids,
        )
