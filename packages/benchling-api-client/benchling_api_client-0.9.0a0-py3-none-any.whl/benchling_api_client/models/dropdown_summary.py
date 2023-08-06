from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class DropdownSummary:
    """  """

    name: str
    id: str

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id

        properties: Dict[str, Any] = dict()

        properties["name"] = name
        properties["id"] = id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DropdownSummary":
        name = d["name"]

        id = d["id"]

        return DropdownSummary(
            name=name,
            id=id,
        )
