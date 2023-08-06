import datetime
from typing import Any, Dict

import attr
from dateutil.parser import isoparse


@attr.s(auto_attribs=True)
class WarehouseCredentials:
    """  """

    expires_at: datetime.datetime
    username: str
    password: str

    def to_dict(self) -> Dict[str, Any]:
        expires_at = self.expires_at.isoformat()

        username = self.username
        password = self.password

        properties: Dict[str, Any] = dict()

        properties["expiresAt"] = expires_at
        properties["username"] = username
        properties["password"] = password
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "WarehouseCredentials":
        expires_at = isoparse(d["expiresAt"])

        username = d["username"]

        password = d["password"]

        return WarehouseCredentials(
            expires_at=expires_at,
            username=username,
            password=password,
        )
