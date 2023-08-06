from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class Primer:
    """  """

    bases: Optional[str] = cast(None, UNSET)
    bind_position: Optional[int] = cast(None, UNSET)
    color: Optional[str] = cast(None, UNSET)
    start: Optional[int] = cast(None, UNSET)
    end: Optional[int] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    oligo_id: Optional[str] = cast(None, UNSET)
    overhang_length: Optional[int] = cast(None, UNSET)
    strand: Optional[int] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        bases = self.bases
        bind_position = self.bind_position
        color = self.color
        start = self.start
        end = self.end
        name = self.name
        oligo_id = self.oligo_id
        overhang_length = self.overhang_length
        strand = self.strand

        properties: Dict[str, Any] = dict()

        if bases is not UNSET:
            properties["bases"] = bases
        if bind_position is not UNSET:
            properties["bindPosition"] = bind_position
        if color is not UNSET:
            properties["color"] = color
        if start is not UNSET:
            properties["start"] = start
        if end is not UNSET:
            properties["end"] = end
        if name is not UNSET:
            properties["name"] = name
        if oligo_id is not UNSET:
            properties["oligoId"] = oligo_id
        if overhang_length is not UNSET:
            properties["overhangLength"] = overhang_length
        if strand is not UNSET:
            properties["strand"] = strand
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Primer":
        bases = d.get("bases")

        bind_position = d.get("bindPosition")

        color = d.get("color")

        start = d.get("start")

        end = d.get("end")

        name = d.get("name")

        oligo_id = d.get("oligoId")

        overhang_length = d.get("overhangLength")

        strand = d.get("strand")

        return Primer(
            bases=bases,
            bind_position=bind_position,
            color=color,
            start=start,
            end=end,
            name=name,
            oligo_id=oligo_id,
            overhang_length=overhang_length,
            strand=strand,
        )
