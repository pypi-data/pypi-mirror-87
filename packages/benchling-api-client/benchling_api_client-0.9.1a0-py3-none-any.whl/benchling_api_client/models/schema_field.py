from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class SchemaField:
    """  """

    is_required: Optional[bool] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        is_required = self.is_required
        name = self.name

        properties: Dict[str, Any] = dict()

        if is_required is not UNSET:
            properties["isRequired"] = is_required
        if name is not UNSET:
            properties["name"] = name
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SchemaField":
        is_required = d.get("isRequired")

        name = d.get("name")

        return SchemaField(
            is_required=is_required,
            name=name,
        )
