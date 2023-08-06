from typing import Any, Dict, Optional, cast

import attr

from ..models.entry_link import EntryLink
from ..types import UNSET


@attr.s(auto_attribs=True)
class EntryTableCell:
    """  """

    text: Optional[str] = cast(None, UNSET)
    link: Optional[EntryLink] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        text = self.text
        if self.link is UNSET:
            link = UNSET
        else:
            link = self.link.to_dict() if self.link else None

        properties: Dict[str, Any] = dict()

        if text is not UNSET:
            properties["text"] = text
        if link is not UNSET:
            properties["link"] = link
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EntryTableCell":
        text = d.get("text")

        link = None
        if d.get("link") is not None:
            link = EntryLink.from_dict(cast(Dict[str, Any], d.get("link")))

        return EntryTableCell(
            text=text,
            link=link,
        )
