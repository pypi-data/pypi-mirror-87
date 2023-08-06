from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class ForbiddenError:
    """  """

    error: Optional[Dict[Any, Any]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.error is UNSET:
            error = UNSET
        else:
            error = self.error if self.error else None

        properties: Dict[str, Any] = dict()

        if error is not UNSET:
            properties["error"] = error
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ForbiddenError":
        error = None
        if d.get("error") is not None:
            error = d.get("error")

        return ForbiddenError(
            error=error,
        )
