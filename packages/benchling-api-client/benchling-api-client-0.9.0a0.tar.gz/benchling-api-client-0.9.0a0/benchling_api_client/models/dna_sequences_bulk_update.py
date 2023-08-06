from typing import Any, Dict, List, Optional, cast

import attr

from ..models.dna_sequence_bulk_update import DnaSequenceBulkUpdate
from ..types import UNSET


@attr.s(auto_attribs=True)
class DnaSequencesBulkUpdate:
    """  """

    dna_sequences: Optional[List[DnaSequenceBulkUpdate]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.dna_sequences is None:
            dna_sequences = None
        elif self.dna_sequences is UNSET:
            dna_sequences = UNSET
        else:
            dna_sequences = []
            for dna_sequences_item_data in self.dna_sequences:
                dna_sequences_item = dna_sequences_item_data.to_dict()

                dna_sequences.append(dna_sequences_item)

        properties: Dict[str, Any] = dict()

        if dna_sequences is not UNSET:
            properties["dnaSequences"] = dna_sequences
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DnaSequencesBulkUpdate":
        dna_sequences = []
        for dna_sequences_item_data in d.get("dnaSequences") or []:
            dna_sequences_item = DnaSequenceBulkUpdate.from_dict(dna_sequences_item_data)

            dna_sequences.append(dna_sequences_item)

        return DnaSequencesBulkUpdate(
            dna_sequences=dna_sequences,
        )
