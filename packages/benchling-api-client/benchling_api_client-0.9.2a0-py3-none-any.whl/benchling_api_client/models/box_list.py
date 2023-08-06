from typing import Any, Dict, List

import attr

from ..models.box import Box


@attr.s(auto_attribs=True)
class BoxList:
    """  """

    next_token: str
    boxes: List[Box]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        boxes = []
        for boxes_item_data in self.boxes:
            boxes_item = boxes_item_data.to_dict()

            boxes.append(boxes_item)

        properties: Dict[str, Any] = dict()

        properties["nextToken"] = next_token
        properties["boxes"] = boxes
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BoxList":
        next_token = d["nextToken"]

        boxes = []
        for boxes_item_data in d["boxes"]:
            boxes_item = Box.from_dict(boxes_item_data)

            boxes.append(boxes_item)

        return BoxList(
            next_token=next_token,
            boxes=boxes,
        )
