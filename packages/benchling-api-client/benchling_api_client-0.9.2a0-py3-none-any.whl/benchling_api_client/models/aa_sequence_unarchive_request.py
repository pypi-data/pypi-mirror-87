from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class AaSequenceUnarchiveRequest:
    """The request body for unarchiving AA sequences."""

    aa_sequence_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        aa_sequence_ids = self.aa_sequence_ids

        properties: Dict[str, Any] = dict()

        properties["aaSequenceIds"] = aa_sequence_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AaSequenceUnarchiveRequest":
        aa_sequence_ids = d["aaSequenceIds"]

        return AaSequenceUnarchiveRequest(
            aa_sequence_ids=aa_sequence_ids,
        )
