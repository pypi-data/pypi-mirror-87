from typing import Any, Dict, List

import attr

from ..models.assay_result_schema import AssayResultSchema


@attr.s(auto_attribs=True)
class PaginatedAssayResultSchemaList:
    """  """

    assay_result_schemas: List[AssayResultSchema]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        assay_result_schemas = []
        for assay_result_schemas_item_data in self.assay_result_schemas:
            assay_result_schemas_item = assay_result_schemas_item_data.to_dict()

            assay_result_schemas.append(assay_result_schemas_item)

        next_token = self.next_token

        properties: Dict[str, Any] = dict()

        properties["assayResultSchemas"] = assay_result_schemas
        properties["nextToken"] = next_token
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PaginatedAssayResultSchemaList":
        assay_result_schemas = []
        for assay_result_schemas_item_data in d["assayResultSchemas"]:
            assay_result_schemas_item = AssayResultSchema.from_dict(assay_result_schemas_item_data)

            assay_result_schemas.append(assay_result_schemas_item)

        next_token = d["nextToken"]

        return PaginatedAssayResultSchemaList(
            assay_result_schemas=assay_result_schemas,
            next_token=next_token,
        )
