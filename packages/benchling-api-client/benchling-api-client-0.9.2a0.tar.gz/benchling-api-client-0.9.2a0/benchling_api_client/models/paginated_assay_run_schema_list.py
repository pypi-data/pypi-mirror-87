from typing import Any, Dict, List

import attr

from ..models.assay_run_schema import AssayRunSchema


@attr.s(auto_attribs=True)
class PaginatedAssayRunSchemaList:
    """  """

    assay_run_schemas: List[AssayRunSchema]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        assay_run_schemas = []
        for assay_run_schemas_item_data in self.assay_run_schemas:
            assay_run_schemas_item = assay_run_schemas_item_data.to_dict()

            assay_run_schemas.append(assay_run_schemas_item)

        next_token = self.next_token

        properties: Dict[str, Any] = dict()

        properties["assayRunSchemas"] = assay_run_schemas
        properties["nextToken"] = next_token
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PaginatedAssayRunSchemaList":
        assay_run_schemas = []
        for assay_run_schemas_item_data in d["assayRunSchemas"]:
            assay_run_schemas_item = AssayRunSchema.from_dict(assay_run_schemas_item_data)

            assay_run_schemas.append(assay_run_schemas_item)

        next_token = d["nextToken"]

        return PaginatedAssayRunSchemaList(
            assay_run_schemas=assay_run_schemas,
            next_token=next_token,
        )
