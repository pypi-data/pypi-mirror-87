from typing import Any, Dict, List

import attr

from ..models.entry import Entry


@attr.s(auto_attribs=True)
class EntryList:
    """  """

    next_token: str
    entries: List[Entry]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        entries = []
        for entries_item_data in self.entries:
            entries_item = entries_item_data.to_dict()

            entries.append(entries_item)

        properties: Dict[str, Any] = dict()

        properties["nextToken"] = next_token
        properties["entries"] = entries
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EntryList":
        next_token = d["nextToken"]

        entries = []
        for entries_item_data in d["entries"]:
            entries_item = Entry.from_dict(entries_item_data)

            entries.append(entries_item)

        return EntryList(
            next_token=next_token,
            entries=entries,
        )
