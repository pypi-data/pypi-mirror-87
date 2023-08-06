from enum import Enum


class UploadStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    ABORTED = "ABORTED"
