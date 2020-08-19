from typing import Optional

from sqlalchemy.orm import Session

from app.models import celery_models


def get_task_status(db: Session, task_id: str) -> Optional[celery_models.CeleryTaskmeta]:
    task = db.query(celery_models.CeleryTaskmeta).filter(
        celery_models.CeleryTaskmeta.task_id == task_id).first()
    return task
