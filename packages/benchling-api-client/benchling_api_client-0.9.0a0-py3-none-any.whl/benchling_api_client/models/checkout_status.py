from enum import Enum


class CheckoutStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    CHECKED_OUT = "CHECKED_OUT"
