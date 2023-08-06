from typing import Any, Dict, List, Optional, cast

import attr

from ..models.entry_link import EntryLink
from ..models.entry_table import EntryTable
from ..models.type1234 import Type1234
from ..types import UNSET


@attr.s(auto_attribs=True)
class NotePart:
    """Notes are the main building blocks of entries. Each note corresponds roughly to a paragraph and has one of these types: - 'text': plain text - 'code': preformatted code block - 'table': a table with rows and columns of text - 'list_bullet': one "line" of a bulleted list - 'list_number': one "line" of a numbered list - 'list_checkbox': one "line" of a checklist - 'external_file': an attached user-uploaded file"""

    type: Optional[Type1234] = cast(None, UNSET)
    indentation: Optional[int] = cast(None, UNSET)
    text: Optional[str] = cast(None, UNSET)
    links: Optional[List[EntryLink]] = cast(None, UNSET)
    checked: Optional[bool] = cast(None, UNSET)
    table: Optional[EntryTable] = cast(None, UNSET)
    external_file_id: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.type is UNSET:
            type = UNSET
        else:
            type = self.type.value if self.type else None

        indentation = self.indentation
        text = self.text
        if self.links is None:
            links = None
        elif self.links is UNSET:
            links = UNSET
        else:
            links = []
            for links_item_data in self.links:
                links_item = links_item_data.to_dict()

                links.append(links_item)

        checked = self.checked
        if self.table is UNSET:
            table = UNSET
        else:
            table = self.table.to_dict() if self.table else None

        external_file_id = self.external_file_id

        properties: Dict[str, Any] = dict()

        if type is not UNSET:
            properties["type"] = type
        if indentation is not UNSET:
            properties["indentation"] = indentation
        if text is not UNSET:
            properties["text"] = text
        if links is not UNSET:
            properties["links"] = links
        if checked is not UNSET:
            properties["checked"] = checked
        if table is not UNSET:
            properties["table"] = table
        if external_file_id is not UNSET:
            properties["externalFileId"] = external_file_id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NotePart":
        type = None
        if d.get("type") is not None:
            type = Type1234(d.get("type"))

        indentation = d.get("indentation")

        text = d.get("text")

        links = []
        for links_item_data in d.get("links") or []:
            links_item = EntryLink.from_dict(links_item_data)

            links.append(links_item)

        checked = d.get("checked")

        table = None
        if d.get("table") is not None:
            table = EntryTable.from_dict(cast(Dict[str, Any], d.get("table")))

        external_file_id = d.get("externalFileId")

        return NotePart(
            type=type,
            indentation=indentation,
            text=text,
            links=links,
            checked=checked,
            table=table,
            external_file_id=external_file_id,
        )
