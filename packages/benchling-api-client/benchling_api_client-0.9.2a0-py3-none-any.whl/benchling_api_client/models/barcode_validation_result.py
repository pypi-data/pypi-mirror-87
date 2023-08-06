from typing import Any, Dict, Optional

import attr


@attr.s(auto_attribs=True)
class BarcodeValidationResult:
    """  """

    barcode: str
    is_valid: bool
    message: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        barcode = self.barcode
        is_valid = self.is_valid
        message = self.message

        properties: Dict[str, Any] = dict()

        properties["barcode"] = barcode
        properties["isValid"] = is_valid
        properties["message"] = message
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BarcodeValidationResult":
        barcode = d["barcode"]

        is_valid = d["isValid"]

        message = d["message"]

        return BarcodeValidationResult(
            barcode=barcode,
            is_valid=is_valid,
            message=message,
        )
