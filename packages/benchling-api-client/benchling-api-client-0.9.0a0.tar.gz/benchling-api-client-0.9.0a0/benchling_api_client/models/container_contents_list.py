from typing import Any, Dict, List

import attr

from ..models.container_content import ContainerContent


@attr.s(auto_attribs=True)
class ContainerContentsList:
    """  """

    contents: List[ContainerContent]

    def to_dict(self) -> Dict[str, Any]:
        contents = []
        for contents_item_data in self.contents:
            contents_item = contents_item_data.to_dict()

            contents.append(contents_item)

        properties: Dict[str, Any] = dict()

        properties["contents"] = contents
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ContainerContentsList":
        contents = []
        for contents_item_data in d["contents"]:
            contents_item = ContainerContent.from_dict(contents_item_data)

            contents.append(contents_item)

        return ContainerContentsList(
            contents=contents,
        )
