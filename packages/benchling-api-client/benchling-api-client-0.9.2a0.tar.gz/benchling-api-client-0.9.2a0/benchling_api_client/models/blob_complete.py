from typing import Any, Dict, List, Optional, cast

import attr

from ..models.blob_part import BlobPart
from ..types import UNSET


@attr.s(auto_attribs=True)
class BlobComplete:
    """  """

    parts: Optional[List[BlobPart]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.parts is None:
            parts = None
        elif self.parts is UNSET:
            parts = UNSET
        else:
            parts = []
            for parts_item_data in self.parts:
                parts_item = parts_item_data.to_dict()

                parts.append(parts_item)

        properties: Dict[str, Any] = dict()

        if parts is not UNSET:
            properties["parts"] = parts
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BlobComplete":
        parts = []
        for parts_item_data in d.get("parts") or []:
            parts_item = BlobPart.from_dict(parts_item_data)

            parts.append(parts_item)

        return BlobComplete(
            parts=parts,
        )
