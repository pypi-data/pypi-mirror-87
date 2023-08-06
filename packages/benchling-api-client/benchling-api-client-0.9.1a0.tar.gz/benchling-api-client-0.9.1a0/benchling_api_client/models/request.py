import datetime
from typing import Any, Dict, List, Optional, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.request_status import RequestStatus
from ..types import UNSET


@attr.s(auto_attribs=True)
class Request:
    """  """

    id: str
    created_at: datetime.datetime
    fields: Dict[Any, Any]
    display_id: str
    assignees: List[Union[Dict[Any, Any], Dict[Any, Any]]]
    request_status: RequestStatus
    web_url: str
    scheduled_on: Optional[datetime.date] = cast(None, UNSET)
    project_id: Optional[str] = cast(None, UNSET)
    api_url: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        created_at = self.created_at.isoformat()

        fields = self.fields

        display_id = self.display_id
        assignees = []
        for assignees_item_data in self.assignees:
            if isinstance(assignees_item_data, Dict[Any, Any]):
                assignees_item = assignees_item_data

            else:
                assignees_item = assignees_item_data

            assignees.append(assignees_item)

        request_status = self.request_status.value

        web_url = self.web_url
        if self.scheduled_on is UNSET:
            scheduled_on = UNSET
        else:
            scheduled_on = self.scheduled_on.isoformat() if self.scheduled_on else None

        project_id = self.project_id
        api_url = self.api_url

        properties: Dict[str, Any] = dict()

        properties["id"] = id
        properties["createdAt"] = created_at
        properties["fields"] = fields
        properties["displayId"] = display_id
        properties["assignees"] = assignees
        properties["requestStatus"] = request_status
        properties["webURL"] = web_url
        if scheduled_on is not UNSET:
            properties["scheduledOn"] = scheduled_on
        if project_id is not UNSET:
            properties["projectId"] = project_id
        if api_url is not UNSET:
            properties["apiURL"] = api_url
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Request":
        id = d["id"]

        created_at = isoparse(d["createdAt"])

        fields = d["fields"]

        display_id = d["displayId"]

        assignees = []
        for assignees_item_data in d["assignees"]:

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

        request_status = RequestStatus(d["requestStatus"])

        web_url = d["webURL"]

        scheduled_on = None
        if d.get("scheduledOn") is not None:
            scheduled_on = isoparse(cast(str, d.get("scheduledOn"))).date()

        project_id = d.get("projectId")

        api_url = d.get("apiURL")

        return Request(
            id=id,
            created_at=created_at,
            fields=fields,
            display_id=display_id,
            assignees=assignees,
            request_status=request_status,
            web_url=web_url,
            scheduled_on=scheduled_on,
            project_id=project_id,
            api_url=api_url,
        )
