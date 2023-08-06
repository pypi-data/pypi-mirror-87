import datetime
from typing import Any, Dict, List, Optional, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.request_status import RequestStatus
from ..types import UNSET


@attr.s(auto_attribs=True)
class RequestPatch:
    """  """

    request_status: Optional[RequestStatus] = cast(None, UNSET)
    assignees: Optional[List[Union[Dict[Any, Any], Dict[Any, Any]]]] = cast(None, UNSET)
    requestor_id: Optional[str] = cast(None, UNSET)
    scheduled_on: Optional[datetime.date] = cast(None, UNSET)
    project_id: Optional[str] = cast(None, UNSET)
    fields: Optional[Dict[Any, Any]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.request_status is UNSET:
            request_status = UNSET
        else:
            request_status = self.request_status.value if self.request_status else None

        if self.assignees is None:
            assignees = None
        elif self.assignees is UNSET:
            assignees = UNSET
        else:
            assignees = []
            for assignees_item_data in self.assignees:
                if isinstance(assignees_item_data, Dict[Any, Any]):
                    assignees_item = assignees_item_data

                else:
                    assignees_item = assignees_item_data

                assignees.append(assignees_item)

        requestor_id = self.requestor_id
        if self.scheduled_on is UNSET:
            scheduled_on = UNSET
        else:
            scheduled_on = self.scheduled_on.isoformat() if self.scheduled_on else None

        project_id = self.project_id
        if self.fields is UNSET:
            fields = UNSET
        else:
            fields = self.fields if self.fields else None

        properties: Dict[str, Any] = dict()

        if request_status is not UNSET:
            properties["requestStatus"] = request_status
        if assignees is not UNSET:
            properties["assignees"] = assignees
        if requestor_id is not UNSET:
            properties["requestorId"] = requestor_id
        if scheduled_on is not UNSET:
            properties["scheduledOn"] = scheduled_on
        if project_id is not UNSET:
            properties["projectId"] = project_id
        if fields is not UNSET:
            properties["fields"] = fields
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RequestPatch":
        request_status = None
        if d.get("requestStatus") is not None:
            request_status = RequestStatus(d.get("requestStatus"))

        assignees = []
        for assignees_item_data in d.get("assignees") or []:

            def _parse_assignees_item(data: Dict[str, Any]) -> Union[Dict[Any, Any], Dict[Any, Any]]:
                assignees_item: Union[Dict[Any, Any], Dict[Any, Any]]
                try:
                    assignees_item = assignees_item_data

                    return assignees_item
                except:  # noqa: E722
                    pass
                assignees_item = assignees_item_data

                return assignees_item

            assignees_item = _parse_assignees_item(assignees_item_data)

            assignees.append(assignees_item)

        requestor_id = d.get("requestorId")

        scheduled_on = None
        if d.get("scheduledOn") is not None:
            scheduled_on = isoparse(cast(str, d.get("scheduledOn"))).date()

        project_id = d.get("projectId")

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        return RequestPatch(
            request_status=request_status,
            assignees=assignees,
            requestor_id=requestor_id,
            scheduled_on=scheduled_on,
            project_id=project_id,
            fields=fields,
        )
