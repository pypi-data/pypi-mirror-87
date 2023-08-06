from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class PlateCreate:
    """  """

    schema_id: str
    barcode: Optional[str] = cast(None, UNSET)
    container_schema_id: Optional[str] = cast(None, UNSET)
    fields: Optional[Dict[Any, Any]] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    parent_storage_id: Optional[str] = cast(None, UNSET)
    project_id: Optional[str] = cast(None, UNSET)
    wells: Optional[Dict[Any, Any]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        schema_id = self.schema_id
        barcode = self.barcode
        container_schema_id = self.container_schema_id
        if self.fields is UNSET:
            fields = UNSET
        else:
            fields = self.fields if self.fields else None

        name = self.name
        parent_storage_id = self.parent_storage_id
        project_id = self.project_id
        if self.wells is UNSET:
            wells = UNSET
        else:
            wells = self.wells if self.wells else None

        properties: Dict[str, Any] = dict()

        properties["schemaId"] = schema_id
        if barcode is not UNSET:
            properties["barcode"] = barcode
        if container_schema_id is not UNSET:
            properties["containerSchemaId"] = container_schema_id
        if fields is not UNSET:
            properties["fields"] = fields
        if name is not UNSET:
            properties["name"] = name
        if parent_storage_id is not UNSET:
            properties["parentStorageId"] = parent_storage_id
        if project_id is not UNSET:
            properties["projectId"] = project_id
        if wells is not UNSET:
            properties["wells"] = wells
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PlateCreate":
        schema_id = d["schemaId"]

        barcode = d.get("barcode")

        container_schema_id = d.get("containerSchemaId")

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        name = d.get("name")

        parent_storage_id = d.get("parentStorageId")

        project_id = d.get("projectId")

        wells = None
        if d.get("wells") is not None:
            wells = d.get("wells")

        return PlateCreate(
            schema_id=schema_id,
            barcode=barcode,
            container_schema_id=container_schema_id,
            fields=fields,
            name=name,
            parent_storage_id=parent_storage_id,
            project_id=project_id,
            wells=wells,
        )
