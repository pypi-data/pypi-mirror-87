from typing import Any, Dict, List

import attr

from ..models.assay_run import AssayRun


@attr.s(auto_attribs=True)
class AssayRunList:
    """  """

    assay_runs: List[AssayRun]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        assay_runs = []
        for assay_runs_item_data in self.assay_runs:
            assay_runs_item = assay_runs_item_data.to_dict()

            assay_runs.append(assay_runs_item)

        next_token = self.next_token

        properties: Dict[str, Any] = dict()

        properties["assayRuns"] = assay_runs
        properties["nextToken"] = next_token
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AssayRunList":
        assay_runs = []
        for assay_runs_item_data in d["assayRuns"]:
            assay_runs_item = AssayRun.from_dict(assay_runs_item_data)

            assay_runs.append(assay_runs_item)

        next_token = d["nextToken"]

        return AssayRunList(
            assay_runs=assay_runs,
            next_token=next_token,
        )
