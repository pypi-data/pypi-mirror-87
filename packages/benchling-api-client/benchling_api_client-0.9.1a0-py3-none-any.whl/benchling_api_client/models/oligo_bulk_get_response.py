from typing import Any, Dict, List

import attr

from ..models.oligo import Oligo


@attr.s(auto_attribs=True)
class OligoBulkGetResponse:
    """  """

    oligos: List[Oligo]

    def to_dict(self) -> Dict[str, Any]:
        oligos = []
        for oligos_item_data in self.oligos:
            oligos_item = oligos_item_data.to_dict()

            oligos.append(oligos_item)

        properties: Dict[str, Any] = dict()

        properties["oligos"] = oligos
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "OligoBulkGetResponse":
        oligos = []
        for oligos_item_data in d["oligos"]:
            oligos_item = Oligo.from_dict(oligos_item_data)

            oligos.append(oligos_item)

        return OligoBulkGetResponse(
            oligos=oligos,
        )
