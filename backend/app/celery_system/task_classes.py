from enum import Enum
from typing import TypedDict


class TaskStates(str, Enum):
    STARTING = "STARTING"
    OCR_FAILURE = "OCR-FAILURE"
    AWS_FAILURE = "AWS-FAILURE"
    SUCCESS = "SUCCESS"

    def __str__(self):
        return str(self.value)


class TaskTypes(str, Enum):
    """
    List of all task types, used for reference in the database
    """
    CCF = "Criminal-Complaint-Form"

    def __str__(self):
        return str(self.value)


class TaskReturnValue(TypedDict):
    id: int
    type: TaskTypes
