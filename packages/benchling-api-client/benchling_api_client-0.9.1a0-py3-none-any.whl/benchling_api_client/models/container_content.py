from typing import Any, Dict

import attr

from ..models.measurement import Measurement


@attr.s(auto_attribs=True)
class ContainerContent:
    """  """

    concentration: Measurement

    def to_dict(self) -> Dict[str, Any]:
        concentration = self.concentration.to_dict()

        properties: Dict[str, Any] = dict()

        properties["concentration"] = concentration
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ContainerContent":
        concentration = Measurement.from_dict(d["concentration"])

        return ContainerContent(
            concentration=concentration,
        )
