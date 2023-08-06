from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class AsyncTaskLink:
    """  """

    task_id: str

    def to_dict(self) -> Dict[str, Any]:
        task_id = self.task_id

        properties: Dict[str, Any] = dict()

        properties["taskId"] = task_id
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AsyncTaskLink":
        task_id = d["taskId"]

        return AsyncTaskLink(
            task_id=task_id,
        )
