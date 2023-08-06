import datetime
from typing import Any, Dict

import attr
from dateutil.parser import isoparse

from ..models.sample_group import SampleGroup
from ..models.sample_group_status import SampleGroupStatus


@attr.s(auto_attribs=True)
class RequestFulfillment:
    """A request fulfillment represents work that is done which changes the status of a request or a sample group within that request.
    Fulfillments are created when state changes between IN_PROGRESS, COMPLETED, or FAILED statuses. Fulfillments do not capture a PENDING state because all requests or request sample groups are considered PENDING until the first corresponding fulfillment is created.
    """

    id: str
    created_at: datetime.datetime
    entry_id: str
    request_id: str
    status: SampleGroupStatus
    sample_group: SampleGroup

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        created_at = self.created_at.isoformat()

        entry_id = self.entry_id
        request_id = self.request_id
        status = self.status.value

        sample_group = self.sample_group.to_dict()

        properties: Dict[str, Any] = dict()

        properties["id"] = id
        properties["createdAt"] = created_at
        properties["entryId"] = entry_id
        properties["requestId"] = request_id
        properties["status"] = status
        properties["sampleGroup"] = sample_group
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RequestFulfillment":
        id = d["id"]

        created_at = isoparse(d["createdAt"])

        entry_id = d["entryId"]

        request_id = d["requestId"]

        status = SampleGroupStatus(d["status"])

        sample_group = SampleGroup.from_dict(d["sampleGroup"])

        return RequestFulfillment(
            id=id,
            created_at=created_at,
            entry_id=entry_id,
            request_id=request_id,
            status=status,
            sample_group=sample_group,
        )
