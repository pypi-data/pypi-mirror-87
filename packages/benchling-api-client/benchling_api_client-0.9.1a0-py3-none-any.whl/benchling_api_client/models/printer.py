from typing import Any, Dict, Optional

import attr


@attr.s(auto_attribs=True)
class Printer:
    """  """

    address: str
    description: Optional[str]
    id: str
    name: str
    port: Optional[int]
    registry_id: str

    def to_dict(self) -> Dict[str, Any]:
        address = self.address
        description = self.description
        id = self.id
        name = self.name
        port = self.port
        registry_id = self.registry_id

        properties: Dict[str, Any] = dict()

        properties["address"] = address
        properties["description"] = description
        properties["id"] = id
        properties["name"] = name
        properties["port"] = port
        properties["registryId"] = registry_id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Printer":
        address = d["address"]

        description = d["description"]

        id = d["id"]

        name = d["name"]

        port = d["port"]

        registry_id = d["registryId"]

        return Printer(
            address=address,
            description=description,
            id=id,
            name=name,
            port=port,
            registry_id=registry_id,
        )
