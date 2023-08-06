from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class LabelTemplate:
    """  """

    id: str
    name: str
    zpl_template: str

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        zpl_template = self.zpl_template

        properties: Dict[str, Any] = dict()

        properties["id"] = id
        properties["name"] = name
        properties["zplTemplate"] = zpl_template
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "LabelTemplate":
        id = d["id"]

        name = d["name"]

        zpl_template = d["zplTemplate"]

        return LabelTemplate(
            id=id,
            name=name,
            zpl_template=zpl_template,
        )
