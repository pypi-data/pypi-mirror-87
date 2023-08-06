from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class Protein:
    """  """

    def to_dict(self) -> Dict[str, Any]:

        properties: Dict[str, Any] = dict()

        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Protein":
        return Protein()
