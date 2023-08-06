from typing import Any, Dict, List

import attr

from ..models.blob import Blob


@attr.s(auto_attribs=True)
class BlobBulkGetResponse:
    """  """

    blobs: List[Blob]

    def to_dict(self) -> Dict[str, Any]:
        blobs = []
        for blobs_item_data in self.blobs:
            blobs_item = blobs_item_data.to_dict()

            blobs.append(blobs_item)

        properties: Dict[str, Any] = dict()

        properties["blobs"] = blobs
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BlobBulkGetResponse":
        blobs = []
        for blobs_item_data in d["blobs"]:
            blobs_item = Blob.from_dict(blobs_item_data)

            blobs.append(blobs_item)

        return BlobBulkGetResponse(
            blobs=blobs,
        )
