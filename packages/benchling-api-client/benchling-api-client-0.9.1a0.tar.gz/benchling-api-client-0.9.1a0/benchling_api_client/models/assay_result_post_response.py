from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class AssayResultPostResponse:
    """  """

    assay_results: List[str]

    def to_dict(self) -> Dict[str, Any]:
        assay_results = self.assay_results

        properties: Dict[str, Any] = dict()

        properties["assayResults"] = assay_results
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AssayResultPostResponse":
        assay_results = d["assayResults"]

        return AssayResultPostResponse(
            assay_results=assay_results,
        )
