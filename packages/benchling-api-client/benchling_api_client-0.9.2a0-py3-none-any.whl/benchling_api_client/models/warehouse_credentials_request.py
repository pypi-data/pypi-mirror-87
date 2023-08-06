from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class WarehouseCredentialsRequest:
    """  """

    expires_in: int

    def to_dict(self) -> Dict[str, Any]:
        expires_in = self.expires_in

        properties: Dict[str, Any] = dict()

        properties["expiresIn"] = expires_in
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "WarehouseCredentialsRequest":
        expires_in = d["expiresIn"]

        return WarehouseCredentialsRequest(
            expires_in=expires_in,
        )
