from typing import Any, Dict, List, Optional, cast

import attr

from ..models.entry_table_row import EntryTableRow
from ..types import UNSET


@attr.s(auto_attribs=True)
class EntryTable:
    """Actual tabular data with rows and columns of text on the note."""

    name: Optional[str] = cast(None, UNSET)
    column_labels: Optional[List[Optional[str]]] = cast(None, UNSET)
    rows: Optional[List[EntryTableRow]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        if self.column_labels is None:
            column_labels = None
        elif self.column_labels is UNSET:
            column_labels = UNSET
        else:
            column_labels = self.column_labels

        if self.rows is None:
            rows = None
        elif self.rows is UNSET:
            rows = UNSET
        else:
            rows = []
            for rows_item_data in self.rows:
                rows_item = rows_item_data.to_dict()

                rows.append(rows_item)

        properties: Dict[str, Any] = dict()

        if name is not UNSET:
            properties["name"] = name
        if column_labels is not UNSET:
            properties["columnLabels"] = column_labels
        if rows is not UNSET:
            properties["rows"] = rows
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EntryTable":
        name = d.get("name")

        column_labels = d.get("columnLabels")

        rows = []
        for rows_item_data in d.get("rows") or []:
            rows_item = EntryTableRow.from_dict(rows_item_data)

            rows.append(rows_item)

        return EntryTable(
            name=name,
            column_labels=column_labels,
            rows=rows,
        )
