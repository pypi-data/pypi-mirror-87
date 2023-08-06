from typing import Any, Dict, Optional, cast

import attr

from ..models.validation_status import ValidationStatus
from ..types import UNSET


@attr.s(auto_attribs=True)
class UserValidation:
    """  """

    validation_status: Optional[ValidationStatus] = cast(None, UNSET)
    validation_comment: Optional[str] = cast(None, UNSET)

    def to_dict(self) -> Dict[str, Any]:
        if self.validation_status is UNSET:
            validation_status = UNSET
        else:
            validation_status = self.validation_status.value if self.validation_status else None

        validation_comment = self.validation_comment

        properties: Dict[str, Any] = dict()

        if validation_status is not UNSET:
            properties["validationStatus"] = validation_status
        if validation_comment is not UNSET:
            properties["validationComment"] = validation_comment
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "UserValidation":
        validation_status = None
        if d.get("validationStatus") is not None:
            validation_status = ValidationStatus(d.get("validationStatus"))

        validation_comment = d.get("validationComment")

        return UserValidation(
            validation_status=validation_status,
            validation_comment=validation_comment,
        )
