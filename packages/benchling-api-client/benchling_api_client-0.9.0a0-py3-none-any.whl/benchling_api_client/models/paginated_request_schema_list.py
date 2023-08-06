from typing import Any, Dict, List

import attr

from ..models.request_schema import RequestSchema


@attr.s(auto_attribs=True)
class PaginatedRequestSchemaList:
    """  """

    request_schemas: List[RequestSchema]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        request_schemas = []
        for request_schemas_item_data in self.request_schemas:
            request_schemas_item = request_schemas_item_data.to_dict()

            request_schemas.append(request_schemas_item)

        next_token = self.next_token

        properties: Dict[str, Any] = dict()

        properties["requestSchemas"] = request_schemas
        properties["nextToken"] = next_token
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PaginatedRequestSchemaList":
        request_schemas = []
        for request_schemas_item_data in d["requestSchemas"]:
            request_schemas_item = RequestSchema.from_dict(request_schemas_item_data)

            request_schemas.append(request_schemas_item)

        next_token = d["nextToken"]

        return PaginatedRequestSchemaList(
            request_schemas=request_schemas,
            next_token=next_token,
        )
