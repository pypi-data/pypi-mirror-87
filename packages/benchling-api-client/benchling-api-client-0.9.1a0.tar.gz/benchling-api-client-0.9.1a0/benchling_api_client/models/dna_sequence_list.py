from typing import Any, Dict, List

import attr

from ..models.dna_sequence import DnaSequence


@attr.s(auto_attribs=True)
class DnaSequenceList:
    """  """

    next_token: str
    dna_sequences: List[DnaSequence]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        dna_sequences = []
        for dna_sequences_item_data in self.dna_sequences:
            dna_sequences_item = dna_sequences_item_data.to_dict()

            dna_sequences.append(dna_sequences_item)

        properties: Dict[str, Any] = dict()

        properties["nextToken"] = next_token
        properties["dnaSequences"] = dna_sequences
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DnaSequenceList":
        next_token = d["nextToken"]

        dna_sequences = []
        for dna_sequences_item_data in d["dnaSequences"]:
            dna_sequences_item = DnaSequence.from_dict(dna_sequences_item_data)

            dna_sequences.append(dna_sequences_item)

        return DnaSequenceList(
            next_token=next_token,
            dna_sequences=dna_sequences,
        )
