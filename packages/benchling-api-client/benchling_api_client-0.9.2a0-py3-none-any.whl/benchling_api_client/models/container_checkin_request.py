from typing import Any, Dict, List, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class ContainerCheckinRequest:
    """  """

    container_ids: List[str]
    comments: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        container_ids = self.container_ids

        comments = self.comments

        properties: Dict[str, Any] = dict()

        properties["containerIds"] = container_ids
        if comments is not UNSET:
            properties["comments"] = comments
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ContainerCheckinRequest":
        container_ids = d["containerIds"]

        comments = d.get("comments")

        return ContainerCheckinRequest(
            container_ids=container_ids,
            comments=comments,
        )
