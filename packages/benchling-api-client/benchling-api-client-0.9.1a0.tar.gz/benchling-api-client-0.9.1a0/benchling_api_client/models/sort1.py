from enum import Enum


class Sort1(str, Enum):
    BARCODE = "barcode"
    MODIFIEDAT = "modifiedAt"
    NAME = "name"
    BARCODEASC = "barcode:asc"
    MODIFIEDATASC = "modifiedAt:asc"
    NAMEASC = "name:asc"
    BARCODEDESC = "barcode:desc"
    MODIFIEDATDESC = "modifiedAt:desc"
    NAMEDESC = "name:desc"
