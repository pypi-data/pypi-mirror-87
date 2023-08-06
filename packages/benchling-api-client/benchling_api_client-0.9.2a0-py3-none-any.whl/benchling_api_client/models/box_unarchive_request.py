from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class BoxUnarchiveRequest:
    """  """

    box_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        box_ids = self.box_ids

        properties: Dict[str, Any] = dict()

        properties["boxIds"] = box_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BoxUnarchiveRequest":
        box_ids = d["boxIds"]

        return BoxUnarchiveRequest(
            box_ids=box_ids,
        )
