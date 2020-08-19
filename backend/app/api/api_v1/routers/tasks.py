import pickle

from fastapi import APIRouter, Depends, HTTPException
from pydantic.types import UUID4

from app.crud.celery_crud import get_task_status
from app.db.session import get_db

task_router = t = APIRouter()


@t.get('/tasks/{task_id}')
def task_details(
        task_id: UUID4,
        db=Depends(get_db),
):
    db_task = get_task_status(db, str(task_id))
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task ID not found")
    # Due to an error in the Celery code results are stored in the backend as pickles
    # regardless of the serializer chosen(JSON is the default). That is why we must
    # unpickle the result before returning(Pydantic does not support pickles)
    # https://github.com/celery/celery/pull/5907
    # Check to make sure the result exists before unpickling
    if db_task.result:
        raw_result = pickle.loads(db_task.result)
    else:
        raw_result = None
    return {'celery_id': task_id, 'task_state': db_task.status, 'db_obj': raw_result}
