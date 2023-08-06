from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class ContainerArchiveResponse:
    """IDs of all items that were unarchived, grouped by resource type. This includes the IDs of containers that were unarchived."""

    container_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        container_ids = self.container_ids

        properties: Dict[str, Any] = dict()

        properties["containerIds"] = container_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ContainerArchiveResponse":
        container_ids = d["containerIds"]

        return ContainerArchiveResponse(
            container_ids=container_ids,
        )
