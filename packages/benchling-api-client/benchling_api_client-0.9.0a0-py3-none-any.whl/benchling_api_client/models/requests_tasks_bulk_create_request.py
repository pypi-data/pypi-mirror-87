from typing import Any, Dict, List

import attr

from ..models.request_tasks_bulk_create import RequestTasksBulkCreate


@attr.s(auto_attribs=True)
class RequestsTasksBulkCreateRequest:
    """  """

    tasks: List[RequestTasksBulkCreate]

    def to_dict(self) -> Dict[str, Any]:
        tasks = []
        for tasks_item_data in self.tasks:
            tasks_item = tasks_item_data.to_dict()

            tasks.append(tasks_item)

        properties: Dict[str, Any] = dict()

        properties["tasks"] = tasks
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RequestsTasksBulkCreateRequest":
        tasks = []
        for tasks_item_data in d["tasks"]:
            tasks_item = RequestTasksBulkCreate.from_dict(tasks_item_data)

            tasks.append(tasks_item)

        return RequestsTasksBulkCreateRequest(
            tasks=tasks,
        )
