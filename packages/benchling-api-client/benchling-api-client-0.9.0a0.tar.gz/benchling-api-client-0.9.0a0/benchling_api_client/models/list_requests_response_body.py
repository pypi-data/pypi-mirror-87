from typing import Any, Dict, List, Optional, cast

import attr

from ..models.request import Request
from ..types import UNSET


@attr.s(auto_attribs=True)
class ListRequestsResponseBody:
    """  """

    requests: List[Request]
    next_token: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        requests = []
        for requests_item_data in self.requests:
            requests_item = requests_item_data.to_dict()

            requests.append(requests_item)

        next_token = self.next_token

        properties: Dict[str, Any] = dict()

        properties["requests"] = requests
        if next_token is not UNSET:
            properties["nextToken"] = next_token
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ListRequestsResponseBody":
        requests = []
        for requests_item_data in d["requests"]:
            requests_item = Request.from_dict(requests_item_data)

            requests.append(requests_item)

        next_token = d.get("nextToken")

        return ListRequestsResponseBody(
            requests=requests,
            next_token=next_token,
        )
