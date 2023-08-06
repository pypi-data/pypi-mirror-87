from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class AutofillSequencesRequest:
    """  """

    dna_sequence_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        dna_sequence_ids = self.dna_sequence_ids

        properties: Dict[str, Any] = dict()

        properties["dnaSequenceIds"] = dna_sequence_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AutofillSequencesRequest":
        dna_sequence_ids = d["dnaSequenceIds"]

        return AutofillSequencesRequest(
            dna_sequence_ids=dna_sequence_ids,
        )
