from typing import Any, Dict, List

import attr

from ..models.aa_sequence import AaSequence


@attr.s(auto_attribs=True)
class AaSequenceList:
    """  """

    next_token: str
    aa_sequences: List[AaSequence]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        aa_sequences = []
        for aa_sequences_item_data in self.aa_sequences:
            aa_sequences_item = aa_sequences_item_data.to_dict()

            aa_sequences.append(aa_sequences_item)

        properties: Dict[str, Any] = dict()

        properties["nextToken"] = next_token
        properties["aaSequences"] = aa_sequences
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AaSequenceList":
        next_token = d["nextToken"]

        aa_sequences = []
        for aa_sequences_item_data in d["aaSequences"]:
            aa_sequences_item = AaSequence.from_dict(aa_sequences_item_data)

            aa_sequences.append(aa_sequences_item)

        return AaSequenceList(
            next_token=next_token,
            aa_sequences=aa_sequences,
        )
