from typing import Any, Dict, List

import attr

from ..models.assay_result import AssayResult


@attr.s(auto_attribs=True)
class AssayResultBulkGet:
    """  """

    assay_results: List[AssayResult]

    def to_dict(self) -> Dict[str, Any]:
        assay_results = []
        for assay_results_item_data in self.assay_results:
            assay_results_item = assay_results_item_data.to_dict()

            assay_results.append(assay_results_item)

        properties: Dict[str, Any] = dict()

        properties["assayResults"] = assay_results
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AssayResultBulkGet":
        assay_results = []
        for assay_results_item_data in d["assayResults"]:
            assay_results_item = AssayResult.from_dict(assay_results_item_data)

            assay_results.append(assay_results_item)

        return AssayResultBulkGet(
            assay_results=assay_results,
        )
