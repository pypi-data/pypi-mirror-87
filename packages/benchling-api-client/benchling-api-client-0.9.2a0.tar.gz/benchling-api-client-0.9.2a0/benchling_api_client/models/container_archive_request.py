from typing import Any, Dict, List, Optional, cast

import attr

from ..models.reason import Reason
from ..types import UNSET


@attr.s(auto_attribs=True)
class ContainerArchiveRequest:
    """  """

    container_ids: List[str]
    reason: Reason
    should_remove_barcodes: Optional[bool] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        container_ids = self.container_ids

        reason = self.reason.value

        should_remove_barcodes = self.should_remove_barcodes

        properties: Dict[str, Any] = dict()

        properties["containerIds"] = container_ids
        properties["reason"] = reason
        if should_remove_barcodes is not UNSET:
            properties["shouldRemoveBarcodes"] = should_remove_barcodes
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ContainerArchiveRequest":
        container_ids = d["containerIds"]

        reason = Reason(d["reason"])

        should_remove_barcodes = d.get("shouldRemoveBarcodes")

        return ContainerArchiveRequest(
            container_ids=container_ids,
            reason=reason,
            should_remove_barcodes=should_remove_barcodes,
        )
