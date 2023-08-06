from typing import Any, Dict, List

import attr

from ..models.assay_result_create import AssayResultCreate


@attr.s(auto_attribs=True)
class AssayResultBulkCreate:
    """  """

    assay_results: List[AssayResultCreate]

    def to_dict(self) -> Dict[str, Any]:
        assay_results = []
        for assay_results_item_data in self.assay_results:
            assay_results_item = assay_results_item_data.to_dict()

            assay_results.append(assay_results_item)

        properties: Dict[str, Any] = dict()

        properties["assayResults"] = assay_results
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AssayResultBulkCreate":
        assay_results = []
        for assay_results_item_data in d["assayResults"]:
            assay_results_item = AssayResultCreate.from_dict(assay_results_item_data)

            assay_results.append(assay_results_item)

        return AssayResultBulkCreate(
            assay_results=assay_results,
        )
