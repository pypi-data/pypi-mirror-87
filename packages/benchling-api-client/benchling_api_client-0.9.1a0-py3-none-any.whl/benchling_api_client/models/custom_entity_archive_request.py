from typing import Any, Dict, List

import attr

from ..models.reason import Reason


@attr.s(auto_attribs=True)
class CustomEntityArchiveRequest:
    """The request body for archiving custom entities."""

    reason: Reason
    custom_entity_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason.value

        custom_entity_ids = self.custom_entity_ids

        properties: Dict[str, Any] = dict()

        properties["reason"] = reason
        properties["customEntityIds"] = custom_entity_ids
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CustomEntityArchiveRequest":
        reason = Reason(d["reason"])

        custom_entity_ids = d["customEntityIds"]

        return CustomEntityArchiveRequest(
            reason=reason,
            custom_entity_ids=custom_entity_ids,
        )
