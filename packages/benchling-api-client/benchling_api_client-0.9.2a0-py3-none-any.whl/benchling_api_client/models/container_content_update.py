from typing import Any, Dict

import attr

from ..models.measurement import Measurement


@attr.s(auto_attribs=True)
class ContainerContentUpdate:
    """  """

    concentration: Measurement

    def to_dict(self) -> Dict[str, Any]:
        concentration = self.concentration.to_dict()

        properties: Dict[str, Any] = dict()

        properties["concentration"] = concentration
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ContainerContentUpdate":
        concentration = Measurement.from_dict(d["concentration"])

        return ContainerContentUpdate(
            concentration=concentration,
        )
