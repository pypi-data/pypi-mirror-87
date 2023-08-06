from typing import Any, Dict, List

import attr

from ..models.project import Project


@attr.s(auto_attribs=True)
class ProjectList:
    """  """

    next_token: str
    projects: List[Project]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        projects = []
        for projects_item_data in self.projects:
            projects_item = projects_item_data.to_dict()

            projects.append(projects_item)

        properties: Dict[str, Any] = dict()

        properties["nextToken"] = next_token
        properties["projects"] = projects
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ProjectList":
        next_token = d["nextToken"]

        projects = []
        for projects_item_data in d["projects"]:
            projects_item = Project.from_dict(projects_item_data)

            projects.append(projects_item)

        return ProjectList(
            next_token=next_token,
            projects=projects,
        )
