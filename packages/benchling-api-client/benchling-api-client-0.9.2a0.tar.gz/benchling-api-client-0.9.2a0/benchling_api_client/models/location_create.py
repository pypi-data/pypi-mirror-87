from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class LocationCreate:
    """  """

    name: str
    schema_id: str
    barcode: Optional[str] = cast(None, UNSET)
    fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    parent_storage_id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        schema_id = self.schema_id
        barcode = self.barcode
        if self.fields is UNSET:
            fields = UNSET
        else:
            fields = self.fields if self.fields else None

        parent_storage_id = self.parent_storage_id

        properties: Dict[str, Any] = dict()

        properties["name"] = name
        properties["schemaId"] = schema_id
        if barcode is not UNSET:
            properties["barcode"] = barcode
        if fields is not UNSET:
            properties["fields"] = fields
        if parent_storage_id is not UNSET:
            properties["parentStorageId"] = parent_storage_id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "LocationCreate":
        name = d["name"]

        schema_id = d["schemaId"]

        barcode = d.get("barcode")

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        parent_storage_id = d.get("parentStorageId")

        return LocationCreate(
            name=name,
            schema_id=schema_id,
            barcode=barcode,
            fields=fields,
            parent_storage_id=parent_storage_id,
        )
