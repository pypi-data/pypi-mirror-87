from typing import Any, Dict, Optional, cast

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class SampleGroup:
    """ Represents a sample group that is an input to a request. A sample group is a set of samples upon which work in the request should be done. """

    id: Optional[str] = cast(None, UNSET)
    samples: Optional[Dict[Any, Any]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        if self.samples is UNSET:
            samples = UNSET
        else:
            samples = self.samples if self.samples else None

        properties: Dict[str, Any] = dict()

        if id is not UNSET:
            properties["id"] = id
        if samples is not UNSET:
            properties["samples"] = samples
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SampleGroup":
        id = d.get("id")

        samples = None
        if d.get("samples") is not None:
            samples = d.get("samples")

        return SampleGroup(
            id=id,
            samples=samples,
        )
