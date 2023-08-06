from typing import Any, Dict, List

import attr

from ..models.dropdown_summary import DropdownSummary


@attr.s(auto_attribs=True)
class DropdownSummaryList:
    """  """

    dropdowns: List[DropdownSummary]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        dropdowns = []
        for dropdowns_item_data in self.dropdowns:
            dropdowns_item = dropdowns_item_data.to_dict()

            dropdowns.append(dropdowns_item)

        next_token = self.next_token

        properties: Dict[str, Any] = dict()

        properties["dropdowns"] = dropdowns
        properties["nextToken"] = next_token
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DropdownSummaryList":
        dropdowns = []
        for dropdowns_item_data in d["dropdowns"]:
            dropdowns_item = DropdownSummary.from_dict(dropdowns_item_data)

            dropdowns.append(dropdowns_item)

        next_token = d["nextToken"]

        return DropdownSummaryList(
            dropdowns=dropdowns,
            next_token=next_token,
        )
