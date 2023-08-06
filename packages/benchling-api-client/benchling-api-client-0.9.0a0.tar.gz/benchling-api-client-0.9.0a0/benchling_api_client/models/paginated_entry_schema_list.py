from typing import Any, Dict, List

import attr

from ..models.entry_schema_detailed import EntrySchemaDetailed


@attr.s(auto_attribs=True)
class PaginatedEntrySchemaList:
    """  """

    entry_schemas: List[EntrySchemaDetailed]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        entry_schemas = []
        for entry_schemas_item_data in self.entry_schemas:
            entry_schemas_item = entry_schemas_item_data.to_dict()

            entry_schemas.append(entry_schemas_item)

        next_token = self.next_token

        properties: Dict[str, Any] = dict()

        properties["entrySchemas"] = entry_schemas
        properties["nextToken"] = next_token
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PaginatedEntrySchemaList":
        entry_schemas = []
        for entry_schemas_item_data in d["entrySchemas"]:
            entry_schemas_item = EntrySchemaDetailed.from_dict(entry_schemas_item_data)

            entry_schemas.append(entry_schemas_item)

        next_token = d["nextToken"]

        return PaginatedEntrySchemaList(
            entry_schemas=entry_schemas,
            next_token=next_token,
        )
