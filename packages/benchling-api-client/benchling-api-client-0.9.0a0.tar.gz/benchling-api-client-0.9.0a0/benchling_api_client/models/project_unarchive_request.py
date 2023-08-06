from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class ProjectUnarchiveRequest:
    """  """

    project_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        project_ids = self.project_ids

        properties: Dict[str, Any] = dict()

        properties["projectIds"] = project_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ProjectUnarchiveRequest":
        project_ids = d["projectIds"]

        return ProjectUnarchiveRequest(
            project_ids=project_ids,
        )
