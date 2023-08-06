from typing import Any, Dict, List

import attr

from ..models.request_fulfillment import RequestFulfillment


@attr.s(auto_attribs=True)
class RequstFulfillmentsEnvelope:
    """ An object containing an array of RequestFulfillments """

    next_token: str
    request_fulfillments: List[RequestFulfillment]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        request_fulfillments = []
        for request_fulfillments_item_data in self.request_fulfillments:
            request_fulfillments_item = request_fulfillments_item_data.to_dict()

            request_fulfillments.append(request_fulfillments_item)

        properties: Dict[str, Any] = dict()

        properties["nextToken"] = next_token
        properties["requestFulfillments"] = request_fulfillments
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RequstFulfillmentsEnvelope":
        next_token = d["nextToken"]

        request_fulfillments = []
        for request_fulfillments_item_data in d["requestFulfillments"]:
            request_fulfillments_item = RequestFulfillment.from_dict(request_fulfillments_item_data)

            request_fulfillments.append(request_fulfillments_item)

        return RequstFulfillmentsEnvelope(
            next_token=next_token,
            request_fulfillments=request_fulfillments,
        )
