from typing import Any, Dict, Optional, Union, cast

import attr

from ..models.archive_record import ArchiveRecord
from ..models.organization import Organization
from ..models.user_summary import UserSummary
from ..types import UNSET


@attr.s(auto_attribs=True)
class Project:
    """  """

    id: Optional[str] = cast(None, UNSET)
    name: Optional[str] = cast(None, UNSET)
    archive_record: Optional[ArchiveRecord] = cast(None, UNSET)
    owner: Optional[Union[Optional[Organization], Optional[UserSummary]]] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        if self.archive_record is UNSET:
            archive_record = UNSET
        else:
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        if self.owner is None:
            owner: Optional[Union[Optional[Organization], Optional[UserSummary]]] = None
        elif self.owner is UNSET:
            owner = UNSET
        elif isinstance(self.owner, Organization):
            if self.owner is UNSET:
                owner = UNSET
            else:
                owner = self.owner.to_dict() if self.owner else None

        else:
            if self.owner is UNSET:
                owner = UNSET
            else:
                owner = self.owner.to_dict() if self.owner else None

        properties: Dict[str, Any] = dict()

        if id is not UNSET:
            properties["id"] = id
        if name is not UNSET:
            properties["name"] = name
        if archive_record is not UNSET:
            properties["archiveRecord"] = archive_record
        if owner is not UNSET:
            properties["owner"] = owner
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Project":
        id = d.get("id")

        name = d.get("name")

        archive_record = None
        if d.get("archiveRecord") is not None:
            archive_record = ArchiveRecord.from_dict(cast(Dict[str, Any], d.get("archiveRecord")))

        def _parse_owner(data: Dict[str, Any]) -> Optional[Union[Optional[Organization], Optional[UserSummary]]]:
            owner: Optional[Union[Optional[Organization], Optional[UserSummary]]]
            try:
                owner = None
                if d.get("owner") is not None:
                    owner = Organization.from_dict(cast(Dict[str, Any], d.get("owner")))

                return owner
            except:  # noqa: E722
                pass
            owner = None
            if d.get("owner") is not None:
                owner = UserSummary.from_dict(cast(Dict[str, Any], d.get("owner")))

            return owner

        owner = _parse_owner(d.get("owner"))

        return Project(
            id=id,
            name=name,
            archive_record=archive_record,
            owner=owner,
        )
