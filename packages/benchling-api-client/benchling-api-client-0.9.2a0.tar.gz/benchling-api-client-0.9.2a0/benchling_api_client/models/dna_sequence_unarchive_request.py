from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class DnaSequenceUnarchiveRequest:
    """The request body for unarchiving DNA sequences."""

    dna_sequence_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        dna_sequence_ids = self.dna_sequence_ids

        properties: Dict[str, Any] = dict()

        properties["dnaSequenceIds"] = dna_sequence_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DnaSequenceUnarchiveRequest":
        dna_sequence_ids = d["dnaSequenceIds"]

        return DnaSequenceUnarchiveRequest(
            dna_sequence_ids=dna_sequence_ids,
        )
