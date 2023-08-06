from typing import Any, Dict, List, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class ContainerCheckoutRequest:
    """  """

    container_ids: List[str]
    assignee_id: str
    comments: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        container_ids = self.container_ids

        assignee_id = self.assignee_id
        comments = self.comments

        properties: Dict[str, Any] = dict()

        properties["containerIds"] = container_ids
        properties["assigneeId"] = assignee_id
        if comments is not UNSET:
            properties["comments"] = comments
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ContainerCheckoutRequest":
        container_ids = d["containerIds"]

        assignee_id = d["assigneeId"]

        comments = d.get("comments")

        return ContainerCheckoutRequest(
            container_ids=container_ids,
            assignee_id=assignee_id,
            comments=comments,
        )
