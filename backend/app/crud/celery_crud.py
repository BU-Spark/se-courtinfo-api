from typing import Optional

from sqlalchemy.orm import Session
from celery.backends.database import models as celery_models


def get_task_status(db: Session, task_id: str) -> Optional[celery_models.Task]:
    task = db.query(celery_models.Task).filter(
        celery_models.Task.task_id == task_id).first()
    print('found:', task.result)
    return task
