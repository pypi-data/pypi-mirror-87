from typing import Any, Dict, List

import attr

from ..models.container_bulk_update_item import ContainerBulkUpdateItem


@attr.s(auto_attribs=True)
class ContainerBulkUpdateRequestBody:
    """  """

    containers: List[ContainerBulkUpdateItem]

    def to_dict(self) -> Dict[str, Any]:
        containers = []
        for containers_item_data in self.containers:
            containers_item = containers_item_data.to_dict()

            containers.append(containers_item)

        properties: Dict[str, Any] = dict()

        properties["containers"] = containers
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ContainerBulkUpdateRequestBody":
        containers = []
        for containers_item_data in d["containers"]:
            containers_item = ContainerBulkUpdateItem.from_dict(containers_item_data)

            containers.append(containers_item)

        return ContainerBulkUpdateRequestBody(
            containers=containers,
        )
