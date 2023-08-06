from enum import Enum


class Reason1(str, Enum):
    MADE_IN_ERROR = "Made in error"
    RETIRED = "Retired"
    OTHER = "Other"
