from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class AssayRunPatch:
    """  """

    fields: Optional[Dict[Any, Any]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.fields is UNSET:
            fields = UNSET
        else:
            fields = self.fields if self.fields else None

        properties: Dict[str, Any] = dict()

        if fields is not UNSET:
            properties["fields"] = fields
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AssayRunPatch":
        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        return AssayRunPatch(
            fields=fields,
        )
