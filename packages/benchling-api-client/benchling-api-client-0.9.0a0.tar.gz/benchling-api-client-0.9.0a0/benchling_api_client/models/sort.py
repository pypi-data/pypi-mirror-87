from enum import Enum


class Sort(str, Enum):
    MODIFIEDAT = "modifiedAt"
    NAME = "name"
    MODIFIEDATASC = "modifiedAt:asc"
    NAMEASC = "name:asc"
    MODIFIEDATDESC = "modifiedAt:desc"
    NAMEDESC = "name:desc"
