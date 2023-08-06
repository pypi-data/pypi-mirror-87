from typing import Any, Dict, List

import attr

from ..models.entry import Entry


@attr.s(auto_attribs=True)
class Entries:
    """  """

    entries: List[Entry]

    def to_dict(self) -> Dict[str, Any]:
        entries = []
        for entries_item_data in self.entries:
            entries_item = entries_item_data.to_dict()

            entries.append(entries_item)

        properties: Dict[str, Any] = dict()

        properties["entries"] = entries
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Entries":
        entries = []
        for entries_item_data in d["entries"]:
            entries_item = Entry.from_dict(entries_item_data)

            entries.append(entries_item)

        return Entries(
            entries=entries,
        )
