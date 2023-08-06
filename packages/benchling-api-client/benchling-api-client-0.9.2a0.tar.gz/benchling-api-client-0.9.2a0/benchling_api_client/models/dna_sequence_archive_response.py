from typing import Any, Dict, List, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class DnaSequenceArchiveResponse:
    """IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of DNA sequences along with any IDs of batches that were archived / unarchived."""

    dna_sequence_ids: Optional[List[str]] = cast(None, UNSET)
    batch_ids: Optional[List[str]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.dna_sequence_ids is None:
            dna_sequence_ids = None
        elif self.dna_sequence_ids is UNSET:
            dna_sequence_ids = UNSET
        else:
            dna_sequence_ids = self.dna_sequence_ids

        if self.batch_ids is None:
            batch_ids = None
        elif self.batch_ids is UNSET:
            batch_ids = UNSET
        else:
            batch_ids = self.batch_ids

        properties: Dict[str, Any] = dict()

        if dna_sequence_ids is not UNSET:
            properties["dnaSequenceIds"] = dna_sequence_ids
        if batch_ids is not UNSET:
            properties["batchIds"] = batch_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DnaSequenceArchiveResponse":
        dna_sequence_ids = d.get("dnaSequenceIds")

        batch_ids = d.get("batchIds")

        return DnaSequenceArchiveResponse(
            dna_sequence_ids=dna_sequence_ids,
            batch_ids=batch_ids,
        )
