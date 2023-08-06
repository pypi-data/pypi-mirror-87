from typing import Any, Dict, List

import attr

from ..models.requests_task_base import RequestsTaskBase


@attr.s(auto_attribs=True)
class RequestsTasksBulkUpdateRequest:
    """A request body for bulk updating request tasks."""

    tasks: List[RequestsTaskBase]

    def to_dict(self) -> Dict[str, Any]:
        tasks = []
        for tasks_item_data in self.tasks:
            tasks_item = tasks_item_data.to_dict()

            tasks.append(tasks_item)

        properties: Dict[str, Any] = dict()

        properties["tasks"] = tasks
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RequestsTasksBulkUpdateRequest":
        tasks = []
        for tasks_item_data in d["tasks"]:
            tasks_item = RequestsTaskBase.from_dict(tasks_item_data)

            tasks.append(tasks_item)

        return RequestsTasksBulkUpdateRequest(
            tasks=tasks,
        )
