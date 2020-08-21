from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel
from pydantic.types import UUID4

from app.celery_system.task_classes import TaskStates


class TaskStatus(BaseModel):
    task_id: UUID4
    state: TaskStates
    created_object_id: int


class CeleryTaskmetaBase(BaseModel):
    id: int
    task_id: str
    status: str
    result: Optional[str]
    date_done: Optional[datetime]
    traceback: Optional[str]
    name: str

    class Config:
        orm_mode = True
