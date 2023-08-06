from typing import Any, Dict, List

import attr

from ..models.label_template import LabelTemplate


@attr.s(auto_attribs=True)
class LabelTemplatesList:
    """  """

    label_templates: List[LabelTemplate]

    def to_dict(self) -> Dict[str, Any]:
        label_templates = []
        for label_templates_item_data in self.label_templates:
            label_templates_item = label_templates_item_data.to_dict()

            label_templates.append(label_templates_item)

        properties: Dict[str, Any] = dict()

        properties["labelTemplates"] = label_templates
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "LabelTemplatesList":
        label_templates = []
        for label_templates_item_data in d["labelTemplates"]:
            label_templates_item = LabelTemplate.from_dict(label_templates_item_data)

            label_templates.append(label_templates_item)

        return LabelTemplatesList(
            label_templates=label_templates,
        )
