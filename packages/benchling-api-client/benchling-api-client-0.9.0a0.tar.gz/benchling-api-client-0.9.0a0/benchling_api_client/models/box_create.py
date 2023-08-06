from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class BoxCreate:
    """  """

    schema_id: str
    barcode: Optional[str] = cast(None, UNSET)
    fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    parent_storage_id: Optional[str] = cast(None, UNSET)
    project_id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        schema_id = self.schema_id
        barcode = self.barcode
        if self.fields is UNSET:
            fields = UNSET
        else:
            fields = self.fields if self.fields else None

        name = self.name
        parent_storage_id = self.parent_storage_id
        project_id = self.project_id

        properties: Dict[str, Any] = dict()

        properties["schemaId"] = schema_id
        if barcode is not UNSET:
            properties["barcode"] = barcode
        if fields is not UNSET:
            properties["fields"] = fields
        if name is not UNSET:
            properties["name"] = name
        if parent_storage_id is not UNSET:
            properties["parentStorageId"] = parent_storage_id
        if project_id is not UNSET:
            properties["projectId"] = project_id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BoxCreate":
        schema_id = d["schemaId"]

        barcode = d.get("barcode")

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        name = d.get("name")

        parent_storage_id = d.get("parentStorageId")

        project_id = d.get("projectId")

        return BoxCreate(
            schema_id=schema_id,
            barcode=barcode,
            fields=fields,
            name=name,
            parent_storage_id=parent_storage_id,
            project_id=project_id,
        )
