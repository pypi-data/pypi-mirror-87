from typing import Any, Dict, List

import attr

from ..models.multiple_containers_transfer_request import MultipleContainersTransferRequest


@attr.s(auto_attribs=True)
class ContainersTransfersRequest:
    """  """

    transfers: List[MultipleContainersTransferRequest]

    def to_dict(self) -> Dict[str, Any]:
        transfers = []
        for transfers_item_data in self.transfers:
            transfers_item = transfers_item_data.to_dict()

            transfers.append(transfers_item)

        properties: Dict[str, Any] = dict()

        properties["transfers"] = transfers
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ContainersTransfersRequest":
        transfers = []
        for transfers_item_data in d["transfers"]:
            transfers_item = MultipleContainersTransferRequest.from_dict(transfers_item_data)

            transfers.append(transfers_item)

        return ContainersTransfersRequest(
            transfers=transfers,
        )
