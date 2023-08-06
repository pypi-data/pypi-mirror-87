from typing import Any, Dict, List

import attr

from ..models.request import Request


@attr.s(auto_attribs=True)
class RequestsBulkGetResponseBody:
    """  """

    requests: List[Request]

    def to_dict(self) -> Dict[str, Any]:
        requests = []
        for requests_item_data in self.requests:
            requests_item = requests_item_data.to_dict()

            requests.append(requests_item)

        properties: Dict[str, Any] = dict()

        properties["requests"] = requests
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RequestsBulkGetResponseBody":
        requests = []
        for requests_item_data in d["requests"]:
            requests_item = Request.from_dict(requests_item_data)

            requests.append(requests_item)

        return RequestsBulkGetResponseBody(
            requests=requests,
        )
