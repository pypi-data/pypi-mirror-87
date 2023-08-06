from typing import Any, Dict, List

import attr

from ..models.registry import Registry


@attr.s(auto_attribs=True)
class RegistryList:
    """  """

    registries: List[Registry]

    def to_dict(self) -> Dict[str, Any]:
        registries = []
        for registries_item_data in self.registries:
            registries_item = registries_item_data.to_dict()

            registries.append(registries_item)

        properties: Dict[str, Any] = dict()

        properties["registries"] = registries
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RegistryList":
        registries = []
        for registries_item_data in d["registries"]:
            registries_item = Registry.from_dict(registries_item_data)

            registries.append(registries_item)

        return RegistryList(
            registries=registries,
        )
