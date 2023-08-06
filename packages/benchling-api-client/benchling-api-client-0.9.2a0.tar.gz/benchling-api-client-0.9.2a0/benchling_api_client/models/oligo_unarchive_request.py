from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class OligoUnarchiveRequest:
    """The request body for unarchiving Oligos."""

    oligo_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        oligo_ids = self.oligo_ids

        properties: Dict[str, Any] = dict()

        properties["oligoIds"] = oligo_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "OligoUnarchiveRequest":
        oligo_ids = d["oligoIds"]

        return OligoUnarchiveRequest(
            oligo_ids=oligo_ids,
        )
