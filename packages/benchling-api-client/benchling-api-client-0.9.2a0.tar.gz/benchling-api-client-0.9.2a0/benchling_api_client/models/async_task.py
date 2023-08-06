from typing import Any, Dict, Optional, cast

import attr

from ..models.status1 import Status1
from ..types import UNSET


@attr.s(auto_attribs=True)
class AsyncTask:
    """  """

    status: Status1
    response: Optional[Dict[Any, Any]] = cast(None, UNSET)
    message: Optional[str] = cast(None, UNSET)
    errors: Optional[Dict[Any, Any]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        if self.response is UNSET:
            response = UNSET
        else:
            response = self.response if self.response else None

        message = self.message
        if self.errors is UNSET:
            errors = UNSET
        else:
            errors = self.errors if self.errors else None

        properties: Dict[str, Any] = dict()

        properties["status"] = status
        if response is not UNSET:
            properties["response"] = response
        if message is not UNSET:
            properties["message"] = message
        if errors is not UNSET:
            properties["errors"] = errors
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AsyncTask":
        status = Status1(d["status"])

        response = None
        if d.get("response") is not None:
            response = d.get("response")

        message = d.get("message")

        errors = None
        if d.get("errors") is not None:
            errors = d.get("errors")

        return AsyncTask(
            status=status,
            response=response,
            message=message,
            errors=errors,
        )
