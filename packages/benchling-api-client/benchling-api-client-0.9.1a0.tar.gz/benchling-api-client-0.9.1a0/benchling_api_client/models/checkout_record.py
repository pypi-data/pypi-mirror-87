from typing import Any, Dict, Optional, Union, cast

import attr

from ..models.status import Status
from ..models.team_summary import TeamSummary
from ..models.user_summary import UserSummary
from ..types import UNSET


@attr.s(auto_attribs=True)
class CheckoutRecord:
    """  """

    status: Status
    comment: str
    modified_at: str
    assignee: Optional[Union[Optional[UserSummary], Optional[TeamSummary]]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        comment = self.comment
        modified_at = self.modified_at
        if self.assignee is None:
            assignee: Optional[Union[Optional[UserSummary], Optional[TeamSummary]]] = None
        elif self.assignee is UNSET:
            assignee = UNSET
        elif isinstance(self.assignee, UserSummary):
            if self.assignee is UNSET:
                assignee = UNSET
            else:
                assignee = self.assignee.to_dict() if self.assignee else None

        else:
            if self.assignee is UNSET:
                assignee = UNSET
            else:
                assignee = self.assignee.to_dict() if self.assignee else None

        properties: Dict[str, Any] = dict()

        properties["status"] = status
        properties["comment"] = comment
        properties["modifiedAt"] = modified_at
        if assignee is not UNSET:
            properties["assignee"] = assignee
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CheckoutRecord":
        status = Status(d["status"])

        comment = d["comment"]

        modified_at = d["modifiedAt"]

        def _parse_assignee(data: Dict[str, Any]) -> Optional[Union[Optional[UserSummary], Optional[TeamSummary]]]:
            assignee: Optional[Union[Optional[UserSummary], Optional[TeamSummary]]]
            try:
                assignee = None
                if d.get("assignee") is not None:
                    assignee = UserSummary.from_dict(cast(Dict[str, Any], d.get("assignee")))

                return assignee
            except:  # noqa: E722
                pass
            assignee = None
            if d.get("assignee") is not None:
                assignee = TeamSummary.from_dict(cast(Dict[str, Any], d.get("assignee")))

            return assignee

        assignee = _parse_assignee(d.get("assignee"))

        return CheckoutRecord(
            status=status,
            comment=comment,
            modified_at=modified_at,
            assignee=assignee,
        )
