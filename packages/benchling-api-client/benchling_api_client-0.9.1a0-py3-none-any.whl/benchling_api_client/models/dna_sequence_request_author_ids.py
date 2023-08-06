from typing import Any, Dict, List, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class DnaSequenceRequestAuthorIds:
    """  """

    author_ids: Optional[List[str]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.author_ids is None:
            author_ids = None
        elif self.author_ids is UNSET:
            author_ids = UNSET
        else:
            author_ids = self.author_ids

        properties: Dict[str, Any] = dict()

        if author_ids is not UNSET:
            properties["authorIds"] = author_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DnaSequenceRequestAuthorIds":
        author_ids = d.get("authorIds")

        return DnaSequenceRequestAuthorIds(
            author_ids=author_ids,
        )
