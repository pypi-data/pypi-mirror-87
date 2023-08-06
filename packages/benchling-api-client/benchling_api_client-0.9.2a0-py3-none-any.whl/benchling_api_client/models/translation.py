from typing import Any, Dict, List, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class Translation:
    """  """

    start: Optional[int] = cast(None, UNSET)
    end: Optional[int] = cast(None, UNSET)
    strand: Optional[int] = cast(None, UNSET)
    amino_acids: Optional[str] = cast(None, UNSET)
    regions: Optional[List[Dict[Any, Any]]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        start = self.start
        end = self.end
        strand = self.strand
        amino_acids = self.amino_acids
        if self.regions is None:
            regions = None
        elif self.regions is UNSET:
            regions = UNSET
        else:
            regions = []
            for regions_item_data in self.regions:
                regions_item = regions_item_data

                regions.append(regions_item)

        properties: Dict[str, Any] = dict()

        if start is not UNSET:
            properties["start"] = start
        if end is not UNSET:
            properties["end"] = end
        if strand is not UNSET:
            properties["strand"] = strand
        if amino_acids is not UNSET:
            properties["aminoAcids"] = amino_acids
        if regions is not UNSET:
            properties["regions"] = regions
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Translation":
        start = d.get("start")

        end = d.get("end")

        strand = d.get("strand")

        amino_acids = d.get("aminoAcids")

        regions = []
        for regions_item_data in d.get("regions") or []:
            regions_item = regions_item_data

            regions.append(regions_item)

        return Translation(
            start=start,
            end=end,
            strand=strand,
            amino_acids=amino_acids,
            regions=regions,
        )
