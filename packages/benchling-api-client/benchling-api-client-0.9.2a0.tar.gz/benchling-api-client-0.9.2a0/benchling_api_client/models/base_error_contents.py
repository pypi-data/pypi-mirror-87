from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class BaseErrorContents:
    """  """

    message: Optional[str] = cast(None, UNSET)
    type: Optional[str] = cast(None, UNSET)
    user_message: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        message = self.message
        type = self.type
        user_message = self.user_message

        properties: Dict[str, Any] = dict()

        if message is not UNSET:
            properties["message"] = message
        if type is not UNSET:
            properties["type"] = type
        if user_message is not UNSET:
            properties["userMessage"] = user_message
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BaseErrorContents":
        message = d.get("message")

        type = d.get("type")

        user_message = d.get("userMessage")

        return BaseErrorContents(
            message=message,
            type=type,
            user_message=user_message,
        )
