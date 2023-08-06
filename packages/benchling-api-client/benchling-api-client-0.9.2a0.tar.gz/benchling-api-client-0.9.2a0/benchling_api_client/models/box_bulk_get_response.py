from typing import Any, Dict, List

import attr

from ..models.box import Box


@attr.s(auto_attribs=True)
class BoxBulkGetResponse:
    """  """

    boxes: List[Box]

    def to_dict(self) -> Dict[str, Any]:
        boxes = []
        for boxes_item_data in self.boxes:
            boxes_item = boxes_item_data.to_dict()

            boxes.append(boxes_item)

        properties: Dict[str, Any] = dict()

        properties["boxes"] = boxes
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BoxBulkGetResponse":
        boxes = []
        for boxes_item_data in d["boxes"]:
            boxes_item = Box.from_dict(boxes_item_data)

            boxes.append(boxes_item)

        return BoxBulkGetResponse(
            boxes=boxes,
        )
