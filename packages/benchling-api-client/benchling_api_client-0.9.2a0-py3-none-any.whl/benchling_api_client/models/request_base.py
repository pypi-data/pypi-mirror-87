from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class RequestBase:
    """ A request is an ask to perform a service, e.g. produce a sample or perform assays on a sample. Requests are usually placed to another team or individual who specializes in performing the service. """

    def to_dict(self) -> Dict[str, Any]:

        properties: Dict[str, Any] = dict()

        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RequestBase":
        return RequestBase()
