from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class AssayResultTransactionPostResponse:
    """  """

    id: str

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        properties: Dict[str, Any] = dict()

        properties["id"] = id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AssayResultTransactionPostResponse":
        id = d["id"]

        return AssayResultTransactionPostResponse(
            id=id,
        )
