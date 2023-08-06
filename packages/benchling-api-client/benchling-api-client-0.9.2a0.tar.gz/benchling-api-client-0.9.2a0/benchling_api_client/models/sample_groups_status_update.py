from typing import Any, Dict, List

import attr

from ..models.sample_group_status_update import SampleGroupStatusUpdate


@attr.s(auto_attribs=True)
class SampleGroupsStatusUpdate:
    """ Specification to update status of sample groups on the request which were executed. """

    sample_groups: List[SampleGroupStatusUpdate]

    def to_dict(self) -> Dict[str, Any]:
        sample_groups = []
        for sample_groups_item_data in self.sample_groups:
            sample_groups_item = sample_groups_item_data.to_dict()

            sample_groups.append(sample_groups_item)

        properties: Dict[str, Any] = dict()

        properties["sampleGroups"] = sample_groups
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SampleGroupsStatusUpdate":
        sample_groups = []
        for sample_groups_item_data in d["sampleGroups"]:
            sample_groups_item = SampleGroupStatusUpdate.from_dict(sample_groups_item_data)

            sample_groups.append(sample_groups_item)

        return SampleGroupsStatusUpdate(
            sample_groups=sample_groups,
        )
