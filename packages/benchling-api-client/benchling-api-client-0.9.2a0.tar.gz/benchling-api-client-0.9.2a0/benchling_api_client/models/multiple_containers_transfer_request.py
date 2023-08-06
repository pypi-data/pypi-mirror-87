from typing import Any, Dict, Optional, cast

import attr

from ..models.measurement import Measurement
from ..types import UNSET


@attr.s(auto_attribs=True)
class MultipleContainersTransferRequest:
    """  """

    destination_container_id: str
    transfer_volume: Measurement
    source_concentration: Optional[Dict[Any, Any]] = cast(None, UNSET)
    final_volume: Optional[Measurement] = cast(None, UNSET)
    source_entity_id: Optional[str] = cast(None, UNSET)
    source_batch_id: Optional[str] = cast(None, UNSET)
    source_container_id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        destination_container_id = self.destination_container_id
        transfer_volume = self.transfer_volume.to_dict()

        if self.source_concentration is UNSET:
            source_concentration = UNSET
        else:
            source_concentration = self.source_concentration if self.source_concentration else None

        if self.final_volume is UNSET:
            final_volume = UNSET
        else:
            final_volume = self.final_volume.to_dict() if self.final_volume else None

        source_entity_id = self.source_entity_id
        source_batch_id = self.source_batch_id
        source_container_id = self.source_container_id

        properties: Dict[str, Any] = dict()

        properties["destinationContainerId"] = destination_container_id
        properties["transferVolume"] = transfer_volume
        if source_concentration is not UNSET:
            properties["sourceConcentration"] = source_concentration
        if final_volume is not UNSET:
            properties["finalVolume"] = final_volume
        if source_entity_id is not UNSET:
            properties["sourceEntityId"] = source_entity_id
        if source_batch_id is not UNSET:
            properties["sourceBatchId"] = source_batch_id
        if source_container_id is not UNSET:
            properties["sourceContainerId"] = source_container_id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "MultipleContainersTransferRequest":
        destination_container_id = d["destinationContainerId"]

        transfer_volume = Measurement.from_dict(d["transferVolume"])

        source_concentration = None
        if d.get("sourceConcentration") is not None:
            source_concentration = d.get("sourceConcentration")

        final_volume = None
        if d.get("finalVolume") is not None:
            final_volume = Measurement.from_dict(cast(Dict[str, Any], d.get("finalVolume")))

        source_entity_id = d.get("sourceEntityId")

        source_batch_id = d.get("sourceBatchId")

        source_container_id = d.get("sourceContainerId")

        return MultipleContainersTransferRequest(
            destination_container_id=destination_container_id,
            transfer_volume=transfer_volume,
            source_concentration=source_concentration,
            final_volume=final_volume,
            source_entity_id=source_entity_id,
            source_batch_id=source_batch_id,
            source_container_id=source_container_id,
        )
