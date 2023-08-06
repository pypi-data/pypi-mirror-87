from typing import Any, Dict, List

import attr

from ..models.assay_run_create import AssayRunCreate


@attr.s(auto_attribs=True)
class AssayRunBulkCreate:
    """  """

    assay_runs: List[AssayRunCreate]

    def to_dict(self) -> Dict[str, Any]:
        assay_runs = []
        for assay_runs_item_data in self.assay_runs:
            assay_runs_item = assay_runs_item_data.to_dict()

            assay_runs.append(assay_runs_item)

        properties: Dict[str, Any] = dict()

        properties["assayRuns"] = assay_runs
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AssayRunBulkCreate":
        assay_runs = []
        for assay_runs_item_data in d["assayRuns"]:
            assay_runs_item = AssayRunCreate.from_dict(assay_runs_item_data)

            assay_runs.append(assay_runs_item)

        return AssayRunBulkCreate(
            assay_runs=assay_runs,
        )
