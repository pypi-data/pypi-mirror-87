from typing import Any, Dict, Optional, cast

import attr

from ..models.measurement import Measurement
from ..types import UNSET


@attr.s(auto_attribs=True)
class ContainerBulkUpdateItem:
    """  """

    container_id: str
    volume: Optional[Measurement] = cast(None, UNSET)
    fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    parent_storage_id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        container_id = self.container_id
        if self.volume is UNSET:
            volume = UNSET
        else:
            volume = self.volume.to_dict() if self.volume else None

        if self.fields is UNSET:
            fields = UNSET
        else:
            fields = self.fields if self.fields else None

        name = self.name
        parent_storage_id = self.parent_storage_id

        properties: Dict[str, Any] = dict()

        properties["containerId"] = container_id
        if volume is not UNSET:
            properties["volume"] = volume
        if fields is not UNSET:
            properties["fields"] = fields
        if name is not UNSET:
            properties["name"] = name
        if parent_storage_id is not UNSET:
            properties["parentStorageId"] = parent_storage_id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ContainerBulkUpdateItem":
        container_id = d["containerId"]

        volume = None
        if d.get("volume") is not None:
            volume = Measurement.from_dict(cast(Dict[str, Any], d.get("volume")))

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        name = d.get("name")

        parent_storage_id = d.get("parentStorageId")

        return ContainerBulkUpdateItem(
            container_id=container_id,
            volume=volume,
            fields=fields,
            name=name,
            parent_storage_id=parent_storage_id,
        )
