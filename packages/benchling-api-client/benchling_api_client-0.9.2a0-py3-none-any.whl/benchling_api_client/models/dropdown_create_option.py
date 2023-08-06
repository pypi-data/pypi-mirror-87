from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class DropdownCreateOption:
    """  """

    name: str

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        properties: Dict[str, Any] = dict()

        properties["name"] = name
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DropdownCreateOption":
        name = d["name"]

        return DropdownCreateOption(
            name=name,
        )
