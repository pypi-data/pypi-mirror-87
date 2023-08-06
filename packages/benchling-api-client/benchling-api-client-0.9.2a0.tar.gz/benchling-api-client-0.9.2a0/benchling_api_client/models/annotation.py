from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class Annotation:
    """  """

    color: Optional[str] = cast(None, UNSET)
    start: Optional[int] = cast(None, UNSET)
    end: Optional[int] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    strand: Optional[int] = cast(None, UNSET)
    type: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        color = self.color
        start = self.start
        end = self.end
        name = self.name
        strand = self.strand
        type = self.type

        properties: Dict[str, Any] = dict()

        if color is not UNSET:
            properties["color"] = color
        if start is not UNSET:
            properties["start"] = start
        if end is not UNSET:
            properties["end"] = end
        if name is not UNSET:
            properties["name"] = name
        if strand is not UNSET:
            properties["strand"] = strand
        if type is not UNSET:
            properties["type"] = type
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Annotation":
        color = d.get("color")

        start = d.get("start")

        end = d.get("end")

        name = d.get("name")

        strand = d.get("strand")

        type = d.get("type")

        return Annotation(
            color=color,
            start=start,
            end=end,
            name=name,
            strand=strand,
            type=type,
        )
