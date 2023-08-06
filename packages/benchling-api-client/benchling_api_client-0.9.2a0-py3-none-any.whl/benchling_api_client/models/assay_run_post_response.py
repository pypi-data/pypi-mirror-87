from typing import Any, Dict, List, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class AssayRunPostResponse:
    """  """

    assay_runs: Optional[List[str]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.assay_runs is None:
            assay_runs = None
        elif self.assay_runs is UNSET:
            assay_runs = UNSET
        else:
            assay_runs = self.assay_runs

        properties: Dict[str, Any] = dict()

        if assay_runs is not UNSET:
            properties["assayRuns"] = assay_runs
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AssayRunPostResponse":
        assay_runs = d.get("assayRuns")

        return AssayRunPostResponse(
            assay_runs=assay_runs,
        )
