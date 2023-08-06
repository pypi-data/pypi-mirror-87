from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class BlobPart:
    """  """

    part_number: Optional[int] = cast(None, UNSET)
    e_tag: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        part_number = self.part_number
        e_tag = self.e_tag

        properties: Dict[str, Any] = dict()

        if part_number is not UNSET:
            properties["partNumber"] = part_number
        if e_tag is not UNSET:
            properties["eTag"] = e_tag
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BlobPart":
        part_number = d.get("partNumber")

        e_tag = d.get("eTag")

        return BlobPart(
            part_number=part_number,
            e_tag=e_tag,
        )
