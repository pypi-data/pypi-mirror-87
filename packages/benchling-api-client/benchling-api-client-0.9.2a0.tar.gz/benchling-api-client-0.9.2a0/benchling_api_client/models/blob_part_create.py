from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class BlobPartCreate:
    """  """

    part_number: int
    data64: str
    md5: str

    def to_dict(self) -> Dict[str, Any]:
        part_number = self.part_number
        data64 = self.data64
        md5 = self.md5

        properties: Dict[str, Any] = dict()

        properties["partNumber"] = part_number
        properties["data64"] = data64
        properties["md5"] = md5
        return properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BlobPartCreate":
        part_number = d["partNumber"]

        data64 = d["data64"]

        md5 = d["md5"]

        return BlobPartCreate(
            part_number=part_number,
            data64=data64,
            md5=md5,
        )
