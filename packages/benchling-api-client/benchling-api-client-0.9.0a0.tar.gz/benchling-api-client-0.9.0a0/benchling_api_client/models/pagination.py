from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class Pagination:
    """  """

    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token

        properties: Dict[str, Any] = dict()

        properties["nextToken"] = next_token
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Pagination":
        next_token = d["nextToken"]

        return Pagination(
            next_token=next_token,
        )
