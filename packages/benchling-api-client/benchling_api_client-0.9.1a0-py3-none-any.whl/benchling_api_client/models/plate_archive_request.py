from typing import Any, Dict, List

import attr

from ..models.reason import Reason


@attr.s(auto_attribs=True)
class PlateArchiveRequest:
    """  """

    plate_ids: List[str]
    reason: Reason
    should_remove_barcodes: bool

    def to_dict(self) -> Dict[str, Any]:
        plate_ids = self.plate_ids

        reason = self.reason.value

        should_remove_barcodes = self.should_remove_barcodes

        properties: Dict[str, Any] = dict()

        properties["plateIds"] = plate_ids
        properties["reason"] = reason
        properties["shouldRemoveBarcodes"] = should_remove_barcodes
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PlateArchiveRequest":
        plate_ids = d["plateIds"]

        reason = Reason(d["reason"])

        should_remove_barcodes = d["shouldRemoveBarcodes"]

        return PlateArchiveRequest(
            plate_ids=plate_ids,
            reason=reason,
            should_remove_barcodes=should_remove_barcodes,
        )
