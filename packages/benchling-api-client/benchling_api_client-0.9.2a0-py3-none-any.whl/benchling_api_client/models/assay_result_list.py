from typing import Any, Dict, List

import attr

from ..models.assay_result import AssayResult


@attr.s(auto_attribs=True)
class AssayResultList:
    """  """

    assay_results: List[AssayResult]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        assay_results = []
        for assay_results_item_data in self.assay_results:
            assay_results_item = assay_results_item_data.to_dict()

            assay_results.append(assay_results_item)

        next_token = self.next_token

        properties: Dict[str, Any] = dict()

        properties["assayResults"] = assay_results
        properties["nextToken"] = next_token
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AssayResultList":
        assay_results = []
        for assay_results_item_data in d["assayResults"]:
            assay_results_item = AssayResult.from_dict(assay_results_item_data)

            assay_results.append(assay_results_item)

        next_token = d["nextToken"]

        return AssayResultList(
            assay_results=assay_results,
            next_token=next_token,
        )
