from typing import Any, Dict, List, Optional, cast

import attr

from ..models.reason1 import Reason1
from ..types import UNSET


@attr.s(auto_attribs=True)
class LocationArchiveRequest:
    """  """

    location_ids: List[str]
    reason: Reason1
    should_remove_barcodes: Optional[bool] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        location_ids = self.location_ids

        reason = self.reason.value

        should_remove_barcodes = self.should_remove_barcodes

        properties: Dict[str, Any] = dict()

        properties["locationIds"] = location_ids
        properties["reason"] = reason
        if should_remove_barcodes is not UNSET:
            properties["shouldRemoveBarcodes"] = should_remove_barcodes
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "LocationArchiveRequest":
        location_ids = d["locationIds"]

        reason = Reason1(d["reason"])

        should_remove_barcodes = d.get("shouldRemoveBarcodes")

        return LocationArchiveRequest(
            location_ids=location_ids,
            reason=reason,
            should_remove_barcodes=should_remove_barcodes,
        )
