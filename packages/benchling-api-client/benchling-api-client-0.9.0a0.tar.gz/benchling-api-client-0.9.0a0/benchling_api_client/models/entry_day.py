from typing import Any, Dict, List, Optional, cast

import attr

from ..models.note_part import NotePart
from ..types import UNSET


@attr.s(auto_attribs=True)
class EntryDay:
    """  """

    date: Optional[str] = cast(None, UNSET)
    notes: Optional[List[NotePart]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        date = self.date
        if self.notes is None:
            notes = None
        elif self.notes is UNSET:
            notes = UNSET
        else:
            notes = []
            for notes_item_data in self.notes:
                notes_item = notes_item_data.to_dict()

                notes.append(notes_item)

        properties: Dict[str, Any] = dict()

        if date is not UNSET:
            properties["date"] = date
        if notes is not UNSET:
            properties["notes"] = notes
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EntryDay":
        date = d.get("date")

        notes = []
        for notes_item_data in d.get("notes") or []:
            notes_item = NotePart.from_dict(notes_item_data)

            notes.append(notes_item)

        return EntryDay(
            date=date,
            notes=notes,
        )
