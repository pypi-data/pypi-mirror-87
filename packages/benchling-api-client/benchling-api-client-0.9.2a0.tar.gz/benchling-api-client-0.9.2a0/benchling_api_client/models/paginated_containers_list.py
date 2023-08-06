from typing import Any, Dict, List

import attr

from ..models.container import Container


@attr.s(auto_attribs=True)
class PaginatedContainersList:
    """  """

    next_token: str
    containers: List[Container]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        containers = []
        for containers_item_data in self.containers:
            containers_item = containers_item_data.to_dict()

            containers.append(containers_item)

        properties: Dict[str, Any] = dict()

        properties["nextToken"] = next_token
        properties["containers"] = containers
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PaginatedContainersList":
        next_token = d["nextToken"]

        containers = []
        for containers_item_data in d["containers"]:
            containers_item = Container.from_dict(containers_item_data)

            containers.append(containers_item)

        return PaginatedContainersList(
            next_token=next_token,
            containers=containers,
        )
