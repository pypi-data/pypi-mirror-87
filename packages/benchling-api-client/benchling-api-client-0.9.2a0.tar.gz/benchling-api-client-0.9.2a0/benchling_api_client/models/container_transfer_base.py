from typing import Any, Dict, Optional, cast

import attr

from ..models.measurement import Measurement
from ..types import UNSET


@attr.s(auto_attribs=True)
class ContainerTransferBase:
    """  """

    transfer_volume: Measurement
    source_entity_id: Optional[str] = cast(None, UNSET)
    source_batch_id: Optional[str] = cast(None, UNSET)
    source_container_id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        transfer_volume = self.transfer_volume.to_dict()

        source_entity_id = self.source_entity_id
        source_batch_id = self.source_batch_id
        source_container_id = self.source_container_id

        properties: Dict[str, Any] = dict()

        properties["transferVolume"] = transfer_volume
        if source_entity_id is not UNSET:
            properties["sourceEntityId"] = source_entity_id
        if source_batch_id is not UNSET:
            properties["sourceBatchId"] = source_batch_id
        if source_container_id is not UNSET:
            properties["sourceContainerId"] = source_container_id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ContainerTransferBase":
        transfer_volume = Measurement.from_dict(d["transferVolume"])

        source_entity_id = d.get("sourceEntityId")

        source_batch_id = d.get("sourceBatchId")

        source_container_id = d.get("sourceContainerId")

        return ContainerTransferBase(
            transfer_volume=transfer_volume,
            source_entity_id=source_entity_id,
            source_batch_id=source_batch_id,
            source_container_id=source_container_id,
        )
