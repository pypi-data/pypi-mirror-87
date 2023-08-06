from typing import Any, Dict, List, Optional, cast

import attr

from ..models.aa_sequence_bulk_create import AaSequenceBulkCreate
from ..types import UNSET


@attr.s(auto_attribs=True)
class AaSequencesBulkCreate:
    """  """

    aa_sequences: Optional[List[AaSequenceBulkCreate]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.aa_sequences is None:
            aa_sequences = None
        elif self.aa_sequences is UNSET:
            aa_sequences = UNSET
        else:
            aa_sequences = []
            for aa_sequences_item_data in self.aa_sequences:
                aa_sequences_item = aa_sequences_item_data.to_dict()

                aa_sequences.append(aa_sequences_item)

        properties: Dict[str, Any] = dict()

        if aa_sequences is not UNSET:
            properties["aaSequences"] = aa_sequences
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AaSequencesBulkCreate":
        aa_sequences = []
        for aa_sequences_item_data in d.get("aaSequences") or []:
            aa_sequences_item = AaSequenceBulkCreate.from_dict(aa_sequences_item_data)

            aa_sequences.append(aa_sequences_item)

        return AaSequencesBulkCreate(
            aa_sequences=aa_sequences,
        )
