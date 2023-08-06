from typing import Any, Dict, List

import attr

from ..models.dropdown_patch_option import DropdownPatchOption


@attr.s(auto_attribs=True)
class DropdownPatch:
    """  """

    options: List[DropdownPatchOption]

    def to_dict(self) -> Dict[str, Any]:
        options = []
        for options_item_data in self.options:
            options_item = options_item_data.to_dict()

            options.append(options_item)

        properties: Dict[str, Any] = dict()

        properties["options"] = options
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DropdownPatch":
        options = []
        for options_item_data in d["options"]:
            options_item = DropdownPatchOption.from_dict(options_item_data)

            options.append(options_item)

        return DropdownPatch(
            options=options,
        )
