from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class AssayResultIds:
    """  """

    assay_result_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        assay_result_ids = self.assay_result_ids

        properties: Dict[str, Any] = dict()

        properties["assayResultIds"] = assay_result_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AssayResultIds":
        assay_result_ids = d["assayResultIds"]

        return AssayResultIds(
            assay_result_ids=assay_result_ids,
        )
