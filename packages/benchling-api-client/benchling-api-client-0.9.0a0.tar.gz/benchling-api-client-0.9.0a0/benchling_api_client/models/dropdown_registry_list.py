from typing import Any, Dict, List

import attr

from ..models.dropdown_summary import DropdownSummary


@attr.s(auto_attribs=True)
class DropdownRegistryList:
    """  """

    dropdowns: List[DropdownSummary]

    def to_dict(self) -> Dict[str, Any]:
        dropdowns = []
        for dropdowns_item_data in self.dropdowns:
            dropdowns_item = dropdowns_item_data.to_dict()

            dropdowns.append(dropdowns_item)

        properties: Dict[str, Any] = dict()

        properties["dropdowns"] = dropdowns
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DropdownRegistryList":
        dropdowns = []
        for dropdowns_item_data in d["dropdowns"]:
            dropdowns_item = DropdownSummary.from_dict(dropdowns_item_data)

            dropdowns.append(dropdowns_item)

        return DropdownRegistryList(
            dropdowns=dropdowns,
        )
