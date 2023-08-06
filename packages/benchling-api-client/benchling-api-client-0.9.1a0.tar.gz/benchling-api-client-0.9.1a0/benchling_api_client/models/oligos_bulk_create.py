from typing import Any, Dict, List, Optional, cast

import attr

from ..models.oligo_bulk_create import OligoBulkCreate
from ..types import UNSET


@attr.s(auto_attribs=True)
class OligosBulkCreate:
    """  """

    oligos: Optional[List[OligoBulkCreate]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.oligos is None:
            oligos = None
        elif self.oligos is UNSET:
            oligos = UNSET
        else:
            oligos = []
            for oligos_item_data in self.oligos:
                oligos_item = oligos_item_data.to_dict()

                oligos.append(oligos_item)

        properties: Dict[str, Any] = dict()

        if oligos is not UNSET:
            properties["oligos"] = oligos
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "OligosBulkCreate":
        oligos = []
        for oligos_item_data in d.get("oligos") or []:
            oligos_item = OligoBulkCreate.from_dict(oligos_item_data)

            oligos.append(oligos_item)

        return OligosBulkCreate(
            oligos=oligos,
        )
