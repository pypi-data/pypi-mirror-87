from typing import Any, Dict, Optional

import attr


@attr.s(auto_attribs=True)
class Measurement:
    """  """

    value: Optional[float]
    units: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        units = self.units

        properties: Dict[str, Any] = dict()

        properties["value"] = value
        properties["units"] = units
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Measurement":
        value = d["value"]

        units = d["units"]

        return Measurement(
            value=value,
            units=units,
        )
