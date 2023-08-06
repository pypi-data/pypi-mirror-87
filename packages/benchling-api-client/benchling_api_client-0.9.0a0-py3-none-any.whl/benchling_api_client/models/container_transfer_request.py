from typing import Any, Dict, List, Optional, cast

import attr

from ..models.measurement import Measurement
from ..types import UNSET


@attr.s(auto_attribs=True)
class ContainerTransferRequest:
    """  """

    transfer_volume: Measurement
    destination_volume: Optional[Measurement] = cast(None, UNSET)
    destination_contents: Optional[List[Dict[Any, Any]]] = cast(None, UNSET)
    source_entity_id: Optional[str] = cast(None, UNSET)
    source_batch_id: Optional[str] = cast(None, UNSET)
    source_container_id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        transfer_volume = self.transfer_volume.to_dict()

        if self.destination_volume is UNSET:
            destination_volume = UNSET
        else:
            destination_volume = self.destination_volume.to_dict() if self.destination_volume else None

        if self.destination_contents is None:
            destination_contents = None
        elif self.destination_contents is UNSET:
            destination_contents = UNSET
        else:
            destination_contents = []
            for destination_contents_item_data in self.destination_contents:
                destination_contents_item = destination_contents_item_data

                destination_contents.append(destination_contents_item)

        source_entity_id = self.source_entity_id
        source_batch_id = self.source_batch_id
        source_container_id = self.source_container_id

        properties: Dict[str, Any] = dict()

        properties["transferVolume"] = transfer_volume
        if destination_volume is not UNSET:
            properties["destinationVolume"] = destination_volume
        if destination_contents is not UNSET:
            properties["destinationContents"] = destination_contents
        if source_entity_id is not UNSET:
            properties["sourceEntityId"] = source_entity_id
        if source_batch_id is not UNSET:
            properties["sourceBatchId"] = source_batch_id
        if source_container_id is not UNSET:
            properties["sourceContainerId"] = source_container_id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ContainerTransferRequest":
        transfer_volume = Measurement.from_dict(d["transferVolume"])

        destination_volume = None
        if d.get("destinationVolume") is not None:
            destination_volume = Measurement.from_dict(cast(Dict[str, Any], d.get("destinationVolume")))

        destination_contents = []
        for destination_contents_item_data in d.get("destinationContents") or []:
            destination_contents_item = destination_contents_item_data

            destination_contents.append(destination_contents_item)

        source_entity_id = d.get("sourceEntityId")

        source_batch_id = d.get("sourceBatchId")

        source_container_id = d.get("sourceContainerId")

        return ContainerTransferRequest(
            transfer_volume=transfer_volume,
            destination_volume=destination_volume,
            destination_contents=destination_contents,
            source_entity_id=source_entity_id,
            source_batch_id=source_batch_id,
            source_container_id=source_container_id,
        )
