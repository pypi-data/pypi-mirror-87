from typing import Any, Dict, List, Optional, cast

import attr

from ..models.assay_result import AssayResult
from ..types import UNSET


@attr.s(auto_attribs=True)
class RequestResponse:
    """  """

    samples: Optional[List[Dict[Any, Any]]] = cast(None, UNSET)
    results: Optional[List[AssayResult]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.samples is None:
            samples = None
        elif self.samples is UNSET:
            samples = UNSET
        else:
            samples = []
            for samples_item_data in self.samples:
                samples_item = samples_item_data

                samples.append(samples_item)

        if self.results is None:
            results = None
        elif self.results is UNSET:
            results = UNSET
        else:
            results = []
            for results_item_data in self.results:
                results_item = results_item_data.to_dict()

                results.append(results_item)

        properties: Dict[str, Any] = dict()

        if samples is not UNSET:
            properties["samples"] = samples
        if results is not UNSET:
            properties["results"] = results
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RequestResponse":
        samples = []
        for samples_item_data in d.get("samples") or []:
            samples_item = samples_item_data

            samples.append(samples_item)

        results = []
        for results_item_data in d.get("results") or []:
            results_item = AssayResult.from_dict(results_item_data)

            results.append(results_item)

        return RequestResponse(
            samples=samples,
            results=results,
        )
