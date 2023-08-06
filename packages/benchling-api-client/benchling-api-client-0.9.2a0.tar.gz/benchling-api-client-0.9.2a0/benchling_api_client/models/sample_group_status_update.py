from typing import Any, Dict

import attr

from ..models.sample_group_status import SampleGroupStatus


@attr.s(auto_attribs=True)
class SampleGroupStatusUpdate:
    """  """

    sample_group_id: str
    status: SampleGroupStatus

    def to_dict(self) -> Dict[str, Any]:
        sample_group_id = self.sample_group_id
        status = self.status.value

        properties: Dict[str, Any] = dict()

        properties["sampleGroupId"] = sample_group_id
        properties["status"] = status
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SampleGroupStatusUpdate":
        sample_group_id = d["sampleGroupId"]

        status = SampleGroupStatus(d["status"])

        return SampleGroupStatusUpdate(
            sample_group_id=sample_group_id,
            status=status,
        )
