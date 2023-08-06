from typing import Any, Dict, List, Optional, cast

import attr

from ..models.barcode_validation_result import BarcodeValidationResult
from ..types import UNSET


@attr.s(auto_attribs=True)
class BarcodeValidationResults:
    """  """

    validation_results: Optional[List[BarcodeValidationResult]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.validation_results is None:
            validation_results = None
        elif self.validation_results is UNSET:
            validation_results = UNSET
        else:
            validation_results = []
            for validation_results_item_data in self.validation_results:
                validation_results_item = validation_results_item_data.to_dict()

                validation_results.append(validation_results_item)

        properties: Dict[str, Any] = dict()

        if validation_results is not UNSET:
            properties["validationResults"] = validation_results
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BarcodeValidationResults":
        validation_results = []
        for validation_results_item_data in d.get("validationResults") or []:
            validation_results_item = BarcodeValidationResult.from_dict(validation_results_item_data)

            validation_results.append(validation_results_item)

        return BarcodeValidationResults(
            validation_results=validation_results,
        )
